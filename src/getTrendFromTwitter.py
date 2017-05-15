#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy
import sys,pprint
import py2neo

def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


consumer_key = 'OTrre8uKO6ztvBjWMVSTKfvPP'
consumer_secret = 'kP42EJH0DXgcyGZpFwZMVJlczkJ4p52H3EEjCg9kg8AzJUVDOT'
access_token = '35557346-dIV0lKIECFm2OlItayxmZG7ll7LBuiz6sF8k17uJv'
access_token_secret = 'DEMs0W8nfpUplvJA7XZDNOmvVUNHfnwUgNTK4wg6mNyXd'


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
trends1 = api.trends_place(1)

data = trends1[0]
# grab the trends
trends = data['trends']
# grab the name from each trend
names = [trend['name'].encode() for trend in trends]
# put all the names together with a ' ' separating them
#trendsName = ' '.join(names)
#print(names)

for n in names :
	if isEnglish(n) and 'Feliz' not in n.decode():
		print(n.decode("utf"))
		nd = n.decode("utf")

		results = api.search(q=nd,lang="en", rpp=100)
		for r in results :
			pprint.pprint(r._json["user"])

			screenName = r._json["user"]["screen_name"]
			id = r._json["user"]["id"]
			nbFollowers = r._json["user"]["followers_count"]
			nbFriends = r._json["user"]["friends_count"]

			followers = api.followers(id)
			print(len(followers))



		sys.exit()
