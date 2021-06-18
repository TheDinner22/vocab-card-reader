# this file has the class that is used to convert text into .mp3 files

from gtts import gTTS

class Reader():
    def __init__(self):
        self.ping = 200
    
    def text_to_speech(self, text):
        """convert text to speech and save as mp3"""
        pass

    def play_text(self, text_to_play):
        """play text that has already been converted into and mp3"""
        pass

    def parse_and_play(self,text):
        """convert text to speech and play it all in the same function"""
        pass
