#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:41:12 2019

@author: swetu
"""

# Fecthing all the tweets

import tweepy
import re
import pickle

from tweepy import OAuthHandler

#initialising the keys the keys that are going to authaticate the clients
consumer_key = 'cmWaWls1utx3mBZw0etljBqMG' 
consumer_secret = 'gw73OFZH0xEgunkqqjYwFqtX1epxaYTeyuE9gkil1aXrVyPrkM'
access_token = '1101076260619411457-jV1c65bhNDMZgJryJRbSj5aeNrr005' 
access_secret = '6ckRPAn8Oqoi1HeIIFug85pPblZRQM1MVuaa7zi5P6N8n'


auth = OAuthHandler(consumer_key,consumer_secret)

auth.set_access_token(access_token,access_secret)

args = ['facebook']
api = tweepy.API(auth,timeout=10)


list_tweets = []
query = args[0]
if len(args) ==1:
    for status in tweepy.Cursor(api.search,q=query+"-filter:retweets",lang = 'en',result_type = 'recent').items(100):
        list_tweets.append(status.text)
# Loading TF-IDF Vectorizer
with open('tfidfmodel.pickle','rb') as f:
    vectorizer = pickle.load(f)

with open('classifier.pickle','rb') as f:
    clf = pickle.load(f)

total_pos = 0
total_neg = 0

for tweet in list_tweets: 
    tweet = re.sub(r"^http://t.co/[a-zA-Z0-9]*\s"," ",tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s"," ",tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$"," ",tweet)
    tweet = tweet.lower()
    tweet = re.sub(r"that's,","that is",tweet)
    tweet = re.sub(r"there's","there is",tweet)
    tweet = re.sub(r"what's","what is",tweet)
    tweet = re.sub(r"where's","where is",tweet)
    tweet = re.sub(r"it's","it is",tweet)
    tweet = re.sub(r"who's","who is",tweet)
    tweet = re.sub(r"she's","she is",tweet)
    tweet = re.sub(r"he's","he is",tweet)
    tweet = re.sub(r"i'm","i am",tweet)
    tweet = re.sub(r"they're","they are",tweet)
    tweet = re.sub(r"ain't","am not",tweet)
    tweet = re.sub(r"wouldn't","would not",tweet)
    tweet = re.sub(r"shouldn't","should not",tweet)
    tweet = re.sub(r"can't","can not",tweet)
    tweet = re.sub(r"couldn't","could not",tweet)
    tweet = re.sub(r"\W"," ",tweet)
    tweet = re.sub(r"\d"," ",tweet)
    tweet = re.sub(r"s+[a-z]\s+"," ",tweet)
    tweet = re.sub(r"s+[a-z]$"," ",tweet)
    tweet = re.sub(r"^[a-z]\s+"," ",tweet)
    tweet = re.sub(r"\s+"," ",tweet)
   
    # predicting sentiments of tweets
    sent = clf.predict(vectorizer.transform([tweet]).toarray()) 
    print(tweet,":",sent)
    if sent[0] == 1:
        total_pos +=1
    else:
        total_neg +=1
        
#plotting the bar chart

import matplotlib.pyplot as plt
import numpy as np
objects = ['positive','negative']
y_pos = np.arange(len(objects))

plt.bar(y_pos,[total_pos,total_neg],alpha = 0.5)
plt.xticks(y_pos,objects)
plt.ylabel('Number')
plt.title('Number of positive and negative tweets')
plt.show()
       
            
                
