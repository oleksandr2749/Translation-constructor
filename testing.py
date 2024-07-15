from pathlib import Path


def search_294100_folder():
    for path in Path('/').rglob('Steam/steamapps/workshop/content/294100'):
        return path.resolve()


print(search_294100_folder())
