'''
09/20/2018
Script for getting auth secret and token for a twitter account, to be used as needed,
keys will be added to config.py and associated with each account
'''

import tweepy
import json

from config import *


def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print ('Error! Failed to get request token.')
        return

    print("please go authorize at the following, do not close the tab until directed. ")
    print (redirect_url)

    # Example w/o callback (desktop)
    verifier = input('Verifier: ')

    try:
        token = auth.get_access_token(verifier)
    except tweepy.TweepError:
        print ('Error! Failed to get access token.')
        return

    if len(token):
        print("TOKENS:  " + token[0] + "  " + token[1] +"\n")
        print("token: " + auth.access_token +"\n")
        print("secret: " + auth.access_token_secret)


if __name__=="__main__":
    main()
