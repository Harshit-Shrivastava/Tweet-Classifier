# -*- coding: UTF-8 -*-
from __future__ import division
import os
import numpy
import glob
import pandas
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

NEWLINE = '\n'
#These are the paths for training data
SOURCES = [
    ('Tweet-Classifier/Data/train/politics','Politics'),
    ('Tweet-Classifier/Data/train/sports',    'Sports'),
('Tweet-Classifier/Data/train/education','Education'),
    ('Tweet-Classifier/Data/train/entertainment',    'Entertainment'),
('Tweet-Classifier/Data/train/health','Health'),
    ('Tweet-Classifier/Data/train/nature',    'Nature'),
('Tweet-Classifier/Data/train/startups','Startups')
]
#These are the paths for testing data
SOURCES1 = [
    ('Tweet-Classifier/Data/test/politics','Politics'),
    ('Tweet-Classifier/Data/test/sports',    'Sports'),
('Tweet-Classifier/Data/test/education','Education'),
    ('Tweet-Classifier/Data/test/entertainment',    'Entertainment'),
('Tweet-Classifier/Data/test/health','Health'),
    ('Tweet-Classifier/Data/test/nature',    'Nature'),
('Tweet-Classifier/Data/test/startups','Startups')
]
SKIP_FILES = {'cmds'}
parentDir = os.path.dirname(os.path.dirname(os.getcwd()))

#This function reads the content from the specified path and puts them in a list
def read_files(path):
    path1 = os.path.join(parentDir, path)
    os.chdir(path1)  # changes the current dir to this
    lines=[]
    for file in glob.glob('*.txt'):
        f = open(file)
        for line in f:
            lines.append(line)
        f.close()
        content = NEWLINE.join(lines)
    yield path1, content

#By using Pandas library,this function builds a DataFrame in a format that can be used as an input to the classifier
def build_data_frame(path, classification):
    rows = []
    index = []
    for file_name, text in read_files(path):
        rows.append({'text': text, 'class': classification})
        index.append(file_name)
    data_frame = DataFrame(rows, index=index)
    return data_frame

data = DataFrame({'text': [], 'class': []})
for path, classification in SOURCES:
    data = data.append(build_data_frame(path, classification))

#Using reindex to reshuffle the records to prevent overfitting
data = data.reindex(numpy.random.permutation(data.index))
count_vectorizer = CountVectorizer()
#This extracts word count features
counts = count_vectorizer.fit_transform(data['text'].values)
#We instantiate a new MultinomialNB and train it by calling fit, passing in the feature vector and the target vector
classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)

#Testing
#Confidence matrix
I = pandas.Index(["Politics", "Sports", "Education", "Entertainment","Health","Nature","Startups"])
C = pandas.Index(["Politics", "Sports", "Education", "Entertainment","Health","Nature","Startups"])
confusion = pandas.DataFrame(0, index=I, columns=C)

counter1=0
counter2=0
for path, classification in SOURCES1:
    examples=[]
    text1=""
    for file_name, text in read_files(path):
        text1+=text
    examples=text1.splitlines()
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)
    for i in range(0,len(predictions)-1):
        if predictions[i]==classification:
            confusion[classification][classification]= confusion[classification][classification]+1
            counter1+=1
        else:
            confusion[classification][predictions[i]]=confusion[classification][predictions[i]]+1
            counter2+=1

print(confusion)
print('Accuracy is',(counter1/(counter1+counter2))*100)
