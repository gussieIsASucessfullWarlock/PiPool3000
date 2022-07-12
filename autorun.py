#!/usr/bin/env python3
from ctypes.wintypes import INT
from secrets import choice
from time import sleep
import time
from tkinter import ttk
import librosa
import tkinter as Tk
import librosa.display
import matplotlib.pyplot as plt
from pyparsing import line
from rich.console import Console
import os
import numpy as np
import random
from pygame import mixer
from tkinter import filedialog
import signal
import sys
import datetime
import glob
import threading
import sys
import RPi.GPIO as GPIO
mixer.init()
os.system('cls' if os.name == 'nt' else 'clear')
Console().print("[cyan bold]__________             .__    __________.__  ________ _______  _______  _______     [/cyan bold]")
Console().print("[cyan bold]\______   \____   ____ |  |   \______   \__| \_____  \\   _  \ \   _  \ \   _  \    [/cyan bold]")
Console().print("[cyan bold] |     ___/  _ \ /  _ \|  |    |     ___/  |   _(__  </  /_\  \/  /_\  \/  /_\  \   [/cyan bold]")
Console().print("[cyan bold] |    |  (  <_> |  <_> )  |__  |    |   |  |  /       \  \_/   \  \_/   \  \_/   \  [/cyan bold]")
Console().print("[cyan bold] |____|   \____/ \____/|____/  |____|   |__| /______  /\_____  /\_____  /\_____  /  [/cyan bold]")
Console().print("[cyan bold]                                                    \/       \/       \/       \/   [/cyan bold]")
print("")
print("")
dotsGenerated = 0
squrtDot1 = 0
squrtDot2 = 0
squrtDot3 = 0
squrtDot4 = 0
lastDot = ""
golbalCurrentName = ""
timeElapsed = 0.00
done = 'true'
djMode = False
timeLeft = 0.00


#Pins
pin1 = 12
pin2 = 16
pin3 = 18
pin4 = 23

#Set Pin Mode
def setup():
    global pin1
    global pin2
    global pin3
    global pin4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pin3, GPIO.OUT)
    GPIO.setup(pin4, GPIO.OUT)
    os.system('cls' if os.name == 'nt' else 'clear')
setup()
#Power on meaning off on the realay
def resetPins():
    GPIO.output(pin1, GPIO.HIGH) #Close OFF pipe
    GPIO.output(pin2, GPIO.HIGH) #Close OFF pipe
    GPIO.output(pin3, GPIO.HIGH) #Close OFF pipe
    GPIO.output(pin4, GPIO.HIGH) #Close OFF pipe
    os.system('cls' if os.name == 'nt' else 'clear')
resetPins()

