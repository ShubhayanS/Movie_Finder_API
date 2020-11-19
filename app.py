import os
from flask import Flask, render_template, request, session, redirect,flash,url_for
from werkzeug.utils import secure_filename

import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

import os
import tweepy as tw
import pandas as pd


app = Flask(__name__)

#arko
# CONSUMER_KEY="8D65ukpUwRS0QLzGqs1ItN2Q9"
# CONSUMER_SECRET="FyLdr5dmWGgB232DlfFHc83bS7VfsAm2rhfAB4STKmCJyyLgcF"
# ACCESS_TOKEN="1224975331552944129-oWGF5X7lnC2mfauwjTUlEGY1QRwyDW"
# ACCESS_TOKEN_SECRET="SahRawRQTxKSxX0b8L5sDeYCYG2Guh0mCsl0vVYpHVdEq"

#rounak
CONSUMER_KEY="3XlvwneYeiizWuJx2GxfJM0tn"
CONSUMER_SECRET="8QhxM6xYIHobqZTA9JLlBRbFFZoQIInQlG5JjbSMA5onF4auPm"
ACCESS_TOKEN="2200824096-Lnn8IM0rGgKUw0BaTAk01ITnOp3gv3an5iwgHcM"
ACCESS_TOKEN_SECRET="g0Dk9NDbtGuvyh2HqYudAauGm5ghWs9bZ62osYqkjv3O4"






#tweet search
auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

@app.route('/')
def home():
    return "Status : True"


@app.route('/tollywood/upcoming')
def tollywood_upcoming_movies():

    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=tamil|telugu'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')
    genre = soup.find_all('div',class_='style__StyledText-tgsgks-0 gSrwRF')
    likes =soup.find_all('div',class_='style__StyledText-tgsgks-0 fQmrOt')
    tolly ={}
    bed= 0
    for r,g,l in zip(results,genre,likes):
        tolly[bed]={}
        tolly[bed]['Movie']=r.text
        tolly[bed]['Genre']=g.text
        tolly[bed]['Likes']=l.text
        bed+=1
    upcome ={'Tamil&Telugu':tolly}
    return upcome






@app.route('/bollywood/upcoming')
def bollywood_upcoming_movies():
    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=hindi'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')
    genre = soup.find_all('div',class_='style__StyledText-tgsgks-0 gSrwRF')
    likes =soup.find_all('div',class_='style__StyledText-tgsgks-0 fQmrOt')
    tolly ={}
    bed= 0
    for r,g,l in zip(results,genre,likes):
        tolly[bed]={}
        tolly[bed]['Movie']=r.text
        tolly[bed]['Genre']=g.text
        tolly[bed]['Likes']=l.text
        bed+=1
    upcome ={'Bollywood':tolly}
    return upcome

@app.route('/hollywood/upcoming')
def hollywood_upcoming_movies():
    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=english'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')
    genre = soup.find_all('div',class_='style__StyledText-tgsgks-0 gSrwRF')
    likes =soup.find_all('div',class_='style__StyledText-tgsgks-0 fQmrOt')
    tolly ={}
    bed= 0
    for r,g,l in zip(results,genre,likes):
        tolly[bed]={}
        tolly[bed]['Movie']=r.text
        tolly[bed]['Genre']=g.text
        tolly[bed]['Likes']=l.text
        bed+=1
    upcome ={'hollywood':tolly}
    return upcome


@app.route('/tollywood/upcoming/tweets')
def tollywood_upcoming_tweets():
    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=tamil|telugu'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')

    tolly =[]
    for r in results:
        tolly.append(r.text)
        #print(r.text,end='\n')

    # Define the search term and the date_since date as variables
    users_locs =[]
    ted =0
    bd =0
    tollywood={}
    bollywood={}

    for k in tolly:
        t=[]
        k.lstrip()
        k.rstrip()
        j=k.encode("ascii","ignore")
        k=j.decode()
        search_words = k.replace(" ","+")
        new_search = search_words + " -filter:retweets"

        tweets = tw.Cursor(api.search,
                            q=new_search,
                            lang="en",tweet_mode="extended").items(10)

        #users_locs = [[tweet.user.screen_name, tweet.user.location,tweet.full_text] for tweet in tweets]
        for tweet in tweets:
            tollywood[ted]={}
            tollywood[ted]['MovieName']=k
            tollywood[ted]['TweetBy']=tweet.user.screen_name
            tollywood[ted]['TweetID']=tweet.user.id_str
            tollywood[ted]['TweetLocation']= tweet.user.location
            tollywood[ted]['Tweet']=tweet.full_text
            t= [search_words,tweet.user.screen_name, tweet.user.id_str,tweet.user.location,tweet.full_text]
            users_locs.append(t)
            ted+=1
    return tollywood

@app.route('/bollywood/upcoming/tweets')
def bollywood_upcoming_tweets():
    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=hindi'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')
    tolly =[]
    for r in results:
        tolly.append(r.text)
        #print(r.text,end='\n')

    # Define the search term and the date_since date as variables
    users_locs =[]
    ted =0
    bd =0
    tollywood={}
    bollywood={}

    for k in tolly:
        t=[]
        k.lstrip()
        k.rstrip()
        j=k.encode("ascii","ignore")
        k=j.decode()
        search_words = k.replace(" ","+")
        new_search = search_words + " -filter:retweets"

        tweets = tw.Cursor(api.search,
                            q=new_search,
                            lang="en",tweet_mode="extended").items(10)

        #users_locs = [[tweet.user.screen_name, tweet.user.location,tweet.full_text] for tweet in tweets]
        for tweet in tweets:
            tollywood[ted]={}
            tollywood[ted]['MovieName']=k
            tollywood[ted]['TweetBy']=tweet.user.screen_name
            tollywood[ted]['TweetID']=tweet.user.id_str
            tollywood[ted]['TweetLocation']= tweet.user.location
            tollywood[ted]['Tweet']=tweet.full_text
            t= [search_words,tweet.user.screen_name, tweet.user.id_str,tweet.user.location,tweet.full_text]
            users_locs.append(t)
            ted+=1           
    return tollywood

@app.route('/hollywood/upcoming/tweets')
def hollywood_upcoming_tweets():
    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=english'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')
    tolly =[]
    for r in results:
        tolly.append(r.text)
        #print(r.text,end='\n')

    # Define the search term and the date_since date as variables
    users_locs =[]
    ted =0
    bd =0
    tollywood={}
    bollywood={}

    for k in tolly:
        t=[]
        k.lstrip()
        k.rstrip()
        j=k.encode("ascii","ignore")
        k=j.decode()
        search_words = k.replace(" ","+")
        new_search = search_words + " -filter:retweets"

        tweets = tw.Cursor(api.search,
                            q=new_search,
                            lang="en",tweet_mode="extended").items(10)

        #users_locs = [[tweet.user.screen_name, tweet.user.location,tweet.full_text] for tweet in tweets]
        for tweet in tweets:
            tollywood[ted]={}
            tollywood[ted]['MovieName']=k
            tollywood[ted]['TweetBy']=tweet.user.screen_name
            tollywood[ted]['TweetID']=tweet.user.id_str
            tollywood[ted]['TweetLocation']= tweet.user.location
            tollywood[ted]['Tweet']=tweet.full_text
            t= [search_words,tweet.user.screen_name, tweet.user.id_str,tweet.user.location,tweet.full_text]
            users_locs.append(t)
            ted+=1           
    return tollywood



# app name 
@app.errorhandler(404)  
def not_found(e):  
  return "Not Defined" 

  
if __name__ == '__main__':
    app.run(debug=True)