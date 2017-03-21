from __future__ import unicode_literals
import tweepy
import os
import glob
import random
import string
import shutil

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
    return tweetStore

#function to get tweets containing a hashtag
#input: hashtag
#returns: list object containing tweets
def hashtagTweets(hashtag):
    tweetStore = []
    c = tweepy.Cursor(api.search, q=hashtag, lang="en")
    for status in c.items(500):
        tweetStore.append(status.text)
    return tweetStore

#function to get tweets containing a keyword
#input: keyword
#returns: list object containing tweets
def keywordTweets(keyword):
    tweetStore = []
    c = tweepy.Cursor(api.search, q=keyword, lang="en")
    for status in c.items(500):
        tweetStore.append(status.text)
    return tweetStore

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
        directory = 'C:/SP17/SMM/Project/Data/train/'
        tweetDir = directory + os.path.splitext(file)[0]
        clearRepository(tweetDir)
        lines = f.readlines()
        for line in lines:
            if line.startswith('@'):
                #line represents a user, pass to the function userTweets, and then to createTweetData
                createTweetData(userTweets(line[1:]), file)
            elif line.startswith('#'):
                #line represents a hashtag, pass to the function hashTagTweets, and then to createTweetData
                createTweetData(hashtagTweets(line), file)
            else:
                # line represents a user, pass to the function userTweets, and then to createTweetData
                createTweetData(keywordTweets(line), file)
    return

#function to create random file name for each tweet
#input: length of the file name
#returns: a random word for file name
def randomWord(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

#function to clear the repository before
#input: length of the file name
#returns: a random word for file name
def clearRepository(repository):
    for root, dirs, files in os.walk(repository):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    return

#function to create individual file for each tweet
#input: list of tweets for a topic, topic
#returns: none
def createTweetData(tweetList, file):
    directory = 'C:/SP17/SMM/Project/Data/train/'
    tweetDir = directory + os.path.splitext(file)[0]
    for tweet in tweetList:
        tweetFile = tweetDir + '/' + randomWord(10)
        f = open(tweetFile + '.txt','w+')
        f.write(tweet.encode('utf-8'))
        f.close()
    return

#function to parse over the topics
#input: path to the topics folder
#returns: none
def readAllTopics(topicsFolder):
    os.chdir('C:/SP17/SMM/Project/Data/Topics')
    for file in glob.glob('*.txt'):
        readTopic(file)
    return

#function to pull tweets for a topic for both test and train
#input: topic
#returns: none
def pullTweets():
    createFolders()
    readAllTopics('../Data/Topics')
    print 'Populating tweets, please wait...'
    return

if __name__ == "__main__":
    pullTweets()