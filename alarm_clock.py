from engi1020.arduino.api import *
from time import sleep
import random
import pyttsx3


engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

xlist = []
ylist = []
zlist = []
def collect_data(samples):
    
    for i in range(samples):
#          x = three_axis_get_accelX()
#          y = three_axis_get_accelY()
#          z = three_axis_get_accelZ()
         #print(x) #just to check values 
         #print(y) #just to check values 
         #print(z) #just to check values 
         xlist.append(three_axis_get_accelX())
         ylist.append(three_axis_get_accelY())
         zlist.append(three_axis_get_accelZ())
         xavg = sum(xlist)/len(xlist)
         yavg = sum(ylist)/len(ylist)
         zavg = sum(zlist)/len(zlist)
         return xavg, yavg, zavg

def alarm_clock():
    
    while True:
        oled_clear()
        
                
        light_sensor = analog_read(6)
        if light_sensor >= 5:
            for i in range(2):
                
                oled_print("                     WAKE UP        (ง •̀_•́)ง")
                speak("WAKE UP!!!!")
                digital_write(4,True)
                buzzer_frequency(5,900)
                sleep(0.2)
                speak("WAKE UP!!!!")
                digital_write(4,False)
                buzzer_frequency(5,300)
                sleep(0.2)
                speak("WAKE UP!!!!")
                digital_write(4,True)
                buzzer_frequency(5,900)
                sleep(0.2)
                speak("get out of bed")
                digital_write(4,False)
                buzzer_frequency(5,300)
                sleep(0.2)
                speak("you have class")
                digital_write(4,True)
                buzzer_frequency(5,900)
                sleep(0.2)
                speak("get up now")
                digital_write(4,False)
                buzzer_frequency(5,300)
                sleep(0.2)
                speak("you dont wanna fail")
                digital_write(4,True)
                buzzer_frequency(5,900)
                sleep(0.2)
                speak("WAKE UP!!!!")
                digital_write(4,False)
                buzzer_frequency(5,300)
                sleep(0.2)
                speak("WAKE UP!!!!")
                digital_write(4,True)
                buzzer_frequency(5,900)
                sleep(0.2)
                speak("WAKE UP!!!!")
                digital_write(4,False)
                buzzer_frequency(5,300)
                sleep(0.2)
                speak("i will call your mom")
                digital_write(4,True)
                buzzer_frequency(5,900)
                sleep(0.2)
                speak("WAKE UP!!!!")
                digital_write(4,False)
                buzzer_frequency(5,300)
                sleep(0.2)

            oled_clear()
            print("WAKE UP")
            oled_print("                     WAKE UP        (ง •̀_•́)ง")
            speak("enter password and press button to turn off")
            #password = input("enter password:")
            if light_sensor >= 4:
             password = input("whats the password:")
             oled_print("whats the password?")
             sleep(2)
             oled_clear()
             oled_print("press button once entered password")
            while True:
                if digital_read(6) == False:
                    continue
                else:
                    oled_clear()
                    buzzer_stop(5)
                    digital_write(4,False)
                    continue
 
            
            if password == "apple":
                oled_clear()
                print("Alaram disabled")
                oled_print("youre good.")
                buzzer_stop(5)
                digital_write(4,False)
                
            else:
                oled_clear()
                password = input("last chance, whats the password:")
                oled_print("last chance, password?")
                if digital_read(6) == True:
                    print("Alaram disabled")
                    oled_print("youre good.")
                    buzzer_stop(5)
                    digital_write(4,False)
                
                if password == "apple":
                  oled_clear()
                  print("Alaram disabled")
                  oled_print("youre good.")
                  buzzer_stop(5)
                  digital_write(4,False)
        else:
            continue
        
alarm_clock()