from engi1020.arduino.api import *
from time import sleep
import random
import pyttsx3

def intrusion_audio():
    speak("INTRUSION")
    digital_write(4,True)
    buzzer_frequency(5,900)
    sleep(0.2)
    speak("INTRUSION")
    digital_write(4,False)
    buzzer_frequency(5,300)
    sleep(0.2)

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
         #print(x) 
         #print(y)
         #print(z)
         xlist.append(three_axis_get_accelX())
         ylist.append(three_axis_get_accelY())
         zlist.append(three_axis_get_accelZ())
         xavg = sum(xlist)/len(xlist)
         yavg = sum(ylist)/len(ylist)
         zavg = sum(zlist)/len(zlist)
         return xavg, yavg, zavg

while True:
    oled_clear()
    o = collect_data(10)
    
    xavg, yavg, zavg = collect_data(10)
     #print(xavg, yavg, zavg) #just to check the values that the axis is reading
    
    if yavg <= -0.23 or yavg > 0.17:
        intrusion_audio()
        intrusion_audio()
        intrusion_audio()
        
        print("INTRUSION!!!!!")
        sleep(0.2)
        oled_print("INTRUSION!!")
        speak("security action to turn the alarm off")
        while True:
               if digital_read(6) == False:
                   continue
               else:
                   oled_clear()
                   buzzer_stop(5)
                   digital_write(4,False)
                   break
            

    light_sensor = analog_read(6)
    if light_sensor >= 5:
        for i in range(2):
            oled_print("INTRUSION!")
            oled_print("(ง •̀_•́)ง")
            intrusion_audio()
            intrusion_audio()
            oled_clear()
           
        oled_clear()
        print("INTRUSION!!!!")
        oled_print("INTRUSION!")
        oled_print("(ง •̀_•́)ง")
        speak("If it was a mistake, Enter Password or Press Button to turn OFF")
        if light_sensor >= 4:
           #speak("Enter Password or Press Button to turn OFF")
           oled_clear()
           oled_print("Whats the       password?")
           password = input("What's the password:")

           sleep(2)
           oled_clear()
           oled_print("Press button    once entered    password")
           while True:
               if password == "apple" and digital_read(6) == True:
                 oled_clear()
                 print("Alaram Disabled")
                 oled_print("Glad You're OK")
                 buzzer_stop(5)
                 digital_write(4,False)
                 sleep(3)
                 break
               if password != 'apple':
                speak("Last chance, What's the password:")
                oled_clear()
                password = input("Last chance, What's the password:")
                oled_print("Last chance, password?")
                if password == "apple" and digital_read(6) == True:
                 oled_clear()
                 print("Alaram Disabled")
                 oled_print("Glad You're OK")
                 buzzer_stop(5)
                 digital_write(4,False)
                 sleep(3)
                 break
                else:
                    continue
                   
               else:
                   oled_clear()
                   buzzer_frequency(5,900)
                   digital_write(4,True)
                   continue 
        
               if password != 'apple':
                speak("Last chance, What's the password:")
                oled_clear()
                password = input("Last chance, What's the password:")
                oled_print("Last chance, password?")
                break
                if digital_read(6) == False:
                   continue
                else:
                   oled_clear()
                   buzzer_stop(5)
                   digital_write(4,False)
                   break

    else:
        continue
    
