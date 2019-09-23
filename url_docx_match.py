# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 12:07:24 2019

@author: Luis Flosi
"""

# Import libraries
import docx2txt
import glob
import requests
import pandas
from bs4 import BeautifulSoup
import re

# Welcome message
print('Welcome to resume match!')
print('We currently only accept .docx resumes')

# Insert URL and resume fodler's path
url_input = input('Enter job URL:')
folder_path = input("Enter resume folder's path:")

# Prepare path to include all .docx in folder
files_path = folder_path + '/*.docx'

symbols = "!@#$%^&*()_-+={[}]|\;:'<>?/., "
common_words = ['also', 'have', 'other', 'such', 'all', 'using', 'will', 'from', 'or','is','a','the','for', 'an', 'as', 'of', 'to', 'at', 'with', 'in', 'on', 'that', 'and', 'into', 'by', 'us', 'we', 'you', 'you', 'are', "isn't", ]
delimiters_re = '; |, |\*|\n|\\t|\b|\| |\s|/|-'
    
# Function to clean file
def splitContent(content):
    words = content.lower()
    # Split content
    new_words = re.split(delimiters_re, words)
    for word in new_words:
        word = word.split
    words = list(filter(None, new_words))
    return(words)

def cleanWordList(wordlist): 
    clean_list =[] 
    for word in wordlist:
        for letter in word:
            if letter in symbols:
                word = word.replace(letter, "")
        if (len(word) > 0 and word not in common_words): 
            clean_list.append(word)
    return clean_list

# Initiate dictionary to store files
files = {}

# Load all .docx into dictionary
def cleanDOCX(path):
    path = path + '\\*.docx'
    path = path.replace('\\', '/')
    for file in glob.glob(path):
        # Get file content
        raw_content = docx2txt.process(file)
        # Clean content
        word_list = splitContent(raw_content)
        clean_file = cleanWordList(word_list)
        # Get file name
        file_name = file.replace('\\', '/').rsplit('/', 1)[-1]
        # Add name and content to dictionary
        files[file_name] = clean_file

def cleanURL(url): 
    # empty list to store the contents of  
    # the website fetched from our web-crawler 
    url_wordlist = [] 
    source_code = requests.get(url).text 
    # BeautifulSoup object which will 
    # ping the requested url for data 
    soup = BeautifulSoup(source_code, 'html.parser') 
    # Text in given web-page is stored under 
    # the <div> tags with class <entry-content>
    for each_text in soup.findAll('div', {'id':'content'}): 
        content = each_text.text
        # use split() to break the sentence into  
        # words and convert them into lowercase  
        words = splitContent(content)
        for each_word in words:
            each_word.lower()
            if each_word not in common_words:
                url_wordlist.append(each_word)
    url_wordlist = cleanWordList(url_wordlist)
    files[url] =  url_wordlist

def dataFrameDic(dic):
    word_count_list = {}
    names = []
    for s,w in dic.items():
        for word in w:
            if word in word_count_list:
                continue
            else:
                word_count_list[word] = []
    for source,words in dic.items():
        word_count = {}
        for word in words:
            if word in word_count: 
                continue
            else:
                count_list = []
                count_list.insert(0,words.count(word))            
                word_count[word] = count_list
        for k, v in word_count_list.items():
            if k in word_count:
                word_count_list[k] += word_count[k]
            else:
                word_count_list[k] += [0]
        names.append(source)
    inverted_word_df = pandas.DataFrame(word_count_list)
    word_df = inverted_word_df.T
    word_df.columns = names
    word_df["sum"] = word_df.sum(axis = 1)
    word_df = word_df.sort_values("sum", ascending=False)
    return word_df
    
cleanDOCX(folder_path)
cleanURL(url_input)
df = dataFrameDic(files)
try:
    df.to_csv(r'answer.csv')
    print("Successfully created csv fille")
except:
    print("Error writing file")






