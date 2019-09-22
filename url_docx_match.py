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

# Welcome message
print('Welcome to resume match!')
print('We currently only accept .docx resumes')

# Insert URL and resume fodler's path
url_input = input('Enter job URL:')
folder_path = input("Enter resume folder's path:")

# Prepare path to include all .docx in folder
files_path = folder_path + '/*.docx'

symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/., '
common_words = ['is','a','the','for', 'an']

# Function to clean file
def cleanContent(content):
    words = content
    # Define delimiters to erase from file
    delimiters = ['\n', ' ', ',', '.', '?', '!', ':']
    # Clean content
    for delimiter in delimiters:
        new_words = []
        for word in words:
            new_words += word.lower().split(delimiter)
        words = new_words
    return(words)

def cleanWordList(wordlist): 
    clean_list =[] 
    for word in wordlist: 
        word.lower()
        for i in range (0, len(symbols)): 
            word = word.replace(symbols[i], '')
        for j in range (0, len(common_words)):
            word = word.replace(common_words[i], '')
        if len(word) > 0: 
            clean_list.append(word)
    return clean_list

# Initiate dictionary to store files
files = {}

# Load all .docx into dictionary
def cleanDOCX(path):
    for file in glob.glob(path):
        # Get file name
        file_name = file.split("\\",1)[-1]
        # Get file content
        raw_content = docx2txt.process(file)
        # Clean content
        word_list = cleanContent(raw_content)
        clean_file = cleanWordList(word_list)
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
    for each_text in soup.findAll('div', {'class':'entry-content'}): 
        content = each_text.text 
        # use split() to break the sentence into  
        # words and convert them into lowercase  
        words = content.lower().split() 
        for each_word in words: 
            url_wordlist.append(each_word)
    cleanWordList(url_wordlist)        
    files[url] =  url_wordlist

def dataFrame(dic):
    word_count_df = {}
    for k,v in dic:
        word_count = {}
        names = []
        for i in v:
            word_count[i] = list(v.count(i))
        for j,c in word_count:
            names = names + list(k)
            word_count_df[j] = word_count_df[j] + c
    inverted_word_df = pandas.DataFrame(word_count_df)
    word_df = inverted_word_df.T
    word_df.columns = names

cleanDOCX(folder_path)
cleanURL(url_input)
df = dataFrame(files)
print(pandas.DataFrame.head(df))








