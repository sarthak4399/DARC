import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import openpyxl

def inner(text):
    def extraction1(text):
        elements={
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', text),
            'hashes': re.findall(r'\b[0-9a-fA-F]{32,64}\b', text),
            'links': re.findall(r'\bhttps?://[^\s<>"]+|www\.[^\s<>"]+\.onion\b', text),
            'passwords': re.findall(r'\b(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}\b', text),
            'usernames': re.findall(r'\b[A-Za-z0-9._-]{3,}\b', text)
        }
        return elements

    t=TfidfVectorizer(stop_words='english')
    X=t.fit_transform(data['text'])
    y=data['category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn=KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)

    new_data=pd.read_excel('new_scraped_data2.xlsx')
    new_X=t.transform(new_data['text'])

    predictions=knn.predict(new_X)
    new_data['category']=predictions

    elements=new_data['text'].apply(extraction1)
    new_data=new_data.join(pd.json_normalize(elements))

    output_columns=['text', 'category', 'emails', 'hashes', 'links', 'passwords', 'usernames']
    new_data.to_excel('categorized_output_data2.xlsx', columns=output_columns, index=False)
    a=pd.read_excel("categorized_output_data2.xlsx")
    print(a.head())

df=pd.read_excel("dark_web_crawler_synthetic_data.xlsx")
print(df.head())

def outer(df):
    def extraction2(df):
        elements={
            'drugs': re.findall(r'\b[DrugsdrugsDRUGSdrugDrugDRUG]{5,100}\b', text),
            'porn': re.findall(r'\b[PornpornPORN]{5,100}\b', text),
            'weapons': re.findall(r'\b[WeaponsweaponsWEAPONSweaponWeaponWEAPON]{5,100}\b', text),
            'redroom': re.findall(r'\b[RedredRED]+[ ]+[RoomroomROOMroomsRoomsROOMS]{5,100}\b', text),
            'bitcoin_addresses': re.findall(r'\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-HJ-NP-Z0-9]{8,87})\b', text),
            'hacker_hiring': re.findall(r'\b[HackerhackerHACKER]+[ ]+[HiringhiringHIRING]{5,100}\b', text),
            'marketplace_urls': re.findall(r'\b(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.onion)\b', text)
        }
        return elements

    t=TfidfVectorizer(stop_words='english')
    X=t.fit_transform(data['text'])
    y=data['category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn=KNeighborsClassifier(n_neighbors=7)
    knn.fit(X_train, y_train)

    new_data=pd.read_excel('new_scraped_data1.xlsx')
    new_X=t.transform(new_data['text'])

    predictions=knn.predict(new_X)
    new_data['category']=predictions

    elements=new_data['text'].apply(extraction2)
    new_data=new_data.join(pd.json_normalize(elements))

    output_columns=['text','category', 'drugs', 'porn', 'weapons', 'redroom', 'bitcoin address', 'hacker hiring', 'market places url']
    text=new_data.to_excel('categorized_output_data1.xlsx', columns=output_columns, index=False)
    return text
outer(df)

