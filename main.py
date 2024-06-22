#Import Libraries
import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import *
from time import sleep
import sys
import threading
from tkinter import Tk

# Color Sensor Setup
s2 = 23
s3 = 24
s0 = 22
s1 = 27
signal = 25
NUM_CYCLES = 10

# Color Cup Positions
red1 = 0
green1 = 78
yellow1=55
purple1=100
orange1=29
misc1=120

# Number of colors sorted
numRed = 0
numGreen = 0
numYellow = 0
numPurple = 0
numOrange = 0
numMisc = 0

# GPIO setup for color sensor
def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  GPIO.setup(s0,GPIO.OUT)
  GPIO.setup(s1,GPIO.OUT)

# Stepper Motor Setup
motor_channel = (5,6,13,19)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_channel, GPIO.OUT)

# Servo Setup
servo_pin = 17
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin,50) # 50 Hz (20 ms PWM period)


paused = False  # Flag to indicate if the operation is paused
stopped = False  # Flag to indicate if the operation is stopped
previous = None # Previous cup position

# Color Sensing Function
def detect_color():
    setup() #setup color setup
    temp = 1
    GPIO.output(s0,GPIO.LOW)
    GPIO.output(s1,GPIO.HIGH)
    #While True
    while(1):
        red = 0
        green = 0
        blue = 0
        for x in range(30):
          #Sense Red Value
          GPIO.output(s2,GPIO.LOW)
          GPIO.output(s3,GPIO.LOW)
          time.sleep(0.001)
          start = time.time()
          for impulse_count in range(NUM_CYCLES):
              GPIO.wait_for_edge(signal, GPIO.FALLING)
          duration = time.time() - start 
          red += NUM_CYCLES / duration   

          #Sense Blue Value 
          GPIO.output(s2,GPIO.LOW)
          GPIO.output(s3,GPIO.HIGH)
          time.sleep(0.001)
          start = time.time()
          for impulse_count in range(NUM_CYCLES):
              GPIO.wait_for_edge(signal, GPIO.FALLING)
          duration = time.time() - start
          blue += NUM_CYCLES / duration

          #Sense Green Value
          GPIO.output(s2,GPIO.HIGH)
          GPIO.output(s3,GPIO.HIGH)
          time.sleep(0.001)
          start = time.time()
          for impulse_count in range(NUM_CYCLES):
              GPIO.wait_for_edge(signal, GPIO.FALLING)
          duration = time.time() - start
          green += NUM_CYCLES / duration  

        #get average values
        red/=30
        green/=30
        blue/=30
        
        #Determine Color Using Red, Green, Blue Values 
        if red>1160 and red<1280 and green>955 and green<1040 and blue>1225 and blue<1360:
            print("green")
            return "green"
            temp=1
        elif red>1220 and red<1400 and green>920 and green<956 and blue>1260 and blue<1350:
            print("orange")
            return "orange"
            temp=1
        elif red>1200 and red<1290 and green>880 and green<970 and blue>1225 and blue<1360:
            print("red")
            return "red"
            temp=1
        elif red>1280 and red<1400 and green>1000 and green<1080 and blue>1230 and blue<1330:
            print("yellow")
            return "yellow"
            temp=1
        elif red>1090 and red<1200 and green>880 and green<970 and blue>1220 and blue<1320:
            print("purple")
            return "purple"
            temp=1
        else:
            print("place the object...")
            return "misc"
            temp=0

#move the stepper clockwise by num times
def move_stepper_clockwise(num):
    for x in range(num):
        try:
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
            time.sleep(0.02)
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
            time.sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
            time.sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
            time.sleep(0.02)
        except():
            print()

#move the stepper anticlockwise by num times
def move_stepper_anticlockwise(num):
    for x in range(num)
        try:
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH))
            time.sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.LOW,GPIO.HIGH,GPIO.HIGH))
            time.sleep(0.02)
            GPIO.output(motor_channel, (GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW))
            time.sleep(0.02)
            GPIO.output(motor_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.LOW,GPIO.LOW))
            time.sleep(0.02)
        except():
            print()

