#!/usr/bin/python3

import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

import nltk
nltk.download('wordnet')

from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

from nltk.corpus import stopwords
en_stop = stopwords.words('english')
en_stop.extend(['software', 'journal','study','engineering'])

import re
def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    tokens = [re.sub('^\d+', '', sent) for sent in tokens]          # numbers 
    tokens = [re.sub('^{\.|\-|\:}\d', '', sent) for sent in tokens] # decimal, negative numbers
    return tokens

import random
import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

text_data = []
path = sys.argv[1]

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        tokens = prepare_text_for_lda(line)
        if random.random() > .99:
            #print(tokens)
            text_data.append(tokens)

from gensim import corpora
dictionary = corpora.Dictionary(text_data)

corpus = [dictionary.doc2bow(text) for text in text_data]

import pickle
#pickle.dump(corpus, open('corpus.pkl', 'wb'))st
dictionary.save('dictionary.gensim')

import gensim
NUM_TOPICS = 10
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=25)
ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)
