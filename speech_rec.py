import speech_recognition
from api import getApiResponse
from time import sleep
import pyttsx3
from engi1020.arduino.api import *

oled_clear()

def no_audio():
    buzzer_frequency(5, 600)
    sleep(0.2)
    buzzer_frequency(5, 500)
    sleep(0.5)
    buzzer_stop(5)

def select_audio():
    buzzer_frequency(5, 400)
    sleep(0.1)
    buzzer_frequency(5, 500)
    sleep(0.1)
    buzzer_frequency(5, 650)
    sleep(0.1)
    buzzer_frequency(5, 730)
    sleep(0.2)
    buzzer_frequency(5, 650)
    sleep(0.1)
    buzzer_frequency(5, 730)
    sleep(0.6)
    buzzer_stop(5)

def yes_face():
    oled_clear()
    oled_print("                ")
    oled_print("      YES!      ")
    oled_print("     =^..^=     ")
    oled_print("                ")
    sleep(0.1)

def no_face():
    oled_clear()
    oled_print("                ")
    oled_print("       NO       ")
    oled_print("    t(-_-t)     ")
    oled_print("                ")
    sleep(0.1)

def yes_or_no():
    while True:
        oled_clear
        selector = analog_read(0)

        if selector <= 500:
            oled_clear()
            yes_face()

            sleep(0.1)
            selected_word = ('                    SELECTED          YES                       ')
        elif selector >500:
            oled_clear()
            no_face()
           
            sleep(0.1)
            selected_word = ('                    SELECTED           NO                       ')
        if digital_read(6):
            oled_clear()
            oled_print(selected_word)
            if selected_word == ('                    SELECTED          YES                       '):
                select_audio()
            else:
                no_audio()

            return selected_word
        
        sleep(0.1)   

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


recognizer = speech_recognition.Recognizer()
speak("Hi! my name is leo. if you need any assistance just call my name")

while True:
    try:
        with speech_recognition.Microphone() as mic:
            
            print('Listening...')
            digital_write(4,True)
            
            audio = recognizer.listen(mic)  # Record audio for wake word detection
            text = recognizer.recognize_google(audio)  # Convert audio to text
            
            
            if 'leo' in text.lower(): # Check for wake word
                digital_write(4,True)
                buzzer_frequency(5,300)
                sleep(0.2)
                buzzer_stop(5)


                print("Wake word detected. Listening for your query...")
                oled_print("How can i help?")
                speak("How can i help you?")
                sleep(0.5)
                oled_clear()


                audio = recognizer.listen(mic)  # Record the user's query
                text = recognizer.recognize_google(audio)  # Convert audio to text
                print(text)
                digital_write(4,False)
                
                print(f"Recognized Query: {text}")
                speak("Hm,")
                speak(f"did you say. {text}")
                sleep(1)
                
                while True:
                    selected_word = yes_or_no()
                    if selected_word == ('                    SELECTED          YES                       '):
                        response = getApiResponse(text)
                        speak(f"let me answer that. {response}") #Speaks the response back
                        print(f"Response: {response}")# Print the response
                        oled_clear()
                        break
                    elif selected_word == ('                    SELECTED           NO                       '):
                        print("let me try again")
                        speak("let me try again")
                        oled_clear
                        break

                else:
                    print("no button pressed. Returning to listening")
                    continue
                
            else:
                print(f"No wake word detected. Recognized: {text}")
                digital_write(4, True)
                continue
                
    except Exception as e:
        print(f"An error occurred: {e}")
        continue



