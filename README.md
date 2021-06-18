# read vocab cards
SAT is coming up and I want to be able to study without
putting actual effort in. The purpose of this program is to read me the definitions of
different vocab words. I plan to get the definitions and .mp3 files from a dictionary api
that I will talk about below. To play the mp3's I will use the playsound library which you
can pip-install. Once every 3-10 minutes it will read me a word, its definition,
synonyms, antonyms, and use it in a sentence.

#  Dictionary API
Really easy to understand tutorial on how to use the api I'm using can be
found here:
https://dictionaryapi.dev/

# Dependencies
-PlaySound, used to play any .mp3 file
use "pip install playsound" to install it  

-Requests, used to send get requests to the API  

use "pip install requests" to install it  

-gTTS, used to convert text to speech
use "pip install gTTS" to install it