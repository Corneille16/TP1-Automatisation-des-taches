import csv
import os
import time
import zipfile
from datetime import datetime
import psutil
import argparse
import win32api


def detecter_cles_usb():
    """Retourne la liste des périphériques de stockage connectés."""
    return [part.device for part in psutil.disk_partitions() if "removable" in part.opts]


def recuperer_arguments():
    """Gère les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(description="Script de nettoyage de clés USB")
    parser.add_argument("--sauvegarder", default=True, action='store_true',
                        help="Sauvegarde les fichiers dans un ZIP(par défaut True)")
    parser.add_argument("--effacer", action='store_true', default=False,
                        help="Efface les fichiers de la clé USB(par défaut False)")
    return parser.parse_args()


def ecrire_log(cle, operations):
    """Écrit les opérations effectuées dans un fichier log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nom_cle = win32api.GetVolumeInformation(cle)[0]
    message_log = f"{timestamp} - Clé {nom_cle} - Opérations: {operations}\n"
    with open("log.txt", "a") as log:
        log.write(message_log)


def creer_archive_zip(cle_usb, dossier_sauvegarde):
    """Crée une archive ZIP du contenu de la clé USB."""
    if not os.path.exists(dossier_sauvegarde):
        os.makedirs(dossier_sauvegarde)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nom_archive = f"sauvegarde_{timestamp}.zip"
    archive_path = os.path.join(dossier_sauvegarde, nom_archive)

    with zipfile.ZipFile(archive_path, "w") as archive:
        for root, dirs, files in os.walk(cle_usb):
            for file in files:
                chemin_fichier = os.path.join(root, file)
                arcname = os.path.relpath(chemin_fichier, cle_usb)
                try:
                    archive.write(chemin_fichier, arcname)
                    fichier_historique_csv(nom_archive, file, timestamp)
                except Exception as e:
                    print(f"Erreur lors de la sauvegarde de {file}: {e}")

    print(f"Fichier sauvegardé : {archive_path}")


def effacer_fichiers(cle_usb):
    """Efface tous les fichiers et dossiers de la clé USB."""
    for root, dirs, files in os.walk(cle_usb, topdown=False):
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


def fichier_historique_csv(nom_archive, nom_fichier_sauvegarde, timestamp):
    """Ajoute une entrée dans l'historique des sauvegardes (fichier CSV)."""
    if not os.path.exists("historique.csv"):
        with open("historique.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Nom archive", "Nom fichier sauvegardé", "Timestamp"])
    with open("historique.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([nom_archive, nom_fichier_sauvegarde, timestamp])


if __name__ == "__main__":
    arguments = recuperer_arguments()
    dossier_sauvegarde = "../../Sauvegardes"
    cles_precedentes = set(detecter_cles_usb())
    print("Surveillance des clés USB... (Ctrl + C pour arrêter)")

    try:
        while True:
            cles_actuelles = set(detecter_cles_usb())
            nouvelles_cles = cles_actuelles - cles_precedentes

            for cle_usb in nouvelles_cles:
                nom_cle = win32api.GetVolumeInformation(cle_usb)[0]
                print(f"Nouvelle clé USB détectée : {nom_cle}")

                operation = []
                if arguments.sauvegarder:
                    print("Creation de l'archive ZIP...")
                    creer_archive_zip(cle_usb, dossier_sauvegarde)
                    operation.append("Sauvegarde")
                    print("Sauvegarde terminé")

                if arguments.effacer:
                    print("Suppression des fichiers...")
                    effacer_fichiers(cle_usb)
                    operation.append("Suppression")
                    print("Fichiers supprimés")

                ecrire_log(cle_usb, operation)

            cles_precedentes = cles_actuelles
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du script.")
