# this file makes get requests too and then
# processes json from the dictionary api

# dependencies
import os, sys, requests

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from lib.config import staging
from lib.backup_dict import hard_code_dict
from lib.text_to_speech import Reader

class Librarian():
    def __init__(self, word, ENV, use_test_dir=False):
        self.word = word
        self.use_test_dir = use_test_dir
        self.data_list = []
        self.base_dir = "data/sounds/" if not self.use_test_dir else "data/test/" 

        # URI for word look up
        self.word_URI = ENV["API_URI"].replace("<word>",self.word)

        # get res object/look up the word
        self.res = requests.get(self.word_URI)

        # get the json from the response
        self.full_json_list = self.res.json()

        # did the api find the word?
        self.word_found = True if self.res.status_code == 200 else False 

        if self.word_found:
            # get all of the things i need from the 
            # list of json
            for api_word_dict in self.full_json_list:
                my_word_dict = {}

                # things i want from each dict:

                
                # the word
                my_word_dict["word"] = api_word_dict['word']

                # mp3 of word being pronounced
                try:
                    link_for_mp3 = api_word_dict["phonetics"][0]["audio"]
                except Exception as _e:
                    link_for_mp3 = ""
                if link_for_mp3 != "":
                    res = requests.get(link_for_mp3)
                    if res.status_code == 200:
                        # write binary to a file in data/sounds
                        filename = my_word_dict["word"] + '.mp3'
                        file_path = self.base_dir + filename
                        with open(file_path, "wb+") as file_object:
                            file_object.write(res.content)
                            my_word_dict["mp3_path"] = file_path
                    else:
                        my_word_dict["mp3_path"] = False    
                else:
                    my_word_dict["mp3_path"] = False

                # NOTE the rest of these are in the meanings key, 
                # this means that there can be several of these in one api_word_dict 
                # which keep in mind we are looping through several of
                
                meanings = []

                for their_obj in api_word_dict["meanings"]:
                    my_dict = {}

                    # part of speech # key in dict in meanings list
                    try:
                        my_dict["part_of_speech"] = their_obj["partOfSpeech"]
                    except Exception as _e:
                        my_dict["part_of_speech"] = False

                    # definition
                    try:
                        my_dict["definition"] = their_obj["definitions"][0]["definition"]
                    except Exception as _e:
                        my_dict["definition"] = False

                    # first 4 synonyms of the word (if they exist)
                    try:
                        synonyms_list = their_obj["definitions"][0]["synonyms"]
                        final_index = 4 if len(synonyms_list) >= 4 else len(synonyms_list)
                        my_dict["synonyms"] = synonyms_list[0:final_index]
                    except Exception as _e:
                        my_dict["synonyms"] = False


                    # first 4 antonyms of the word (if they exist)
                    try:
                        antonyms_list = their_obj["definitions"][0]["antonyms"]
                        final_index = 4 if len(antonyms_list) >= 4 else len(antonyms_list)
                        my_dict["antonyms"] = antonyms_list[0:final_index]
                    except Exception as _e:
                        my_dict["antonyms"] = False

                    # word used in sentance (example param)
                    try:
                        my_dict["example"] = their_obj["definitions"][0]["example"] if type(their_obj["definitions"][0]["example"]) == str and their_obj["definitions"][0]["example"] != "" else False
                    except Exception as _e:
                        my_dict["example"] = False

                    meanings.append(my_dict)

                # add the meanings dict-list to data-list
                my_word_dict["meanings"] = meanings if meanings != [] else False

                # make sure the api supplied us with the following:

                word_is_ok = True

                # a word
                if type(my_word_dict["word"]) != str or my_word_dict["word"] == '':
                    word_is_ok = False
                
                # a definition
                elif my_word_dict["meanings"] == False:
                    word_is_ok = False

                elif word_is_ok:
                    for meaning_dict in my_word_dict["meanings"]:
                        if "definition" in meaning_dict:
                            if type(meaning_dict["definition"]) == str and meaning_dict["definition"] != "":
                                word_is_ok = True
                                break
                            else:
                                word_is_ok = False
                        else:
                            word_is_ok = False

                # at least one part of speech
                elif word_is_ok:
                    for meaning_dict in my_word_dict["meanings"]:
                        if "part_of_speech" in meaning_dict:
                            if type(meaning_dict["part_of_speech"]) == str and meaning_dict["part_of_speech"] != "":
                                word_is_ok = True
                                break
                            else:
                                word_is_ok = False
                        else:
                            word_is_ok = False
                    
                # NOTE im not adding this but ill leave it here as an idea for the future
                # synonyms or antonyms or an example of the word being used

                if word_is_ok:
                    # add the my_word_dict to data_list
                    self.data_list.append(my_word_dict)
                else:
                    self.hard_coded_definitions()
                    break
        else:
            if not self.use_test_dir:
                print(f'word: {self.word} was not found')
            self.hard_coded_definitions()

        # if the mp3 was not created, make it now using text to speech
        self.confirm_mp3_path()
    
    def hard_coded_definitions(self):
        """get the words definition from a txt file"""
        # TODO del me print('i ran ++++++++++')
        # re-set self.data list
        self.data_list = []
        # loop through each word until we find our word
        for definition_list in hard_code_dict:
            for word_dict in definition_list:
                if word_dict["word"] == self.word:
                    self.data_list = definition_list
                if self.data_list != []:
                    break
            if self.data_list != []:
                break
                    
    def confirm_mp3_path(self):
        mp3_path = self.data_list[0]["mp3_path"]

        if not os.path.exists(mp3_path):
            # here we are going to use tts to make the mp3 path exist 
            #TODO make unit tests for this file

            # make a new data_list to store and then save the new dictionaries
            new_data_list = []

            # init the reader, change its base dir to this classes base dir
            reader = Reader()
            reader.base_dir = self.base_dir

            # save the word as an mp3 for each dict in data list
            for data_dict in self.data_list:
                # get the word and create filename and file_path
                word = data_dict["word"]
                filename = (word.replace(" ","_")) + ".mp3"
                file_path = self.base_dir + filename

                # create the file
                reader.text_to_speech(word)

                # update and save the dictionary
                data_dict['mp3_path'] = file_path
                new_data_list.append(data_dict)


            # update the data list with the new dictionaries
            self.data_list = new_data_list

    def purge_all_mp3_files(self):
        """remove all files from self.base_dir"""
        all_files = os.listdir(self.base_dir)
        for file in all_files:
            full_file_path = self.base_dir + file
            if os.path.exists(full_file_path) and file.replace(".mp3","") != file:
                os.remove(full_file_path)
            elif not self.use_test_dir and __name__ == "__main__":
                print(f"could not remove {full_file_path}")

if __name__ == "__main__":
    librar_bad = Librarian("abed",staging,use_test_dir=True)

    # print(librar_bad.data_list)

    librar_good = Librarian("wane",staging,use_test_dir=True)

    #print(librar_good.data_list[0])
    #print('\n')
    #print(librar_good.data_list[1])

