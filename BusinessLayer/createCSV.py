import os
import csv
from getTweets import clearRepository

#paths to the training data folder and CSV data folder
trainPath = os.path.join(os.path.dirname(os.getcwd()), 'Data\\train')
csvPath = os.path.join(os.path.dirname(os.getcwd()), 'Data\\CSV')

#clear the CSV data folder before populating again
clearRepository(csvPath)

#function to populate tweets into folder-wise CSV files
#input: path to the training data folder
#returns: none
for dir in os.listdir(trainPath):
    with open(os.path.join(csvPath, dir + '.csv'), 'a') as fd:
        wr = csv.writer(fd, dialect='excel')
        for fname in os.listdir(os.path.join(trainPath, dir)):
            with open(os.path.join(os.path.join(trainPath, dir), fname), 'r') as f:
                wr.writerow(f.readlines())
    fd.close()