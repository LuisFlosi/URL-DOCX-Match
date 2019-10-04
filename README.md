# URL-DOCX-Match

Matches URL and DOCX main words, showing word count per docx document against the main URL

###############################################

The following functions have been defined:

splitContent(content) -> returns a list of words in lower case
cleanWordList(wordlist) -> removes unnecessary symbols and common english words from the word list
cleanDOCX(path) -> loads, splits and cleans words from all docs in the provided path
cleanURL(url) -> scrapes URL for important words and adds them to a list, then cleans the list
dataFrameDic(dic) -> creates a dataframe including every unique word from all documents and URL and a count of each word for each document/URL

###############################################

This has only been tested with a limited number of websites, and certain modifications may be necessary in order to scrape other sites.

###############################################

I have used a few sources to help me build parts of the code. The sources are the following:
  
https://stackoverflow.com/questions/47922302/reading-multiple-docx-files-in-python-in-one-variable
https://stackoverflow.com/questions/55718448/how-do-i-get-docx2txt-to-process-all-docx-files-in-directory
https://www.geeksforgeeks.org/python-program-crawl-web-page-get-frequent-words/
https://stackoverflow.com/questions/13323851/python-3-counting-matches-in-two-lists-including-duplicates
https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
