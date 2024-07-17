from pathlib import Path
def search_294100_folder():
    volumes = ['/', 'A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:',]

    for volume in volumes:
        for path in Path(volume).rglob('Steam/steamapps/workshop/content/294100'):
            return path.resolve()

print(search_294100_folder())
