import requests
from bs4 import BeautifulSoup

import os
import tweepy as tw
import pandas as pd
import time

#arko
CONSUMER_KEY="8D65ukpUwRS0QLzGqs1ItN2Q9"
CONSUMER_SECRET="FyLdr5dmWGgB232DlfFHc83bS7VfsAm2rhfAB4STKmCJyyLgcF"
ACCESS_TOKEN="1224975331552944129-oWGF5X7lnC2mfauwjTUlEGY1QRwyDW"
ACCESS_TOKEN_SECRET="SahRawRQTxKSxX0b8L5sDeYCYG2Guh0mCsl0vVYpHVdEq"

#rounak
# CONSUMER_KEY="3XlvwneYeiizWuJx2GxfJM0tn"
# CONSUMER_SECRET="8QhxM6xYIHobqZTA9JLlBRbFFZoQIInQlG5JjbSMA5onF4auPm"
# ACCESS_TOKEN="2200824096-Lnn8IM0rGgKUw0BaTAk01ITnOp3gv3an5iwgHcM"
# ACCESS_TOKEN_SECRET="g0Dk9NDbtGuvyh2HqYudAauGm5ghWs9bZ62osYqkjv3O4"

while (True):
    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=tamil|telugu'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')

    tolly =[]
    for r in results:
        tolly.append(r.text)
        #print(r.text,end='\n')


    bolly =[]
    URL = 'https://in.bookmyshow.com/explore/upcoming-movies-chennai?languages=hindi'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    results = soup.find_all('div',class_='style__StyledText-tgsgks-0 gbzvvd')

    print("##################################")
    for r in results:
        bolly.append(r.text)
        #print(r.text,end='\n')


    print("Tollywood -",tolly ,'\n')
    print("Bollywood -",bolly,'\n')
    #print(results.prettify())

    #tweet search
    auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    users_locs =[]
    ted =0
    bd =0
    tollywood={}
    bollywood={}

    def find(search_words):
        t=[]
        search_words = search_words
        new_search = search_words + " -filter:retweets"

        tweets = tw.Cursor(api.search,
                            q=new_search,
                            lang="en",tweet_mode="extended").items(10)

        #users_locs = [[tweet.user.screen_name, tweet.user.location,tweet.full_text] for tweet in tweets]
        for tweet in tweets:
            t= [search_words,tweet.user.screen_name,tweet.user.id_str, tweet.user.location,tweet.full_text]
            users_locs.append(t)
        # tollywood['SouthIndian_Movies']=users_locs
        
    
    for i in tolly:
        i.lstrip()
        i.rstrip()
        j=i.encode("ascii","ignore")
        i=j.decode()
        find(i.replace(" ","+"))

    for i in bolly:
        i.lstrip()
        i.rstrip()
        j=i.encode("ascii","ignore")
        i=j.decode()
        find(i.replace(" ","+"))

    # print(users_locs)
    tweet_text = pd.DataFrame(data=users_locs,columns=['search_word','username', "userid","location",'tweet'])
    print(tweet_text)
    print('##############################')
    # print(tollywood)

    try:
        tweet_text.to_csv (r'movie_dump.csv',mode='a', index = False, header=False)
        print("Fetching Done....")
    except:
        print("Couldn't Fetch....")
    
    time.sleep(10800)

