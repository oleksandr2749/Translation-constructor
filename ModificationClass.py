from pathlib import Path

# Клас модифікації
class Mod:
    def __init__(self, path=None, name=None, author=None, supported_versions=None, package_id=None, published_file_id=None):
        self.__Path = path
        self.__Name = name
        self.__Author = author
        self.__SupportedVersions = supported_versions
        self.__PackageId = package_id
        self.__PublishedFileId = published_file_id

    def return_atribute(self):
        return self.__Path, self.__Name, self.__Author, self.__SupportedVersions, self.__PackageId, self.__PublishedFileId


# Функція отримання істинного шляху до теки модів гри.
# Знаходить шлях незалежно від місця розташування теки.
# Зробити: Виправити впадання в нескінченну рекурсію пошуку, якщо файл не знайдено. Запитувати шлях, перевіряти його.
def find_mod_folder():
    for path in Path('/').rglob('Steam/steamapps/workshop/content/294100'):
        if path.is_dir():
            return path.resolve()


def get_path_to_mod(path_to_mod_folder):
    pass


# Функція ініціалізації об'єкта класу Mod з всіма атрибутами. Повертає кортеж об'єктів.
def create_mod_list():
    path_to_mod_folder = find_mod_folder()

    subdirs = list()
    for i in path_to_mod_folder.iterdir():
        if i.is_dir():
            subdirs.append(i.name)

    mods = list()
    for i in range(len(subdirs)):
        mods.append(Mod(path=subdirs[i]))
    return mods


mod_list = create_mod_list()
print()
for i in range(len(mod_list)):
    print('Об\'єкт', i, mod_list[i].return_atribute())
