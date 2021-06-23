# file that combines get_dictionary.py and text_to_speech.py
# it looks up words and then turns them into sentences

# dependencies
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from playsound import playsound
from lib.config import staging
from lib.get_dictionary import Librarian
from lib.text_to_speech import Reader

class Sentence():
    def __init__(self, word, ENV, use_test_dir=False):
        self.word = word
        self.env = ENV
        self.use_test_dir = use_test_dir

        # get the word
        self.librar = Librarian(self.word, self.env, use_test_dir=self.use_test_dir)
        self.word_data_list = self.librar.data_list

        # set up/construct the sentace
        self.word_sentence = ""
        for my_dict in self.word_data_list:
            for meaning_dict in my_dict["meanings"]:
                self.word_sentence += f" As a {meaning_dict['part_of_speech']}, {my_dict['word']} means: {meaning_dict['definition']}."

                # add synonyms if they exist
                if meaning_dict["synonyms"] != False:
                    self.word_sentence += f" Some synonyms of {my_dict['word']} are:"
                    for synonym in meaning_dict["synonyms"]:
                        self.word_sentence += f" {synonym}"
                        if synonym != meaning_dict["synonyms"][-1]:
                            self.word_sentence += ","
                        else:
                            self.word_sentence += "."

                # add antonyms if they exist
                if meaning_dict["antonyms"] != False:
                    self.word_sentence += f" Some antonyms of {my_dict['word']} are:"
                    for antonym in meaning_dict["antonyms"]:
                        self.word_sentence += f" {antonym}"
                        if antonym != meaning_dict["antonyms"][-1]:
                            self.word_sentence += ","
                        else:
                            self.word_sentence += "."

                # add an example if it exists
                if meaning_dict["example"] != False:
                    self.word_sentence += f" In a sentence, you would say: {meaning_dict['example']}."

                self.word_sentence += f" Again, that word was {my_dict['word']}."

        # fix double '..' and white space
        self.word_sentence = self.word_sentence.strip().replace("  "," ").replace("..", ".")

        # play word 
        playsound(self.word_data_list[0]["mp3_path"])

        # play word_sentace
        reader = Reader(use_test_dir=self.use_test_dir)
        reader.parse_and_play(self.word_sentence)

        # remove any now un-needed mp3's
        self.librar.purge_all_mp3_files()


if __name__ == "__main__":
    sentence = Sentence("", staging)
