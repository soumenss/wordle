import pandas as pd 

with open('5_words_La.txt') as f: lines = f.readlines()
words = [word[:-1] for word in lines]