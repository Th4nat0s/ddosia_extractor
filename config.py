#!/bin/env python3
import re
import os
import sys
import subprocess
import json
import hashlib
from datetime import datetime, timezone

def find_random(data,pattern):
    # La séquence "random" en binaire (en bytes)

    # Parcourir les données
    for i in range(len(data) - len(pattern) + 1):
        # Extraire une sous-séquence de la longueur de la séquence "random"
        subsequence = data[i:i + len(pattern)]

        # Vérifier si la sous-séquence correspond à la séquence "random"
        if subsequence == pattern:
            # La séquence "random" a été trouvée à l'emplacement i
            return i

    # Si la séquence n'a pas été trouvée
    return -1

def confnotseen(md5):
    # regarde si le hash est deja la
    # Ouvrir le fichier texte
    with open("hashs.txt", 'r') as fichier:
        # Ouvrir le fichier texte en mode lecture
        lignes = fichier.readlines()

    # cree l'array md5 sans crlf
    md5s = []
    for ligne in lignes:
        md5s.append(ligne.strip())  # strip() enlève les caractères de saut de ligne ('\n')

    # Sauve les 6 derniesr md5 
    if md5 not in md5s:
        md5s = md5s[-5:]  # save last 5 item of the list
        md5s.append(md5)
        # Ouvrir le fichier texte en mode écriture
        with open('hashs.txt', 'w') as fichier:
            # erire chaque élément de la liste suivi d'un saut de ligne
            for element in md5s:
                fichier.write(element + '\n')
        return True
    return False


print("Starting DDos Agent")
# Définissez la commande avec ses paramètres sous forme de liste
commande = ["gdb", "-x","./ddosia_dump.gdb", "./d_lin_x64"]

# Exécutez la commande et attendez qu'elle se termine
processus = subprocess.Popen(commande)

# Attendre que le processus se termine
processus.wait()
print("Dump Done")

# Récupérez le paramètre à partir de sys.argv
file = "dump"

print("Extracting config")
# Ouvrir le fichier binaire en mode lecture binaire ('rb')
with open(file, 'rb') as fichier:
    # Lire le contenu du fichier en tant que données binaires (bytes)
    data = fichier.read()

    # Cleanp data looking for a string random at start and a double stop byte at end
    result = find_random(data, b'{"random')
    data = data[result:]
    result = find_random(data, b'\x00\x00')
    data = data[:result]
    contenu = data.decode('utf', errors='replace')

    # Appliquer une expression régulière directement sur les données binaires
    pattern = r'{"randoms".*}'  
    resultats = re.findall(pattern, contenu)

    # Traiter les résultats
    for resultat in resultats:
        out_json = json.loads(resultat)

    # Créer un objet hasher MD5
    md5_hasher = hashlib.md5()

    json_str = json.dumps(out_json, indent=4)
    # Mettre le hasher avec la chaîne (convertie en bytes)
    md5_hasher.update(json_str.encode('utf', errors="replace"))

    # Obtenir la somme de contrôle MD5 sous forme de chaîne hexadécimale
    md5_sum = md5_hasher.hexdigest()

    if confnotseen(md5_sum):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        nom_fichier = f"confs/{timestamp}_ddosia.json"

        with open(nom_fichier, "w") as fichier_json:
            fichier_json.write(json_str)
    else:
        print("Configuration already saved")
