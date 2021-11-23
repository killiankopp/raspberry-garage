#!/usr/bin/env python3.9
#-- coding: utf-8 --

# bouton entre GND et la pin 11

import RPi.GPIO as GPIO             # GPIO
import time                         # time
import subprocess                   # sous-processus

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)
GPIO.setwarnings(False) #On désactive les messages d'alerte

#NA             =  1 # 3.3V
#NA             =  2 # 5V
#NA             =  3 # GPIO 02
#NA             =  4 # 5V
#NA             =  5 # GPIO 03
#NA             =  6 # GND
#NA             =  7 # GPIO 04
#NA             =  8 # GPIO 14
#NA             =  9 # GND
#NA             = 10 # GPIO 15
BTN             = 11 # GPIO 17
#BUZZER         = 12 # GPIO 18
#NA             = 13 # GPIO 27
#NA             = 14 # GND
#NA             = 15 # GPIO 22
#NA             = 16 # GPIO 23
#RFID           = 17 # 3.3V
#RFID           = 18 # GPIO 24
#RFID           = 19 # GPIO 10
#RFID           = 20 # GND
#RFID           = 21 # GPIO 09
#RFID           = 22 # GPIO 25
#RFID           = 23 # GPIO 11
#RFID           = 24 # GPIO 08
#NA             = 25 # GND
#NA             = 26 # GPIO 07
#NA             = 27 # DNC
#NA             = 28 # DNC
#NA             = 29 # GPIO 05
#NA             = 30 # GND
#NA             = 31 # GPIO 06
#RELAIS_1       = 32 # GPIO 12
#NA             = 33 # GPIO 13
#NA             = 34 # GND
#NA             = 35 # GPIO 19
#NA             = 36 # GPIO 16
#NA             = 37 # GPIO 26
#NA             = 38 # GPIO 20
#NA             = 39 # GND
#NA             = 40 # GPIO 21



GPIO.setup(BTN, GPIO.IN, pull_up_down = GPIO.PUD_UP)



def bip(son = 200, silence = 800):
    subprocess.call("python3 buz.py " + str( son ) + " " + str( silence ), shell=True)



def ouverture():
    subprocess.call("python3 ouverture_garage.py", shell=True)



while True :
    etat = GPIO.input(BTN)

    if (etat == 0) :
        bip(250, 0)
        ouverture()

    time.sleep(0.3) #évite la surchauffe du processeur