#sorting candy function       
def sort_candy():
    #Get variables
    global paused, stopped
    global previous
    global red1, orange1, yellow1, green1, purple1, misc1
    global numRed, numOrange, numGreen, numYellow, numPurple, numMisc
    global lblmain
    
    #While program is not paused
    while paused==False:
        lblmain.config(text="Getting Candy")
        print("candy")

        #Move servo to get candy
        pwm.start(8.6) # start PWM by rotating to 90 degrees
        pwm.ChangeDutyCycle(8.6) # rotate to candy tube
        time.sleep(1)
        
        #Move servo under the color sensor
        pwm.ChangeDutyCycle(6.9) # rotate to color sensor
        time.sleep(1)
        pwm.ChangeDutyCycle(0) # this prevents jitter
        
        #Detect Color
        detected_color = detect_color()
        count = 0
        while detected_color == "misc":
            detected_color = detect_color()
            count+=1
            if count>50:
                break
        print(detected_color)
        
        # move stepper based on detected color

        lblmain.config(text="Sorting...")
        if detected_color == "red":
            numRed=numRed+1 #update number of reds sorted
            num = red1
            move_stepper_clockwise(abs(num)) #move the stepper
            previous = red1 #update stepper location
        elif detected_color == "green":
            numGreen=numGreen+1
            num = green1
            move_stepper_clockwise(abs(num))
            previous = green1
        elif detected_color == "yellow":
            numYellow=numYellow+1
            num = yellow1
            move_stepper_clockwise(abs(num))
            previous = yellow1
        elif detected_color == "orange":
            numOrange=numOrange+1
            num = orange1
            move_stepper_clockwise(abs(num))
            previous = orange1
        elif detected_color == "purple":
            numPurple=numPurple+1
            num = purple1
            move_stepper_clockwise(abs(num))
            previous = purple1
        elif detected_color == "misc":
            numMisc=numMisc+1
            num = misc1
            move_stepper_clockwise(abs(num))
            previous = misc1

        updateR()
        #move servo to drop the candy 
        pwm.ChangeDutyCycle(2.4) # rotate to 180 degrees
        time.sleep(1)
        print('reset')
        lblmain.config(text="Reset...")

        #move stepper back
        move_stepper_anticlockwise(abs(previous-red1))
        
        while paused:
            time.sleep(0.1)  # Wait while the operation is paused
            if stopped:
                return  # Stop the operation if the stop flag is set

def pause():
    global paused
    paused = True

def resume():
    global paused
    paused = False

def stop():
    global stopped
    stopped = True

def cleanup():
    pwm.stop() 
    GPIO.cleanup()

#Find the most common element in a list
def most_common(List):
    return max(set(List), key=List.count)

def start_candy_sort():
  t1 = threading.Thread(target=sort_candy, args=())
  t1.start()
  
#update GUI for the candy counts
def updateR():
    lRed['text']="Red "+str(numRed)
    lRed.pack()
    lGreen['text']="Green "+str(numGreen)
    lGreen.pack()
    lOrange['text']="Orange "+str(numOrange)
    lOrange.pack()
    lYellow['text']="Yellow "+str(numYellow)
    lYellow.pack()
    lPurple['text']="Purple "+str(numPurple)
    lPurple.pack()
    lMisc['text']="Misc "+str(numMisc)
    lMisc.pack()
    parent.after(100, updateR)
    
# GUI

parent = Tk(className = 'Color Sorter Project') #Create window Tk w/ Title
parent = tk.Tk()
parent.geometry('500x500') #Window Size

frame = tk.Frame(parent)
frame.pack()

# Create label
title = Label(parent, text = "Color Sorter Program")
title.config(font =("Arial", 14))
title.pack()

#status
lblmain = Label(parent, text='Ready') #create a label on main window called root
lblmain.config(text='Click the start button to begin: ')

sort_candy_button = tk.Button(frame, text="Sort Candy", command=sort_candy)
sort_candy_button.pack()

pause_button = tk.Button(frame, text="Pause", command=pause)
pause_button.pack()

resume_button = tk.Button(frame, text="Resume", command=resume)
resume_button.pack()

stop_button = tk.Button(frame, text="Stop", command=stop)
stop_button.pack()

#Candy counts
lRed = Label(parent, text = "Red 0")
lRed.config(font =("Arial", 10))
lRed.pack()

lGreen = Label(parent, text = "Green 0")
lGreen.config(font =("Arial", 10))
lGreen.pack()

lYellow = Label(parent, text = "Yellow 0")
lYellow.config(font =("Arial", 10))
lYellow.pack()

lOrange = Label(parent, text = "Orange 0")
lOrange.config(font =("Arial", 10))
lOrange.pack()

lPurple = Label(parent, text = "Purple 0")
lPurple.config(font =("Arial", 10))
lPurple.pack()

lMisc = Label(parent, text = "Misc 0")
lMisc.config(font =("Arial", 10))
lMisc.pack()

lblmain.pack() #force label to be visible
parent.mainloop()
