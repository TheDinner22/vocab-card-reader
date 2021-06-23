# the main file

# dependencies
import os, sys, time, random

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from test.main_test import _App
from lib.sentence_constructor import Sentence
from lib.config import production

def get_and_play_a_random_word(words, sent, env):
    """randomly select a word and play its definition out loud"""
    random_num = random.randint(0,len(words)-1)
    word = words[random_num]
    sent(word, env)

print ("Type 'help' for help")

flag = True
words_list = production["WORDS_LIST"]
while flag:
    user_cmd = input("$").lower().strip()
    if user_cmd == "kill" or user_cmd == "quit" or user_cmd == "q":
        flag = False
        break
    elif user_cmd == "man" or user_cmd == "help" or user_cmd == "manual":
        print("---------------------------------------------------------")
        print('"help", "man", or "manual" - to see the help menu')
        print('"test" - to run all tests')
        print('"run" - to run the vocab reader')
        print("---------------------------------------------------------")
    elif user_cmd == "test":
        tester = _App()
        tester.run_all_tests()
    elif user_cmd == 'run':
        flag = False

        # get the time between words
        while True:
            user_time = input("How many minutes would you like me to wait before saying the next word?: ")
            try:
                user_time = int(user_time)
                if user_time >= 1:
                    real_time = user_time * 60
                    break
            except Exception as _e:
                continue



        # run for eternity
        while True:
            get_and_play_a_random_word(words_list, Sentence, production)
            time.sleep(real_time)
