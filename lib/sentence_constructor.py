# file that combines get_dictionary.py and text_to_speech.py
# it looks up words and then turns them into sentances

# dependencies
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from lib.config import staging
from lib.get_dictionary import Librarian
from lib.text_to_speech import Reader

class Sentance():
    def __init__(self, word):
        self.word = word

        # get the word

        # convert to text

        # construct sentace

    def read_sentance(self):
        pass
