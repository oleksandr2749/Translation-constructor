from pathlib import Path


def search_294100_folder():
    drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:']
    for drive in drives:
        try:
            for path in Path(drive).rglob('Steam/steamapps/workshop/content/294100'):
                return path.resolve()
        except PermissionError:
            # Пропустити диски, до яких немає доступу
            continue


print(search_294100_folder())
