# importing necessary modules

import pandas as pd
import numpy as np
from math import log as lg
from tqdm import tqdm
import json


# import all the five lettered words and keeping them in a list 'words', total number is 'totalWordCount'

with open('5_words_La.txt') as f: lines = f.readlines()
words = [word[:-1] for word in lines]

totalWordCount = len(words)


# importing the iteration choices, twoBit for only Green Black, threeBit for Green, Black, Yellow
# choices are kept in 'choices' list

with open('threeBit.txt') as f: lines = f.readlines()
choices = [word[:-1] for word in lines]



# returns the number of words posible for green and black and yellow

def numberIter (green, yel, black):
    selected = 0
    black_list = list(black)
    green_list = list(green)
    yellow_list = list(yel)
    for word in words:
        temp = 0

        for i in black_list:
            if i in word: temp = 1
        for i in range(len(green_list)):
            if green_list[i].isalpha():
                if word.find(green_list[i])!= i: temp = 1
        for i in range(len(yellow_list)):
            if yellow_list[i].isalpha():
                
                if word.find(yellow_list[i]) in [i, -1]: temp = 1    
        if temp == 0: selected = selected+1
#     print(selected)
    return selected



# returns expected value for each iterations, not summation

def exval(x, y):
#     print(x/y)
    if(x):
        return (x/y)*lg((y/x), 2)
#         print(lg((y/x), 2))
    else: return 0




# returns the green, yellow, black combinations of a certain selected word

def greenYelBlack(intNum, testword):
    choice = choices[intNum]
    testletters = list(testword)
    green= ''
    black = ''
    yel = ''
    for i in range(5):
        if(int(choice[i])==2):
            green = green + testletters[i]
            black = black + '-'
            yel = yel + '-'
        elif(int(choice[i])==1):
            green = green + '-'
            black = black + '-'
            yel = yel + testletters[i]    
        else:
            green = green + '-'
            black = black + testletters[i]
            yel = yel + '-'
            
    return green, yel, black





# returns the cummiliative expected value from all the green, yellow, black combinations of a word

def expectedValue(subject):
    value = 0
    for i in range(243):
        [green, yel, black] = greenYelBlack(i, subject)
        smallval = exval(numberIter(green, yel, black), totalWordCount)
        value = value + smallval
#         print(smallval)
    return value



# all the words are tested and expected value are calculated, printed in a txt file and also put in a dictionary

dicty = {}
for word in tqdm(words):
    tempValue = expectedValue(word)
    dicty[word] = tempValue
    df=open('greenYelBlack_ExpectedValue.txt','a')
    df.write(word)
    df.write('\t')
    df.write(str(tempValue))
    df.write('\n')
    df.close()


# the dictionary is sorted in descending order of expected value

sortedDict = dict(sorted(dicty.items(), key=lambda x: x[1], reverse= True))



# printed in a json file 

with open("greenYelBlack_ExpectedValue.json", "w") as outfile:
    json.dump(sortedDict, outfile)


# printed in a csv file

sorted_df = pd.DataFrame.from_dict(sortedDict.items())
sorted_df.to_csv('greenYelBlack_ExpectedValue.csv')