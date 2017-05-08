# ProfanityChecker

To run the application 

>>> python init.py profanity_en.txt data/negative_tweets.json False

data folder
- contains three json files

profanity_en.txt - list of obscene words to be flagged

init.py - main file

bloomfilter.py - bloom filter class and functions

profanitychecker.py - functions to parse text and use bloom filter

