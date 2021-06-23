# this file has the class that is used to convert text into .mp3 files

# dependencies
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from playsound import playsound
from gtts import gTTS

class Reader():
    def __init__(self, use_test_dir=False):
        self.use_test_dir = use_test_dir
        self.language = "en"
        self.base_dir = "data/text_from_speech/" if not use_test_dir else "data/test/"
    
    def text_to_speech(self, text):
        """convert text to speech and save as mp3"""
        # sanity check the text and create the filename and file_path
        if type(text) == str:
            text = text.lower().strip()
            filename = "lib/" + ((text.replace(" ","_")) + ".mp3")
            file_path = self.base_dir + ((text.replace(" ","_")) + ".mp3")
            if text != "":
                # convert text to .mp3 obj
                speechObj = gTTS(text=text, lang=self.language, slow=False)
                
                # save as an mp3
                speechObj.save(filename)

                #get the file as a var
                with open(filename, "rb") as file_object:
                    file_as_var = file_object.read()

                # move to correct location
                with open(file_path, "wb+") as file_object:
                    file_object.write(file_as_var)
                
                #delete origonal file
                if os.path.exists(filename):
                    os.remove(filename)
                else:
                    print("could not find the .mp3 in lib so could not delete it")
        elif not self.use_test_dir:
            print("I only take strings I was given:\n\n")
            print(text)

    def play_text(self, text_to_play):
        """play text that has already been converted into an mp3"""
        if type(text_to_play) == str:
            # sanity check text
            if text_to_play.lower().strip() != "":
                text_to_play = text_to_play.lower().strip()
                # create the file path
                file_path = self.base_dir + (text_to_play.replace(" ","_") + ".mp3")

                # make sure the file exists
                if os.path.exists(file_path):
                    playsound(file_path)
                else:
                    print(file_path + " was not found and so, could not be played") 
        elif not self.use_test_dir:
            print("I only take strings I was given:\n\n")
            print(text_to_play)  

    def parse_and_play(self,text):
        """convert text to speech and play it all in the same function"""
        if type(text) == str:
            if text.lower().strip() != "":
                text = text.lower().strip()

                # gt filename and file_path
                filename = "tmp_file.mp3"# TODO DEL ME (text.replace(" ","_")) + ".mp3"
                file_path = "lib/" + filename
                
                # convert to speech
                speechObj = gTTS(text=text, lang=self.language, slow=False)

                # save here
                speechObj.save(file_path)

                # play here
                playsound(file_path)

                # delete file here
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    print("file did not exist, and so could not be deleted -- parse and play")
        elif not self.use_test_dir:
            print("I only take strings I was given:\n\n")
            print(text)

    def purge_all_mp3_files(self):
        """remove all files from self.base_dir"""
        all_files = os.listdir(self.base_dir)
        for file in all_files:
            full_file_path = self.base_dir + file
            if os.path.exists(full_file_path) and file.replace(".mp3","") != file:
                os.remove(full_file_path)
            elif not self.use_test_dir:
                print(f"could not remove {full_file_path}")

#im here for testing
if __name__ == "__main__":
    reader = Reader(use_test_dir=True)
    
    #reader.text_to_speech('del me')

    # reader.purge_all_mp3_files()

    # reader.parse_and_play("stringy boi")

    #reader.text_to_speech("     @@@@@@@@@@@@@@@@@@@@@@@@@@@rat@   \n\n")
    #reader.play_text("\n\n        @@@@@@@@@@@@@@@@@@@@@@@@@@@rat@     \n\n\n   ")
