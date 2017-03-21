import tweepy
import os
import glob

#credentials for the app
API_KEY = "kjhjED58EIPLCB0jTJr9KUCjW"
API_SECRET = "rpg8LzlXjG27FvfdGnuNi1vjNWWsZzsV5SVHf4nKXIvtZ58nfK"

#set basic authentication
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify= True)

#function to get tweets by a user
#input: user handle
#returns: list object containing tweets
def userTweets(user):
    tweetStore = []
    c = tweepy.Cursor(api.user_timeline, id=user)
    for status in c.items(500):
        tweetStore.append(status.text)
    #print tweetStore
    return tweetStore

#function to get tweets containing a hashtag
#input: hashtag
#returns: list object containing tweets
def hashtagTweets(hashtag):
    tweetStore = []
    c = tweepy.Cursor(api.search, q=hashtag, lang="en")
    for status in c.items(500):
        tweetStore.append(status.text)
    print tweetStore
    return tweetStore

#function to get tweets containing a keyword
#input: keyword
#returns: list object containing tweets
def keywordTweets(keyword):
    return []

#function to create folders for a topic for test and train data
#input: none
#returns: none
def createFolders():
    os.chdir('../Data/Topics')
    for file in glob.glob('*.txt'):
        folderName = os.path.splitext(file)[0]
        trainFolder = os.path.join('../train', folderName)
        testFolder = os.path.join('../test', folderName)
        if not os.path.exists(trainFolder):
            os.makedirs(trainFolder)
        if not os.path.exists(testFolder):
            os.makedirs(testFolder)
    return

def readTopic(file):
    directory = 'C:/SP17/SMM/Project/Data/Topics/'
    with open(directory + file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('@'):
                #line represents a user, pass to the function userTweets, and then to createTweetData
                createTweetData(userTweets(line[1:]), file)
            elif line.startswith('#'):
                #line represents a hashtag, pass to the function hashTagTweets, and then to createTweetData
                createTweetData(hashtagTweets(line[1:]), file)
            else:
                if line.startswith('@'):
                # line represents a user, pass to the function userTweets, and then to createTweetData
                    createTweetData(keywordTweets(line), file)
    return

#function to create individual file for each tweet
#input: list of tweets for a topic, topic
#returns: none
def createTweetData(tweetList, file):
    return

#function to parse over the topics
#input: path to the topics folder
#returns: none
def readAllTopics(topicsFolder):
    os.chdir('C:/SP17/SMM/Project/Data/Topics')
    for file in glob.glob('*.txt'):
        readTopic(file)
    return

# def readFile(topic):
#     tweetBag = []
#
#     word = ''
#     if word.startswith('#'):
#         tweetBag.append(hashtagTweets(word))
#     elif word.startswith('@'):
#         tweetBag.append(userTweets(word))
#     else:
#         tweetBag.append(keywordTweets(word))

#function to pull tweets for a topic for both test and train
#input: topic
#returns: none
def pullTweets():
    createFolders()
    readAllTopics('../Data/Topics')
    return

if __name__ == "__main__":
    pullTweets()