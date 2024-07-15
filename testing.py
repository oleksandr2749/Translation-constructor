import os
from pathlib import Path


def get_all_drives():
    drives = []
    bitmask = os.sysconf("SC_DRIVES")
    for i in range(26):
        if bitmask & (1 << i):
            drives.append(chr(65 + i) + ':\\')
    return drives


def search_294100_folder():
    for drive in get_all_drives():
        for path in Path(drive).rglob('Steam/steamapps/workshop/content/294100'):
            return path.resolve()


# Виклик функції для пошуку
result = search_294100_folder()
if result:
    print(f"Folder found at: {result}")
else:
    print("Folder not found.")
