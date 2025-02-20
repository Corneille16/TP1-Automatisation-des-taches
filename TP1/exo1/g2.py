import os
import zipfile
from datetime import datetime
import psutil
import argparse
import win32api
import win32file


def get_disk():
    return [part.device for part in psutil.disk_partitions() if "removable" in part.opts]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Script de nettoyage de clés USB")
    parser.add_argument("--sauvegarder", default=True, action='store_false',
                        help="Sauvegarde les fichiers dans un ZIP(par défaut True)")
    parser.add_argument("--effacer", action='store_true', default=False,
                        help="Efface les fichiers de la clé USB(par défaut False)")
    return parser.parse_args()


def ecrire_log(disque, operations):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nom_disque = win32api.GetVolumeInformation(disque)[0]
    message_log = f"{timestamp} - Disque {nom_disque} - Opérations: {operations}\n"
    with open("log.txt", "a") as log:
        log.write(message_log)


def creer_archive_zip(cle_usb, dossier_sauvegarde):
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
                archive.write(chemin_fichier, arcname)

    print(f"Fichier sauvegardé : {archive_path}")


if __name__ == "__main__":
    disques = get_disk()
    for disque in disques:
        creer_archive_zip(disque, "sauvegarde")
