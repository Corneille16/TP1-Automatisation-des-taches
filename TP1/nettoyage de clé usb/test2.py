import psutil


def get_removable_drives():
    # Retourne les lettres des lecteurs amovibles
    return [part.mountpoint for part in psutil.disk_partitions(all=False) if 'removable' in part.opts]


if __name__ == "__main__":
    removable_drives = get_removable_drives()
    print(removable_drives)
    print("Lecteurs amovibles :")
    for drive in removable_drives:
        print(drive)
