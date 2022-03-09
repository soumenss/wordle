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

def possibleWordList(bigList, green, yel, black):
    '''
    The input is a big list, green, yel and black.
    Take a empty smallList and then check for each and every words
    in the biglist if they meet the conditions of green, yel, black.
    
    Words are appended in the smallList and the list is returned.
    '''
    black_list = list(black)
    green_list = list(green)
    yellow_list = list(yel)
    smallList= []
    for word in bigList:
        temp = 0
        for i in black_list:
            if i in word:
                temp = 1
                break
        if temp == 0:
            for i in range(len(green_list)):
                if word.find(green_list[i])!= i and green_list[i].isalpha():
                    temp = 1
                    break
        if temp == 0:
            for i in range(len(yellow_list)):
                if yellow_list[i].isalpha() and word.find(yellow_list[i]) in [i, -1]:
                    temp = 1
                    break
        
        if temp == 0: smallList.append(word)
    return smallList


def exvalfromProb(probability):
    if(probability): return (-1) * probability * lg(probability, 2)
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



def probabilityFromAllWords(suitableWordsList):
    prob_dict = json.load(open('unigram/unigram_freq_lata_sorted_sigmoid_prob.json'))
    allProbSum = 6486.499954602115 # sum(list(prob_dict.items()))
    
    selectedProbSum = 0
    for word in suitableWordsList:
        selectedProbSum = selectedProbSum + prob_dict[word]
    
    return selectedProbSum/allProbSum


# returns the cummiliative expected value from all the green, yellow, black combinations of a word

def expectedValue(subject, onWhomList):
    value = 0
    for i in range(243):
        [green, yel, black] = greenYelBlack(i, subject)
        smallval = exvalfromProb(probabilityFromAllWords(possibleWordList(onWhomList, green, yel, black)))
        value = value + smallval
    return value



# all the words are tested and expected value are calculated, printed in a txt file and also put in a dictionary

dicty = {}
for word in tqdm(words):
    tempValue = expectedValue(word, words)
    dicty[word] = tempValue
    df=open('greenYelBlack_ExpectedValue_La_sigmoid_prob.txt','a')
    df.write(word)
    df.write('\t')
    df.write(str(tempValue))
    df.write('\n')
    df.close()

# the dictionary is sorted in descending order of expected value

sortedDict = dict(sorted(dicty.items(), key=lambda x: x[1], reverse= True))

# printed in a json file 

with open("greenYelBlack_ExpectedValue_La_sigmoid_prob.json", "w") as outfile:
    json.dump(sortedDict, outfile)

# printed in a csv file

sorted_df = pd.DataFrame.from_dict(sortedDict.items())
sorted_df.to_csv('greenYelBlack_ExpectedValue_La_sigmoid_prob.csv')