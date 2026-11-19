import speech_recognition
import openai 
from api import getApIresponse

recognizer = speech_recognition.Recognizer()

with speech_recognition.Microphone() as mic:
    audio = recognizer.listen(mic)
    text = recognizer.recognize_sphinx(audio)
    print(text)
    print("getting the response")
    print(getApIresponse(text))


