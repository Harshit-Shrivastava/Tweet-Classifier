import tweepy

API_KEY = "kjhjED58EIPLCB0jTJr9KUCjW"
API_SECRET = "rpg8LzlXjG27FvfdGnuNi1vjNWWsZzsV5SVHf4nKXIvtZ58nfK"

auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify= True)

#get tweets by a user
#pass the Twitter handler without the @ character
#user = api.get_user("SrishtiParakh")
#userFollowers = user.followers()
#tweets = user.timeline()
#for t in tweets:
#    print t.text
#    print ("*"*50)

#get followers of a user
# for f in userFollowers[:10]:
#     print(f.name)
#     print(f.description)
#     print("*"*50)

# geolocation = []
# for f in user.friends():
#     l = f.location
#     print l
#     geolocation.append(l)

# #search based on a query
# search_results = api.search(q="ISRO", lang="hi")
# for status in search_results[:10]:
#     print(status.text)
#     print(status.created_at)
#     print("*"*50)

#find what is trending in a particular region
#takes a woeid
#trending_us is a JSON object
# trending_us = api.trends_place(23424977)
# theObject = trending_us[0]
# theTrends = theObject['trends']
# first_trend = theTrends[0]
# print first_trend['tweet_volume']
# print first_trend['url']
# for trend in theTrends[:10]:
#     print(trend['name'], trend['tweet_volume'])
#     #None tweet count means that this trending happened in last 24 hours, so no statistcics on it yet

# trends_russia = api.trends_place(23424936)
# for trend in trends_russia[0]['trends'][:5]:
#     print(trend['name'])

#iterating over large datasets
# search_results = api.search(q="#StarTrek50")
# print len(search_results)

# user = api.get_user("IUBloomington")
# followers = user.followers()
# print len(followers)
# print user.followers_count

#Twitter rate limit issue
#Every API client can make only a certain amount of requests every minute
#create a cursor object
#give parameters to the Cursor method, not to the search method
c = tweepy.Cursor(api.search, q = "Business", lang = "en")

#cannot save the results, however, can iterate over them
tweet_store=[]
for status in c.items(1000):
    statusText = status.text
    tweet_store.append(statusText)
print tweet_store
print len(tweet_store)

#Getting a user's tweets
#c = tweepy.Cursor(api.user_timeline, id="SrishtiParakh")
#tweet_store = []
#for status in c.items(100):
#    tweet_store.append(status.text)

#print tweet_store
#print len(tweet_store)

#for item in tweet_store:
#    print item.text

#Twitter search API is limited to Tweets published in the past 7 days only
#This limit applies to Twitter Search API, but not on user timelines

#Workaround
#Use search API to find out who has been talking about a certain topic within the last 7 days
#Find most prolific authors among those tweets: perform frequency distribution on the authors who
#contribute the most on this topic
#Get tweets of those authors using user_timeline
#Pro: you now have a set of tweets that cover more than 7 days
#Con: your sample is far from representative
