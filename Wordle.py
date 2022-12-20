'''Wordle clone with some extra features
uses SOWPODS (Scrabble official dictionary)'''
#pip install requests, colorama, 
'''
TODO:
-fix duplicate letters showing as possible when only one in word
'''
import random,re,requests,os
from collections import Counter
from string import ascii_lowercase
from colorama import Fore,Style

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
  if guess=='1':
    return guess
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
        check.append(f"*{letter}*")
    else:
      check.append('-')
  print(check)    
  return check
'---'
def words_remaining(word_list,L,guess,check):
  '''Build regex from guesses, check against potential words and return count of remaining words'''    
  answers=word_list

  '''
  yapok
  guessing happy -> -AP*p**y*
  need to handle duplicate p showing as possibility
  '''
  
  #---build sets of guessed letters in and not in word
  for pos, ele in enumerate(check):
    if ele == '-':        
      not_in.add(guess[pos])
    elif '*' in ele:
      contains.add(guess[pos])
      if regex[pos]=='\w':
        pattern=f'[^{guess[pos]} ]'
        regex.pop(pos)
        regex.insert(pos,pattern)
      else:
        regex[pos]=regex[pos][:2]+guess[pos]+regex[pos][2:]
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
def print_letters():
  '''Print letters to choose from'''
  letters=[ltr for ltr in ascii_lowercase]
  base=[ltr for ltr in ascii_lowercase]
  def first():
    for ltr in not_in:
      index=base.index(ltr)
      letters.pop(index)
      letters.insert(index,'-')
    for ltr in contains:
      index=base.index(ltr)
      letters.pop(index)
      letters.insert(index,f'*{ltr}*')
    for ltr in regex:
      if ltr.isalpha():
        index=base.index(ltr)
        letters.pop(index)
        letters.insert(index,ltr.upper())
    print(letters)
  ''
  for ltr in letters:
    if ltr in not_in:
      print('-',end=' ')
    elif ltr in regex:
      #-only exact matches
      if ltr.isalpha():
        print(Fore.GREEN+ltr.upper(),end=' ')
        print(Style.RESET_ALL,end='')
    elif ltr in contains:
      print(Fore.YELLOW+ltr.upper(),end=' ')
      print(Style.RESET_ALL,end='')
    else:
      print(ltr,end=' ')
  print()
'---'
def select_length():
  try:
    return int(input('Select word length: '))
  except:
    print('Must be number from 2 to 15')
    select_length()

#---INITIALIZE---
all_words=create_wordlist()
L=5

# enables other word lengths
choice=False
choice=True
if choice:
  word_count(all_words)
  L=select_length()

potential_words=limit_words(all_words,L)
print(f'{len(potential_words)} potential {L}-letter words.')
#-fast enough to get len() again rather than pull from Counter
# print(potential_words)
answer=pick_answer(potential_words)
# answer='woken'
# print(answer)
guess=''

#---make these global so they carry over after each call of words_remaining
not_in=set()
contains=set()
regex=[]
for i in range(L):
  regex.append('\w')

#---TEST---

#---PLAY---
def play():
  guess_history=[]
  check_history=[]
  while True:
    guess=make_guess(potential_words,L)
    if guess=='1':
      print(*list(zip(guess_history,check_history)),sep='\n')
      return False
    guess_history.append(guess)
    if guess==answer:
      print(*list(zip(guess_history,check_history)),sep='\n')
      return True
    #clear terminal
    os.system('cls')
    #print guesses and corresponding checks
    print(*list(zip(guess_history,check_history)),sep='\n')
    print(guess,end=', ')
    check=check_guess(guess,answer)
    check_history.append(check)
    num_remain=words_remaining(potential_words,L,guess,check)
    print(f'{num_remain} potential words remain.')
    print_letters()
  ...
outcome=play()

if outcome:
  print(f'The word is: {answer}')
  print('YOU WIN!')
else:
  print(f'The word is: {answer}')
  print('YOU LOST!')
