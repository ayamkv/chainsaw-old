import tweepy, sys, time
from keys import apikey, apikey_secret, token, token_secret

auth = tweepy.OAuthHandler(apikey, apikey_secret)
auth_url = auth.get_authorization_url()
auth.set_access_token(token, token_secret)
api = tweepy.API(auth)

desc = ("Latest Tweet From Fiiouus: %s" % api.me().screen_name)  
tweetL = api.user_timeline(screen_name=("%s" % api.me().screen_name), tweet_mode="extended", include_entities=True)

screen_name = ("%s" % api.me().screen_name)



last_tweet = next((tw for tw in tweetL if tw.in_reply_to_screen_name is None
                or tw.in_reply_to_screen_name == screen_name), None)


tL = last_tweet.full_text

tick, frame, fnumber, *texts, tLink = tL.split()

def get_last_tweet_id(api):
    tweet = api.user_timeline(
        id = screen_name, 
        count = 1, 
        tweet_mode="extended", 
        include_entities=True 
        )[0]
    print(tweet.id)
    return tweet.id
    

id_tweet = get_last_tweet_id(api)
print(fnumber)


