# this file makes get requests too and then
# processes json from the dictionary api

# dependencies
import os, sys, requests

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from lib.config import staging

class Librarian():
    def __init__(self, word, ENV):
        self.word = word

        # URI for word look up
        self.word_URI = ENV["API_URI"].replace("<word>",self.word)

        # get res object
        self.res = requests.get(self.word_URI)

        # look up a word
        self.full_json_list = self.res.json()

        # did the api find the word?
        # TODO del me self.word_found = True if type(self.full_json_list) == list else False
        self.word_found = True if self.res.status_code == 200 else False 


        if self.word_found:
            # get all of the things i need from the 
            # list of json 
            pass
        else:
            # just default to a "word not found" thing 
            # or default to a less specific definition 
            # that I hard code
            pass

if __name__ == "__main__":
    librar_bad = Librarian("abed",staging)
    librar_good = Librarian("hello",staging)