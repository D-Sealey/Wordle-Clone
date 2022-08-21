'''Wordle clone with some extra features
uses SOWPODS (Scrabble official dictionary)'''

'''
TODO:
-implement letter list
-fix/complete words remaining
'''
import random
import re
import requests
from collections import Counter

#---Functions---
def create_wordlist():    
  'Made with SOWPODS'
  # import requests
  url='http://norvig.com/ngrams/sowpods.txt'
  r=requests.get(url)
  sowpods=r.text
  return sowpods.casefold().split('\n')
'---'

def word_count(word_list):
  '''Displays length of words and associated counts in word list'''
  counts=Counter([len(word) for word in word_list])
  # return counts
  for length,count in sorted(counts.items()):
    print(length,count)
'---'

def limit_words(word_list, L):
  '''Create list of L-length words'''
  words=[word for word in word_list if len(word)==L]
  return words
'---'

def pick_answer(word_list):
  '''Pick word from word list'''  
  return random.choice(word_list)
'---'

def make_guess(word_list,L):
  '''Ask user for guess and verify appropriate'''
  guess=input(f'Guess a {L}-letter word: ')
  while len(guess)!=L:
    print(f'Must be {L} letters')
    guess=make_guess(word_list,L)
  if guess not in word_list:
    print('Not in word list')
    guess=make_guess(word_list,L)
  return guess.lower() 
'---'

def check_guess(guess,answer):
  '''Compare guess to puzzle'''
  check=[]
  for position, letter in enumerate(guess):
    if letter in answer: 
      if letter==answer[position]:
        check.append(letter.upper())
      else:
        check.append(f"{letter}*")
    else:
      check.append('-')
  print(check)    
  return check
'---'

def words_remaining(word_list,L,guess,check):
  '''Build regex from guesses, check against potential words and return count of remaining words'''    
  answers=word_list

  '''['g*', 'r*', 'e*', '-', 'T']
['egret', 'greet']
  build regex with [^g] except g'''
  
  #---build sets of guessed letters in and not in word
  for pos, ele in enumerate(check):
    if ele == '-':        
      not_in.add(guess[pos])
    elif '*' in ele:
      contains.add(guess[pos])
    else:
      regex.pop(pos)
      regex.insert(pos,guess[pos])

  #-remove words
  for l in not_in:
    #-elimnated letters
    answers=[word for word in answers if word.count(l)==0]
  for l in contains:
    #-letter somewhere in word
    answers=[word for word in answers if l in word]

  #-run regex on list for exact letter placement
  #-regex only works on string so joined the answers list space separated
  # print(regex)
  test=' '.join(answers)
  exact=''.join(regex)
  answers=re.findall(exact,test)

  '''Turn on for list of remaining words'''
  # print(answers)
  return len(answers)
'---'
  
#---INITIALIZE---
all_words=create_wordlist()
# counts=word_count(all_words)
# L=input('Select word length: ')
L=5
potential_words=limit_words(all_words,L)
print(f'{len(potential_words)} potential {L}-letter words.')
#-fast enough to get len() again rather than pull from Counter

answer=pick_answer(potential_words)
# answer='coyly'
# answer='boozy'
# print(answer)
guess=''

#---make these global so they carry over after each call of words_remaining
not_in=set()
contains=set()
regex=[]
for i in range(L):
  regex.append('\w')

#---PLAY---
while True:
  guess=make_guess(potential_words,L)
  # guess='helps'
  if guess==answer:
    print(guess)
    break  
  print(guess)
  check=check_guess(guess,answer)
  num_remain=words_remaining(potential_words,L,guess,check)
  print(f'{num_remain} potential words remain.')
''

print('YOU WIN!')