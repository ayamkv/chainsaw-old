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

# print(last_tweet.full_text)
*texts, tLink = tL.split()

