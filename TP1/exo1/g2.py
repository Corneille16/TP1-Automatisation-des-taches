import psutil
import argparse


def get_disk():
    return [part.mountpoint for part in psutil.disk_partitions() if "removable" in part.opts]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Script de nettoyage de clés USB")
    parser.add_argument("--sauvegarder", type=bool, default=True, help="Sauvegarde les fichiers dans un ZIP")
    parser.add_argument("--effacer", type=bool, default=False, help="Efface les fichiers de la clé USB")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(f"Sauvegarder : {args.sauvegarder}")
    print(f"Effacer : {args.effacer}")
