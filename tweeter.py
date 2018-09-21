'''
09/20/2018
copying over/updating to work as a standalone script
'''

import tweepy

from config import *

class Tweeter:
    API = None
    last_mention_id = ""
    last_tweeted_id = ""
    last_threaded_tweet = ""
    thread_tweets = True

    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    acccess_token = ""
    access_key = ""

    character_limit = 280

    def __init__(self, account):
        self.set_account(account)

        self.api_connect()


    def api_connect(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        self.API = tweepy.API(auth)


    def set_account(self, account):
        LOG.warning("SETTING ACCOUNT: " + account)
        if account in ACCESS_TOKEN.keys():
            self.access_token = ACCESS_TOKEN[account]
            self.access_secret = ACCESS_SECRET[account]
        else:
            LOG.error("ACCOUNT "+account+" NOT FOUND, AUTH WILL FAIL")


    def clean_string(self,string):
        #unicode characters like pesky emojis can break processing and output,
        #clear them out
        return "".join((i if ord(i) < 10000 else '\ufffd' for i in string))


    def send_tweet(self, content):
        status = self.API.update_status(content)
        self.last_tweeted_id = status.id_str
        LOG.warn("tweeted with id: "+status.id_str)
        return status.id_str

    def send_thread_tweet(self,content):
        if self.thread_tweets and len(self.last_tweeted_id):
            status = self.API.update_status(content, self.last_tweeted_id)
            id_str = status.id_str
        else:
            id_str = self.send_tweet(content)
        self.last_threaded_tweet = id_str
        self.last_tweeted_id = id_str


    def reply_last_mention(self, content):
        if len(self.last_mention_id):
            status = self.API.update_status(content, self.last_mention_id)
            id_str = status.id_str
        else:
            #cannot reply to last mention if it doesn't exist
            return False


    def clear_thread(self):
        self.last_threaded_tweet = ""


    def set_threading(self, do_it):
        # only try and change if we're sent a boolean
        if isinstance(do_it, bool):
            self.thread_tweets = do_it
            return True
        return False


    def get_mentions(self):
        mentions = tweepy.Cursor(self.API.mentions_timeline).items()
        mention_array = []
        mention_ids = []
        for mention in mentions:
            user = mention.user.name
            text = self.clean_string(mention.text)
            mention_ids.append(mention.id_str)
            mention_array.append((user, text))
        self.last_mention_id = mention_ids[0]
        return mention_array


    def get_last_mention_link(self):
        if len(self.last_mention_id):
            return "https://twitter.com/statuses/"+self.last_mention_id
        #if we don't have an id for last mention, we can't give a link
        return "https://twitter.com"


    def get_last_tweet_link(self):
        if len(self.last_tweeted_id):
            return "https://twitter.com/statuses/"+self.last_tweeted_id
        return "https://twitter.com"

    def keep_tweet_in_characount(self, tweet):
        cutoff = self.character_limit -1
        sizetweet = tweet[:cutoff]
        return sizetweet

def main():
    at = input("Who do we tweet as: lapinstance, foredewindev? ")
    whom = input("tweet at someone? ")
    say_what = input("What do we say? ")
    tweeterer = Tweeter(at)
    pause = input("wait until it says account set please")
    tweet = "@%s %s" % (whom, say_what)
    to_send = input("do you want to send this tweet?")
    if to_send == "yes":
        tweeterer.send_tweet(tweet)
    mentions_get = input("do you want to get your mentions?")
    if mentions_get == "yes":
        mentions = tweeterer.get_mentions()
        print(mentions)
        print("last mention id:: " + tweeterer.last_mention_id)
    #print("Tweet sent!!")


if __name__=="__main__":
    main()
