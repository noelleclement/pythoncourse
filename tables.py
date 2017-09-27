"""
for i in range (10):    # forloop for the table of 1
    print (i + 1)
"""

#question = input ('Geef een tafel: ')

"""
for tableIndex in range (10):
    for multiplyIndex in range (10):
        print multiplyIndex+1 , ' x ' , tableIndex+1 , ' = ' , ((multiplyIndex+1)*(tableIndex+1))
    print ('')
"""

"""
####### VERSION 1 ######## 
#asks user how many tables they want to practice
#puts all those tables in array 
#loops through them in order and prints them
#user can answer 
#score is recorded and given after finishing all the tables


questionTable = []
score = 0
amountTables = int(input('How many tables to you want to practice?'))

for tableIndex in range (amountTables):
    for multiplyIndex in range (10):
        table = str(multiplyIndex+1) + ' x ' + str(tableIndex+1) + ' = '
        answer = (multiplyIndex+1)*(tableIndex+1)
        questionTable.append([table,answer])


for i in range (len(questionTable)):
    inputUser = int(input(questionTable[i][0]))
    if inputUser == questionTable[i][1]:
        print ('Correct!')
        score += 1
    else:
        print ('Incorrect...')

print ('Your score is: ', score)

"""





"""
####### VERSION 2 #######
#asks user how many tables they want to practice (not the full tables, but how many questions)
#puts all those tables in array (at the moment fe if <10 only table of 1)
#loops through them in random and prints them
#user can answer 
#score is recorded and given after finishing all the tables

from random import randint

questionTable = []
score = 0
amountTables = int(input('How many tables to you want to practice?'))

for tableIndex in range (amountTables):
    for multiplyIndex in range (10):
        table = str(multiplyIndex+1) + ' x ' + str(tableIndex+1) + ' = '
        answer = (multiplyIndex+1)*(tableIndex+1)
        questionTable.append([table,answer])

for i in range (amountTables):
    randomNumber = randint(0,amountTables)
    inputUser = int(input(questionTable[randomNumber][0]))
    if inputUser == questionTable[randomNumber][1]:
        print ('Correct!')
        score += 1
    else:
        print ('Incorrect...')

print ('Your score is: ', score)

"""




###### VERSION 3 ####### FINAL!!
#asks how many table user wants to practise
#asks what specific table user wants to practise (range)
#create random multiply and random table, and answer
#ask user for answer
#give feedback and if wrong save the user's answer
#give score and give option to see mistakes
#show mistakes

from random import randint


score = 0
amountTables = int(input('How many tables to you want to practice? '))
fromTables = int(input('What tables? From: '))
toTables = int(input('to: '))

mistakes = []

for i in range (amountTables):
    randMultiply = randint(1,10)
    randTable = randint(fromTables,toTables)
    question = str(randMultiply) + ' x ' + str(randTable) + ' = '
    answer = int(randMultiply*randTable)
    inputUser = int(input(question))
    if inputUser == answer:
        print ('Correct!')
        score += 1
    else:
        print ('Incorrect...')
        mistakes.append([question, answer, inputUser])

print ('Your score is: ', score, '/', amountTables)
if len(mistakes) > 0:
    inputMistakes = str(input('Do you want to know your mistakes? Y/N '))
    if inputMistakes == 'Y' or inputMistakes == 'y':
        for i in range (len(mistakes)):
            print('')
            print('Your answer: ', mistakes[i][0], mistakes[i][2])
            print('Correct answer: ', mistakes[i][0], mistakes[i][1])
            print('')
    else:
        print('Thanks for using my application!')
else:
    print('Thanks for using my application!')




