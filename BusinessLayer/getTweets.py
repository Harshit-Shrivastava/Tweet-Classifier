from __future__ import unicode_literals
from os.path import basename
import tweepy
import os
import glob
import random
import string
import shutil

#parent directory for the codebase
parentDir = os.path.dirname(os.path.dirname(os.getcwd()))

#credentials for the app
API_KEY = "kjhjED58EIPLCB0jTJr9KUCjW"
API_SECRET = "rpg8LzlXjG27FvfdGnuNi1vjNWWsZzsV5SVHf4nKXIvtZ58nfK"

#set basic authentication and create API object
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
    path = os.path.join(parentDir, 'Data\\Topics')
    os.chdir(path)
    for file in glob.glob('*.txt'):
        folderName = os.path.splitext(file)[0]
        trainFolder = os.path.join(os.path.join(parentDir, 'Data\\train'), folderName)
        testFolder = os.path.join(os.path.join(parentDir, 'Data\\test'), folderName)
        if not os.path.exists(trainFolder):
            os.makedirs(trainFolder)
        if not os.path.exists(testFolder):
            os.makedirs(testFolder)
    return

#function to read text files named with topics and redirect to respective functions
#input: file
#returns: none
def readTopic(file):
    with open(file, 'r') as f:
        directory = os.path.join(parentDir, 'Data\\train\\')
        tweetDir = os.path.join(directory, os.path.splitext(file)[0])
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
    topic = os.path.splitext(basename(file))[0]
    tweetDir = os.path.join(os.path.join(parentDir, 'Data\\train'), topic)
    for tweet in tweetList:
        tweetFile = os.path.join(tweetDir, randomWord(10))
        f = open(tweetFile + '.txt','w+')
        f.write(tweet.encode('utf-8'))
        f.close()
    return

#function to parse over the topics
#input: path to the topics folder
#returns: none
def readAllTopics(topicsFolder):
    os.chdir(os.path.join(parentDir, 'Data\\Topics\\'))
    for file in glob.glob(os.path.join(os.getcwd(),'*.txt')):
        readTopic(file)
    return

#function to pull tweets for a topic for both test and train
#input: topic
#returns: none
def pullTweets():
    print 'Populating tweets, please wait...'
    createFolders()
    readAllTopics( os.path.join (parentDir, 'Data\\Topics'))
    return

def flaskPOC():
    return "Hello Harshit!"

if __name__ == "__main__":
    pullTweets()