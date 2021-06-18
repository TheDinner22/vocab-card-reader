# this file has the class that is used to convert text into .mp3 files

# dependencies
import os, sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # adds project dir to places it looks for the modules
sys.path.append(BASE_PATH)

from gtts import gTTS

class Reader():
    def __init__(self, use_test_dir=False):
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
        else:
            print("I only take strings I was given:\n\n")
            print(text)

    def play_text(self, text_to_play):
        """play text that has already been converted into and mp3"""
        pass

    def parse_and_play(self,text):
        """convert text to speech and play it all in the same function"""
        pass

#im here for testing
if __name__ == "__main__":
    reader = Reader() #use_test_dir=True)
    reader.text_to_speech("     skippity bop mm da da    \n\n")
