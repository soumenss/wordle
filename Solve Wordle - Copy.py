# importing necessary modules

from math import log as lg
from tqdm import tqdm


doneUpto = 'ninja'




# returns the smaller list which are the potential answer according to green, yel, blue

def getSmallList(bigList, green, yel, black):
    '''
    The input is a big list, green, yel and black.
    Take a empty smallList and then check for each and every words
    in the biglist if they meet the conditions of green, yel, black.
    
    Words are appended in the smallList and returned.
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



with open('5_words_La.txt') as f: lines = f.readlines()
words = [word[:-1] for word in lines]


# importing the iteration choices, twoBit for only Green Black, threeBit for Green, Black, Yellow
# choices are kept in 'choices' list

with open('threeBit.txt') as f: lines = f.readlines()
choices = [word[:-1] for word in lines]



def sortedExpectedValue(onWhomList, testingList):
    '''
    The testing list is the list of which the entropy will be measured.
    The onWhomList is the list on whom the entropy will be measurred. 
    The testing list will be typically larger of equal to the onWhomList.
    As the iterations will go on. The onWhomList will exponentially reduce.
    
    It will return a dictionary of which the index will be items from testingList
    and the value of that item will be entropy of the item on the onWhomList.
    
    
    '''
    
    dicty = {}
    
    # for word in tqdm(testingList):

    for word in testingList:
        tempValue = expectedValue(word, onWhomList)
        dicty[word] = tempValue
    
    sortedDict = dict(sorted(dicty.items(), key=lambda x: x[1], reverse= True))
    return sortedDict


# returns the cummiliative expected value from all the green, yellow, black combinations of a word

def expectedValue(subject, onWhomList):
    value = 0
    for i in range(243):
        [green, yel, black] = greenYelBlack(i, subject)
        smallval = exval(possibleWordNumber(onWhomList, green, yel, black), len(onWhomList))
        value = value + smallval
    
    return value



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



# returns expected value for each iterations, not summation

def exval(x, y):
    if(x): return (x/y)*lg((y/x), 2)
    else: return 0
    
def bitInformation(x, y):
    if(x): return lg((y/x), 2)
    else: return 0


# returns the number of words posible for green and black and yellow

def possibleWordNumber(bigList, green, yel, black):
    '''
    The input is a big list, green, yel and black.
    Take a empty smallList and then check for each and every words
    in the biglist if they meet the conditions of green, yel, black.
    
    Words are appended in the smallList and the length is returned.
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
    return len(smallList)



def checkWordle(guess, real):
    gList = list(guess)
    rList = list(real)
    
    colPal = ''
    letterCount = 0
    for gLetter in gList:
        if gLetter not in rList: colPal = colPal + 'B'
        else:
            if real.find(gLetter)== letterCount: colPal = colPal + 'G'
            else: colPal = colPal + 'Y'
        letterCount = letterCount + 1
        
    return colPal




def GYBfromColPal(guess, colPal):
    green = ''
    yel = ''
    black = ''
    
    gList = list(guess)
    colList = list(colPal)
    
    if len(gList)!= len(colList): print('The length is not same!!')
        
    else:
        for i in range(len(gList)):
            if colList[i] == 'B':
                black = black + gList[i]
                yel = yel + '-'
                green = green + '-'
            elif colList[i] == 'Y':
                black = black + '-'
                yel = yel + gList[i]
                green = green + '-'
            elif colList[i] == 'G':
                black = black + '-'
                yel = yel + '-'
                green = green + gList[i]
        return green, yel, black




def GYBfromGuessReal(guess, real):
    gList = list(guess)
    rList = list(real)
    
    green = ''
    yel = ''
    black = ''
    letterCount = 0
    
    for gLetter in gList:
        if gLetter not in rList:
            black = black + gLetter
            yel = yel + '-'
            green = green + '-'
        else:
            if real.find(gLetter)== letterCount:
                black = black + '-'
                yel = yel + '-'
                green = green + gLetter
            else:
                black = black + '-'
                yel = yel + gLetter
                green = green + '-'
                
        letterCount = letterCount + 1
        
    return green, yel, black



with open('5_words_La.txt') as f: lines = f.readlines()
puzzles = [word[:-1] for word in lines]
# puzzles = ['shirt', 'score', 'party', 'touch', 'south', 'extra', 'grade', 'whole', 'sheet', 'knoll']
# puzzles = puzzles[5:300]
# puzzles = ['knoll', 'shirt', 'india']
doneUptoIndex = puzzles.index(doneUpto)
puzzles = puzzles[doneUptoIndex+1:]




puzzleCount = 0
Score = 0

for real in puzzles:
    df=open('Wordle All Words Small Dataset.txt','a')

    df.write(real)
    df.write('\t')

    guess = 'tares'
    guesses = ['tares']

    df.write(guess)
    df.write('\t')

    [green, yel, black] = GYBfromGuessReal(guess, real)
    small = getSmallList(words, green, yel, black)
    newdict = sortedExpectedValue(small, words)

    stepCount = 1

    while(guess!=real):
        guess = list(newdict.keys())[0]
        guesses.append(guess)

        df.write(guess)
        df.write('\t')

        [green, yel, black] = GYBfromGuessReal(guess, real)
        prevSmall = small
        small = getSmallList(prevSmall, green, yel, black)
        newdict = sortedExpectedValue(small, prevSmall)
        stepCount = stepCount + 1
        if stepCount == 7:
            stepCount = 0
            puzzleCount = puzzleCount - 1
            break
        
    puzzleCount = puzzleCount + 1
    Score = Score + stepCount
    AvgScore = Score/puzzleCount
    
    print(real, stepCount, guesses, AvgScore)

    
    
    df.write(str(stepCount))
    df.write('\t')
    df.write(str(AvgScore))
    df.write('\n')
    df.close()