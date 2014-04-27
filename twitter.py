from twython import Twython
import threading
import os
from datetime import datetime

#this demo posts tweets from piworkshop (https://twitter.com/piworkshop)



class TweetThread(threading.Thread):

    def __init__(self,message):
        super(TweetThread,self).__init__()
        self.message = message
        self.twitter = Twython(
            #consumer key
            "fF86BdSdopE9FAES5UNgPw",
            #consumer secret
            "n7G4K80kYQ6NDMQiYn3GY5Hyk82fF2So17Nl1UQdGWE",
            #access_token
            "1336977176-4CgpPJnJBx7kCRqnwLcRbXI3nLpHj44sp3r2bXy",
            #access_token_secret
            "5rLNvZm3JZdkx0K1Jx9jgsqMG6MmGLAQmPdJ7ChtzA",
        )

    def run(self):
        #send a picture tweet
        print("sending a tweet with an image...")
        photo = open('mugshot.jpg', 'rb')
        try:
            self.twitter.update_status_with_media(media=photo, status=self.message)
            print("sent")
        except:
            print("twython problem")


