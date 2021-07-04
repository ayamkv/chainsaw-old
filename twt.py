import tweepy 
from keys import apikey, apikey_secret, token, token_secret

auth = tweepy.OAuthHandler(apikey, apikey_secret)
auth_url = auth.get_authorization_url()
auth.set_access_token(token, token_secret)
api = tweepy.API(auth)
print('Auth success')
print ("Authenticated as: %s" % api.me().screen_name)   

msg = '[ #CSM866 #CSM867 ] Im moving the #ChainsawManFrames Tweet at this account \n\n:: @fidenjii'
api.update_status(msg)
print('Tweeted')
