import os
from pathlib import Path
import shutil

import ModificationClass
# import UI
import Process

import ModificationClass
ModList = ModificationClass.create_mod_list(path_294100=ModificationClass.search_294100_folder())

def delete_directory(directory_path):
    path = Path(directory_path)

    if path.exists():
        shutil.rmtree(directory_path)
        print(f"Тека '{directory_path}' успішно видалена\n")
    else:
        print(f"Тека '{directory_path}' не існує\n")


# Очищення теки
delete_directory('/home/oleksanlr/Стільниця/Програма')
Path('/home/oleksanlr/Стільниця/Програма').mkdir()


# симуляція вказаного шляху до теки зберігання
save_folder_path = '/home/oleksanlr/Стільниця/Програма'
# симуляція вибору моду в вікні програми
Process.run(mod='/home/oleksanlr/.local/share/Steam/steamapps/workshop/content/294100/1888705256')
