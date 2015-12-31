"""
REDDIT CURRENCY CONVERSION BOT V0.2
Parses submission titles for currency values and replies with a comment
containing converted values between USD, GBP, and EUR
using up-to-date exchange rates from the fixer.io API
DEPEDENCIES:
PRAW (Python Reddit API Wrapper)
OAuth2Util
currencyconverter library for python (available at my github profile - github.com/cp2846)
"""

import currencyconverter
import praw
import time
import OAuth2Util
import os

class CurrencyBot:
    def __init__(self, subreddits):
        if not os.path.isfile("posts_replied_to.txt"):
            self.posts_replied_to = []
            print "no file"
        else:
            with open("posts_replied_to.txt", "r") as f:
                self.posts_replied_to = f.read()
                self.posts_replied_to = self.posts_replied_to.split("\n")
                self.posts_replied_to = filter(None, self.posts_replied_to)
        self.subreddits = subreddits
        self.signature = "***\n\nCurrent exchange rates from [fixer.io](http://fixer.io) | [Source](https://github.com/cp2846/reddit-currency-bot) | [Contact](https://www.reddit.com/message/compose/?to=Psychovyle)"
   
    #save replied posts in txt file 
    def writeFile(self):
        with open("posts_replied_to.txt", "w") as f:
            for post_id in self.posts_replied_to:
                f.write(post_id + "\n")                
    #generate and post reply
    def generateComment(self, submission, results):
        conversions = ""
        for result in results:
            conversions  += "\n\n" + converter.convert(result)
        try:
            submission.add_comment(">" + submission.title + "\n\n" + conversions + "\n\n" + self.signature)
            print "Successfully added comment on submission " + submission.id
            posts_replied_to.append(submission.id)
        except:
            print "Error encountered on submission " + submission.id 
    def run(self):
        o.refresh(force=True)
        for subreddit in self.subreddits:
            print "Searching submissions in r/" + subreddit
            s = r.get_subreddit(subreddit)
            submissions = s.get_hot(limit=25)
            
            for submission in submissions:
                title_text = submission.title.encode("utf-8")
                detected_currency = converter.parse_string(title_text)
                if len(detected_currency) > 0 and submission.id not in self.posts_replied_to:
                    print "found one! attempting to reply... "
                    self.generateComment(submission, detected_currency)
        self.writeFile()
        print "Sleeping... "
        time.sleep(3600)
        
        
r = praw.Reddit(user_agent = "Reddit Currency Exchange Bot by /u/Psychovyle")
o = OAuth2Util.OAuth2Util(r)
converter = currencyconverter.Converter()
#instantiate bot with list of subreddits to crawl        
bot = CurrencyBot(["test"])
while True:
    bot.run()