import json
import tweepy
from tweeter import Tweeter

from config import *
'''
data = {}
data['authOpts'] = []

data['authOpts'].append({
    'name': '',
    'token': 'google.com',
    'secret': 'Michigan'
})
'''

def getNewAuth():

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

    tokenDict = {"token" : auth.access_token, "secret" : auth.access_token_secret}

    # tokenDict = {"token" : "asdkflasjd token", "secret" : "asdfkasdjfas secret"}
    return tokenDict


def getAuthOptions():
    data = {}
    returnAuths = {}
    with open('auths.json', 'a+') as auth_file:
        auth_file.seek(0)
        file = auth_file.read()
        #auth_file = '{"authOpts": [{"name": "aldsfkajs", "token": "asdkflasjd token", "secret": "asdfkasdjfas secret"}]}'
        auth_file.seek(0, 0)
        try:
            data = json.loads(file)
            if 'authOpts' not in data:
                #we don't, time to just jump to the asking for things
                data['authOpts'] = []
        except ValueError as e:
            print(str(e))
            data['authOpts'] = []

    with open('auths.json', 'r+') as auth_file:
        printstr = "Let's start with an account. Select from the authorized options or add a new one!\n"
        authOpts = data['authOpts']
        for option in authOpts:
            printstr += "\t" + option["name"] + "\n"

        printstr += "Enter -1 to add a new account\n\t-->"

        acct = input(printstr)
        if acct == "-1":
            acctName = input("Please enter the nickname for this new account: ")
            auth = getNewAuth()
            data['authOpts'].append({
                'name': acctName,
                'token': auth["token"],
                'secret': auth["secret"]
            })

            json.dump(data, auth_file)
            auth_file.truncate()
            returnAuths["token"] = auth["token"]
            returnAuths["secret"] = auth["secret"]
            return returnAuths
        else:
            for acctOpts in data['authOpts']:
                if acctOpts['name'] == acct:
                    returnAuths["token"] = acctOpts['token']
                    returnAuths["secret"] = acctOpts['secret']
                    return returnAuths
        return "auth acquisition unsuccessful, try again later"


def main():
    print("Welcome to my nonary game....\n")
    authDict = getAuthOptions()
    if isinstance(authDict, str):
        print("Unable to get authorization tokens, please try again")
        return
    tweeterer = Tweeter(authDict["token"], authDict["secret"])
    pause = input("wait until it says account set please")
    say_what = input("What do we say? ")
    whom = input("tweet at someone? ")

    tweet = "@%s %s" % (whom, say_what)
    to_send = input("do you want to send this tweet?")
    if to_send == "yes":
        tweeterer.send_tweet(tweet)

    '''
    whom = input("tweet at someone? ")
    say_what = input("What do we say? ")
    tweeterer = Tweeter(authDict["token"], authDict["secret"])
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
    # print("Tweet sent!!")
    '''

if __name__=="__main__":
    main()
