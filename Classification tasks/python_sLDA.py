#!/usr/bin/python3

#%matplotlib inline
import re
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import seaborn as sns
#df = pd.read_csv("train_COMPLETE_CATEGORY.csv", encoding = "ISO-8859-1")
#df = pd.read_csv("train_TOP_CATEGORY.csv", encoding = "ISO-8859-1")
#df = pd.read_csv("train_AZd_CATEGORY.csv", encoding = "ISO-8859-1")
df = pd.read_csv("train_ALL_SAMPLE.csv", encoding = "ISO-8859-1")

ccs = [] 
for i in df['CCS']: 
    x = i.split()
    ccs.append(x)
    
df['CCS_new'] = ccs

# function to clean text (needs more refinement)
def clean_text(text):
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    text = re.sub("\'", "", text) 
    text = re.sub("[^a-zA-Z]"," ",text) 
    text = ' '.join(text.split()) 
    text = text.lower() 
    return text

df['text'] = df['text'].map(lambda com : clean_text(com))

# function to remove stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

df['text'] = df['text'].apply(lambda x: remove_stopwords(x))

import nltk
from nltk.stem import WordNetLemmatizer 

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(w) for w in text]  ##Notice the use of text.

df['text'].apply(lemmatize_text)


# Transform target variables
from sklearn.preprocessing import MultiLabelBinarizer
multilabel_binarizer = MultiLabelBinarizer()
multilabel_binarizer.fit(df['CCS_new'])
y = multilabel_binarizer.transform(df['CCS_new'])

# Convert text to features
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000)
xtrain, xval, ytrain, yval = train_test_split(df['text'], y, test_size=0.1, random_state=9)
xtrain_tfidf = tfidf_vectorizer.fit_transform(xtrain)
xval_tfidf = tfidf_vectorizer.transform(xval)

# build model
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
lr = LogisticRegression()
clf = OneVsRestClassifier(lr)
clf.fit(xtrain_tfidf, ytrain)

# make predictions for validation set
y_pred = clf.predict(xval_tfidf)
y_pred[3]
score = f1_score(yval, y_pred, average="micro")
print("F1 score: ", score)

def infer_tags(q):
    q = clean_text(q)
    q = remove_stopwords(q)
    q_vec = tfidf_vectorizer.transform([q])
    q_pred = clf.predict(q_vec)
    q_pred = multilabel_binarizer.inverse_transform(q_pred)
    return str(q_pred)[1:-1]

with open('myfile.txt') as f:
    test_paper = f.readline()

print("Predicted CCS: ", infer_tags(test_paper))

#for i in range(5): 
  #k = xval.sample(1).index[0] 
  #print("Paper: ", df['paper_ID'][k], "\nPredicted CCS: ", infer_tags(xval[k])), print("Actual CCS: ",df['CCS_new'][k], "\n")


