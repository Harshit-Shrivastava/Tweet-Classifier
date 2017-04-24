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
#from sklearn.cross_validation import KFold
#from sklearn.metrics import confusion_matrix, f1_score

NEWLINE = '\n'



SOURCES = [
    ('Tweet-Classifier/Data/train/politics','Politics'),
    ('Tweet-Classifier/Data/train/sports',    'Sports'),
('Tweet-Classifier/Data/train/education','Education'),
    ('Tweet-Classifier/Data/train/entertainment',    'Entertainment'),
('Tweet-Classifier/Data/train/health','Health'),
    ('Tweet-Classifier/Data/train/nature',    'Nature'),
#('Tweet-Classifier/Data/train/news','News'),
    #('Tweet-Classifier/Data/train/business',    'Business'),
('Tweet-Classifier/Data/train/startups','Startups')
    #('Tweet-Classifier/Data/train/travel',    'Travel'),
#('Tweet-Classifier/Data/train/technology',    'Technology')
]

SOURCES1 = [
    ('Tweet-Classifier/Data/test/politics','Politics'),
    ('Tweet-Classifier/Data/test/sports',    'Sports'),
('Tweet-Classifier/Data/test/education','Education'),
    ('Tweet-Classifier/Data/test/entertainment',    'Entertainment'),
('Tweet-Classifier/Data/test/health','Health'),
    ('Tweet-Classifier/Data/test/nature',    'Nature'),
#('Tweet-Classifier/Data/test/news','News'),
    #('Tweet-Classifier/Data/test/business','Business'),
('Tweet-Classifier/Data/test/startups','Startups')
    #('Tweet-Classifier/Data/train/travel',    'Travel'),
#('Tweet-Classifier/Data/train/technology',    'Technology')
]
SKIP_FILES = {'cmds'}
parentDir = os.path.dirname(os.path.dirname(os.getcwd()))

def read_files(path):
    path1 = os.path.join(parentDir, path)
    os.chdir(path1)  # changes the current dir to this
    #print('path1',path1)
    lines=[]
    for file in glob.glob('*.txt'):
        #print('file',file)
        f = open(file)
        for line in f:
            lines.append(line)
        f.close()
        content = NEWLINE.join(lines)
    #print('con',content)
    yield path1, content


def build_data_frame(path, classification):
    #print(path)
    #print('po')
    #print(read_files(path))
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

data = data.reindex(numpy.random.permutation(data.index))
count_vectorizer = CountVectorizer()
counts = count_vectorizer.fit_transform(data['text'].values)
classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)

#Testing
#Confidence matrix
I = pandas.Index(["Politics", "Sports", "Education", "Entertainment","Health","Nature","Startups"])
C = pandas.Index(["Politics", "Sports", "Education", "Entertainment","Health","Nature","Startups"])
confusion = pandas.DataFrame(0, index=I, columns=C)
#print(confusion)

counter1=0
counter2=0
for path, classification in SOURCES1:
    #print('class',classification)
    examples=[]
    text1=""
    #print('path',path)
    for file_name, text in read_files(path):
        text1+=text
    examples=text1.splitlines()
    #print('exam',examples)
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)
    #print(predictions)
    #print(predictions[0])
    for i in range(0,len(predictions)-1):
        if predictions[i]==classification:
            confusion[classification][classification]= confusion[classification][classification]+1
            counter1+=1
        else:
            confusion[classification][predictions[i]]=confusion[classification][predictions[i]]+1
            counter2+=1

print(confusion)
#print(counter1)
#print(counter2)
print('Accuracy is',(counter1/(counter1+counter2))*100)
#examples = [u'RT @MyStayAtHome: Quit spending!! 8 Tips On How To Not Spend Money This Month #money #spending #Finances - https://t.co/LViGWmGCx5 https://…', u"Investigators were in contact via cellphone with Facebook video murder suspect, Cleveland cops say… https://t.co/SoyeW4GYMQ"]
#example_counts = count_vectorizer.transform(examples)
#predictions = classifier.predict(example_counts)
#print(predictions)