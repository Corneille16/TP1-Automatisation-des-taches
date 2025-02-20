from datetime import datetime
import win32file
import win32api
import win32con
import time
import argparse
import os
import zipfile
import csv


def parse_arguments():
    parser = argparse.ArgumentParser(description="Script de nettoyage de clés USB")
    parser.add_argument("--sauvegarder", type=bool, default=True, help="Sauvegarde les fichiers dans un ZIP")
    parser.add_argument("--effacer", type=bool, default=False, help="Efface les fichiers de la clé USB")
    return parser.parse_args()


def recupere_lecteurs():
    lecteurs = win32api.GetLogicalDriveStrings()
    return lecteurs.split('\000')[:-1]


def est_amovible(lecteur):
    return win32file.GetDriveType(lecteur) == win32con.DRIVE_REMOVABLE


def ecrire_log(lecteur, operations):
    timestamp = datetime.now().__str__()
    message_log = f"{timestamp} - Clé USB {lecteur} - Opérations: {operations}\n"
    with open("../log.txt", 'a') as log:
        log.write(message_log)


def creer_sauvegarde(lecteur, dossier_sauvegarde):
    timestamp = datetime.now().__str__()
    nom_archive = f"sauvegarde_{timestamp}.zip"
    chemin_archive = os.path.join(dossier_sauvegarde, nom_archive)
    with zipfile.ZipFile(chemin_archive, 'w') as zip_file:
        for root, dirs, files in os.walk(lecteur):
            for file in files:
                chemin_archive = os.path.join(root, file)
                try:
                    zip_file.write(chemin_archive, os.path.relpath(chemin_archive, lecteur))
                    fichier_historique(nom_archive, file, timestamp)
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde de {file}: {e}")

    return chemin_archive


def effacer_fichiers(lecteur):
    for root, dirs, files in os.walk(lecteur, topdown=False):
        for name in files:
            try:
                os.remove(os.path.join(root, name))
            except Exception as e:
                print(f"Erreur lors de la suppression de {name}: {e}")
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except Exception as e:
                print(f"Erreur lors de la suppression du dossier {name}: {e}")


def fichier_historique(nom_fichier, nom_fichier_zip, timestamp):
    if not os.path.exists('historique.csv'):
        with open('historique.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Nom fichier', 'Nom fichier zip', 'Timestamp'])

    with open('historique.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nom_fichier_zip, nom_fichier, timestamp])


def main():
    arguments = parse_arguments()
    dosssier_sauvegarde = "sauvegarde"
    os.makedirs(dosssier_sauvegarde, exist_ok=True)
    print("Détection de clé USB en cours...")

    lecteur_precedent = set(recupere_lecteurs())
    try:
        while True:
            lecteur_actuel = set(recupere_lecteurs())
            nouveaux_lecteurs = lecteur_actuel - lecteur_precedent
            for lecteur in nouveaux_lecteurs:
                if est_amovible(lecteur):
                    print(f"\nNouvelle clé USB détectée : {lecteur}")

                    operations = []
                    if arguments.sauvegarder:
                        print("Création de la sauvegarde...")
                        chemin_archive = creer_sauvegarde(lecteur, dosssier_sauvegarde)
                        operations.append("Sauvegarde")
                        print(f"Sauvegarde créée : {chemin_archive}")

                    if arguments.effacer:
                        print("Effacement des fichiers...")
                        effacer_fichiers(lecteur)
                        operations.append("Effacement")
                        print("Fichiers effacés.")

                ecrire_log(lecteur, operations)
                print("Traitement terminé.")

            lecteur_precedent = lecteur_actuel
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nArrêt du programme.")


if __name__ == "__main__":
    #main()
    drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
    usb_labels = {}
    for drive in drives:
        try:
            label = win32api.GetVolumeInformation(drive)[0]  # Nom du volume
            usb_labels[drive] = label
        except:
            pass
    print(usb_labels)

