#!/usr/bin/env python3.9
#-- coding: utf-8 --

import RPi.GPIO as GPIO #Importe la bibliothèque pour contrôler les GPIOs
from pirc522 import RFID
import time

# biblio datetime
from datetime import datetime

# biblio liste des fichiers
import os

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
BUZZER          = 12 # GPIO 18
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

GPIO.setup(BTN,         GPIO.IN,    pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER,      GPIO.OUT)
GPIO.setup(RELAIS_1,    GPIO.OUT)

rc522 = RFID() #On instancie la lib



def bip(pin, son = 200, silence = 800):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(son / 1000)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(silence / 1000)



def ouveture():
    # impulsion d'ouverture de la porte
    GPIO.output(RELAIS_1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RELAIS_1, GPIO.LOW)

    # attente pendant l'ouverture de la porte
    time.sleep(15)

    # attente pendant le passage (entrée ou sortie du garage) + 3 bips courts et un long
    time.sleep(6)
    for x in range(0, 3)
        bip(BUZZER)

    bip(BUZZER, 1000, 0)

    # impulsion de fermeture de la porte
    GPIO.output(RELAIS_1, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RELAIS_1, GPIO.LOW)

    # attente pendant la fermeture de la porte
    time.sleep(22)



print('Système armé') #On affiche un message demandant à l'utilisateur de passer son badge

#On va faire une boucle infinie pour lire en boucle
while True :
    rc522.wait_for_tag() #On attnd qu'une puce RFID passe à portée
    (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos

    if (GPIO.input(BTN) == 0):
        ouverture()

    if not error : #Si on a pas d'erreur
        (error, uid) = rc522.anticoll() #On nettoie les possibles collisions, ça arrive si plusieurs cartes passent en même temps

        if not error : #Si on a réussi à nettoyer
            now = datetime.now()
            s1 = now.strftime("%Y-%m-%d %H:%M:%S")

            fichier = open("logs/access.log", "a")
            fichier.write(s1 + " " + format(uid) +  "\n")
            fichier.close()

            badges = os.listdir('authorized')
            uid_flat = str(uid[0]) + "-" + str(uid[1]) + "-" + str(uid[2]) + "-" + str(uid[3]) + "-" + str(uid[4])

            for badge in badges :
                if badge == uid_flat :
                    bip(BUZZER, 500, 0)
                    print('OK')
                    fichier = open("logs/success.log", "a")
                    fichier.write(s1 + " " + format(uid) +  "\n")
                    fichier.close()

                    ouverture()
                else :
                    bip(BUZZER, 100, 100)
                    bip(BUZZER, 100, 100)
                    bip(BUZZER, 100, 100)
                    print('KO')
                    fichier = open("logs/error.log", "a")
                    fichier.write(s1 + " " + format(uid) +  "\n")
                    fichier.close()

            #print(s1 + ' {}'.format(uid)) #On affiche l'identifiant unique du badge RFID
            time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-secondes
