
import csv
import pandas
import gensim

# read WhenInManila crawled data in csv format
csv.file_name = '../../Data Set/when_in_manila/364824_1_csv.csv'
csv.file = pandas.read_csv(csv.file_name, error_bad_lines=False) #ignore erroneous lines

len(csv.file) #9,729 blogs
#headers: url, dateCrawled, text, errors

text = csv.file['text']
urls = csv.file['url']


from text_processor import  LabeledLineSentence

x = LabeledLineSentence.LabeledLineSentence(doc_list=text, labels_list=urls)

model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate

model.build_vocab(x)

for epoch in range(10):
    model.train(x)
    model.alpha -= 0.002 # decrease the learning rate
    model.min_alpha = model.alpha # fix the learning rate, no decay
    model.train(x)

#oersist model to external file

model.docvecs[urls[600]]

ftrs = list(model.docvecs)
idx = 600
print urls[idx]
model.docvecs.most_similar(urls[idx])
model.most_similar('mouse')

#run k-means algorithm to the ftrs extracted

import sklearn
from sklearn.cluster import KMeans

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