def animate():
    global done
    global timeElapsed
    while done == 'false':
        GPIO.output(a1, GPIO.LOW)
        sleep(0.25)
        GPIO.output(a1, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(a2, GPIO.LOW)
        sleep(0.25)
        GPIO.output(a2, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(a3, GPIO.LOW)
        sleep(0.25)
        GPIO.output(a3, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(a4, GPIO.LOW)
        sleep(0.25)
        GPIO.output(a4, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(a3, GPIO.LOW)
        sleep(0.25)
        GPIO.output(a3, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(a2, GPIO.LOW)
        sleep(0.25)
        GPIO.output(a2, GPIO.HIGH)
        sleep(0.25)

def spray(socket, len, songlen):
    global timeLeft
    global pin1
    global pin2
    global pin3
    global pin4
    resetPins()
    if len == "short":
        timeLeft = timeLeft + 0.125
    else:
        timeLeft = timeLeft + 0.25
    lastDot = socket
    os.system('cls' if os.name == 'nt' else 'clear')
    Console().print("[cyan bold]Currently Playing: " + name + " with " + str(round((timeLeft - songlen), 2)) + "SEC. remaining. [/cyan bold]")
    global dotsGenerated
    global squrtDot1
    global squrtDot2
    global squrtDot3
    global squrtDot4
    output = ""
    colors = ["blue", "cyan", "green", "pink", "red", "yellow"]
    choice = random.choice(colors)
    choice2 = random.choice(colors)
    choice3 = random.choice(colors)
    choice4 = random.choice(colors)
    if "1" in socket:
        output = "[" + choice + "] 0 0 [/" + choice + "]"
        squrtDot1 = squrtDot1 + 1
        GPIO.output(pin1, GPIO.LOW) #Open UP Pipe
    else:
        output = "[bold] . . [/bold]"
    if "2" in socket:
        output = output + "[" + choice2 + "] 0 0 [/ " + choice2 +" ]"
        squrtDot2 = squrtDot2 + 1
        GPIO.output(pin2, GPIO.LOW) #Open UP Pipe
    else:
        output = output + "[bold] . . [/bold]"
    if "3" in socket:
        output = output + "[" + choice3 + "] 0 0 [/ " + choice3 +" ]"
        squrtDot3 = squrtDot3 + 1
        GPIO.output(pin3, GPIO.LOW) #Open UP Pipe
    else:
        output = output + "[bold] . . [/bold]"
    if "4" in socket:
        output = output + "[" + choice4 + "] 0 0 [/ " + choice4 +" ]"
        squrtDot4 = squrtDot4 + 1
        GPIO.output(pin4, GPIO.LOW) #Open UP Pipe
    else:
        output = output + "[bold] . . [/bold]"
    Console().print(output)
    dotsGenerated += 4

def pickDot(randomAAR):
    global lastDot
    choice = random.choice(randomAAR)
    return(choice)

def playSong(name, songfliedir, noOptions):
    global done
    global djMode
    done = 'false'
    t = threading.Thread(target=animate)
    t.start()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(name)
    compstart = time.time()
    songLength = round(librosa.get_duration(filename=songfiledir))
    y, sr = librosa.load(songfiledir, duration=songLength)
    y_harm, y_perc = librosa.effects.hpss(y)
    dataSetTotal = 0
    intervals = 0.25
    for i in y_perc:
        dataSetTotal = dataSetTotal + 1

    dataSetIntervals = round((dataSetTotal * intervals) / songLength)
    currentInterval = 0
    audioLevels = []
    intervalSamples = []
    for i in y_perc:
        if audioLevels == []:
            audioLevels = audioLevels + [i]
            intervalSamples = intervalSamples + [currentInterval]
        elif dataSetIntervals == currentInterval:
            audioLevels = audioLevels + [i]
            intervalSamples = intervalSamples + [currentInterval]
            currentInterval = -1
        currentInterval = currentInterval + 1

    countAvrage = 0
    lenAvrage = 0
    for i in audioLevels:
        lenAvrage = lenAvrage + 1
        countAvrage = countAvrage + i
    dataAvrage = countAvrage / lenAvrage
    compend = time.time()
    done = 'true'
    if djMode:
        #run Program
        os.system('cls' if os.name == 'nt' else 'clear')
        mixer.music.load(songfiledir)
        mixer.music.play()

        os.system('cls' if os.name == 'nt' else 'clear')
        Console().print("[cyan bold]__________             .__    __________.__  ________ _______  _______  _______     [/cyan bold]")
        Console().print("[cyan bold]\______   \____   ____ |  |   \______   \__| \_____  \\   _  \ \   _  \ \   _  \    [/cyan bold]")
        Console().print("[cyan bold] |     ___/  _ \ /  _ \|  |    |     ___/  |   _(__  </  /_\  \/  /_\  \/  /_\  \   [/cyan bold]")
        Console().print("[cyan bold] |    |  (  <_> |  <_> )  |__  |    |   |  |  /       \  \_/   \  \_/   \  \_/   \  [/cyan bold]")
        Console().print("[cyan bold] |____|   \____/ \____/|____/  |____|   |__| /______  /\_____  /\_____  /\_____  /  [/cyan bold]")
        Console().print("[cyan bold]                                                    \/       \/       \/       \/   [/cyan bold]")
        print("")
        print("")





        a = datetime.datetime.now()
        b = a + datetime.timedelta(0,songLength)
        for i in audioLevels:
            if datetime.datetime.now() < b :
                if i == 0:
                    sleep(intervals)
                elif i > dataAvrage:
                    randomAAR = ["14", "24", "34", "13", "23", "21", "123", "134", "124", "234"]
                    spray(random.choice(randomAAR), "short", songLength)
                    sleep(intervals / 2)
                    spray(random.choice(randomAAR), "short", songLength)
                    sleep(intervals / 2)
                elif i < dataAvrage:
                    spray(pickDot(["1", "2", "3", "4"]), "long", songLength)
                    sleep(intervals)
    else:
        #run Program
        mixer.music.load(songfiledir)
        mixer.music.play()

        os.system('cls' if os.name == 'nt' else 'clear')
        Console().print("[cyan bold]__________             .__    __________.__  ________ _______  _______  _______     [/cyan bold]")
        Console().print("[cyan bold]\______   \____   ____ |  |   \______   \__| \_____  \\   _  \ \   _  \ \   _  \    [/cyan bold]")
        Console().print("[cyan bold] |     ___/  _ \ /  _ \|  |    |     ___/  |   _(__  </  /_\  \/  /_\  \/  /_\  \   [/cyan bold]")
        Console().print("[cyan bold] |    |  (  <_> |  <_> )  |__  |    |   |  |  /       \  \_/   \  \_/   \  \_/   \  [/cyan bold]")
        Console().print("[cyan bold] |____|   \____/ \____/|____/  |____|   |__| /______  /\_____  /\_____  /\_____  /  [/cyan bold]")
        Console().print("[cyan bold]                                                    \/       \/       \/       \/   [/cyan bold]")
        print("")
        print("")





        a = datetime.datetime.now()
        b = a + datetime.timedelta(0,songLength)
        for i in intervalSamples:
            if datetime.datetime.now() < b :
                if y_perc[i] > y_harm[i]:
                    if y_perc[i] >= dataAvrage:
                        randomAAR = ["1", "2", "3", "4"]
                        spray(random.choice(randomAAR), "long", songLength)
                        sleep(intervals)
                else:
                    randomAAR = ["13", "24"]
                    spray(random.choice(randomAAR), "short", songLength)
                    sleep(intervals)
    os.system('cls' if os.name == 'nt' else 'clear')
    Console().print("[cyan bold]__________             .__    __________.__  ________ _______  _______  _______     [/cyan bold]")
    Console().print("[cyan bold]\______   \____   ____ |  |   \______   \__| \_____  \\   _  \ \   _  \ \   _  \    [/cyan bold]")
    Console().print("[cyan bold] |     ___/  _ \ /  _ \|  |    |     ___/  |   _(__  </  /_\  \/  /_\  \/  /_\  \   [/cyan bold]")
    Console().print("[cyan bold] |    |  (  <_> |  <_> )  |__  |    |   |  |  /       \  \_/   \  \_/   \  \_/   \  [/cyan bold]")
    Console().print("[cyan bold] |____|   \____/ \____/|____/  |____|   |__| /______  /\_____  /\_____  /\_____  /  [/cyan bold]")
    Console().print("[cyan bold]                                                    \/       \/       \/       \/   [/cyan bold]")
    print("")
    print("")
    print("-------------------------------------------")
    print( str(dotsGenerated * 2) + " dots generated")
    print("Dot set 1 was displayed " + str(squrtDot1) + " times.")
    print("Dot set 2 was displayed " + str(squrtDot2) + " times.")
    print("Dot set 3 was displayed " + str(squrtDot3) + " times.")
    print("Dot set 4 was displayed " + str(squrtDot4) + " times.")
    total_time = compend - compstart
    print("")
    print("-------------------------------------------")
    print("Computation Time "+ str(total_time) + "sec.")
    print("Avrage Waveform "+ str(dataAvrage) + ".")
    print("Song Length "+ str(songLength) + ".")

def sigint_handler(signal, frame):
    resetPins()
    print("")
    print( str(dotsGenerated * 2) + " dots generated")
    print("Dot set 1 was displayed " + str(squrtDot1) + " times.")
    print("Dot set 2 was displayed " + str(squrtDot2) + " times.")
    print("Dot set 3 was displayed " + str(squrtDot3) + " times.")
    print("Dot set 4 was displayed " + str(squrtDot4) + " times.")
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)
while True:
	dir = "/var/www/html/playlist"
	for songfiledir in glob.glob(dir + "/*"):
	    name = songfiledir.split("/")[-1].removesuffix(".mp3").removesuffix(".wav")
	    golbalCurrentName = name
	    noOptions = True
	    playSong(name, songfiledir, noOptions)
	    GPIO.cleanup()
	    setup()
	    resetPins()
