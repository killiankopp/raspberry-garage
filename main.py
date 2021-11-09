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

rc522 = RFID() #On instancie la lib

print('Système armé') #On affiche un message demandant à l'utilisateur de passer son badge

#On va faire une boucle infinie pour lire en boucle
while True :
    rc522.wait_for_tag() #On attnd qu'une puce RFID passe à portée
    (error, tag_type) = rc522.request() #Quand une puce a été lue, on récupère ses infos

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
                    print('OK')
                    fichier = open("logs/success.log", "a")
                    fichier.write(s1 + " " + format(uid) +  "\n")
                    fichier.close()
                else :
                    print('KO')
                    fichier = open("logs/error.log", "a")
                    fichier.write(s1 + " " + format(uid) +  "\n")
                    fichier.close()
                    
            #print(s1 + ' {}'.format(uid)) #On affiche l'identifiant unique du badge RFID
            time.sleep(1) #On attend 1 seconde pour ne pas lire le tag des centaines de fois en quelques milli-secondes
