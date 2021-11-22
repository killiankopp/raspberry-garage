#!/usr/bin/env python3.9
#-- coding: utf-8 --

import RPi.GPIO as GPIO             # GPIO
import time                         # time
from datetime import datetime       # datetime
import os                           # fichiers
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
#NA             = 11 # GPIO 17
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
RELAIS_1        = 32 # GPIO 12
#NA             = 33 # GPIO 13
#NA             = 34 # GND
#NA             = 35 # GPIO 19
#NA             = 36 # GPIO 16
#NA             = 37 # GPIO 26
#NA             = 38 # GPIO 20
#NA             = 39 # GND
#NA             = 40 # GPIO 21

# Définition des temps en secondes
ouverture   = 15
ouvert      = 26
fermeture   = 22



GPIO.setup(RELAIS_1,    GPIO.OUT)
GPIO.output(RELAIS_1,   GPIO.HIGH)



def bip(son = 200, silence = 800):
    subprocess.call("python3 buz.py " + son + " " + silence, shell=True)



# impulsion d'ouverture de la porte
print("ouverture")
GPIO.output(RELAIS_1, GPIO.LOW)
time.sleep(2)
GPIO.output(RELAIS_1, GPIO.HIGH)

time.sleep(ouverture) # attente pendant l'ouverture de la porte



# attente pendant le passage (entrée ou sortie du garage) + 4 bips courts et un long
time.sleep(ouvert)

for x in range(0, 4):
    bip(200, 800)

bip(1000, 0)



# impulsion de fermeture de la porte
print("fermeture")
GPIO.output(RELAIS_1, GPIO.LOW)
time.sleep(2)
GPIO.output(RELAIS_1, GPIO.HIGH)

# attente pendant la fermeture de la porte
time.sleep(fermeture)
