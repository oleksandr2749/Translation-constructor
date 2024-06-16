from pathlib import Path

# Клас модифікації
class Mod:
    def __init__(self, packageid=None, path=None, name=None, author=None, supported_versions=None, published_file_id=None):
        self.__PackageId = packageid
        self.__Path = path
        self.__Name = name
        self.__Author = author
        self.__SupportedVersions = supported_versions
        self.__PublishedFileId = published_file_id

    def return_atribute(self):
        return self.__PackageId, self.__Path, self.__Name, self.__Author, self.__SupportedVersions, self.__PublishedFileId


# Функція отримання істинного шляху до теки модів гри.
# Знаходить шлях незалежно від місця розташування теки.
# Зробити: Виправити впадання в нескінченну рекурсію пошуку, якщо файл не знайдено. Запитувати шлях, перевіряти його.
def find_mod_folder():
    for path in Path('/').rglob('Steam/steamapps/workshop/content/294100'):
        if path.is_dir():
            return path.resolve()


def get_mod_name(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for i in file.readlines():
                if '<displayName>' in i or '<name>' in i:
                    i = i.strip().replace('<displayName>', '').replace('</displayName>', '').replace('<name>', '').replace('</name>', '')
                    return i
    except FileNotFoundError:
        print('Помилка функції write_to_file')
        return None


def get_mod_author(path):
    is_name = False
    a = str()
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for i in file.readlines():
                i = i.strip()
                if i.startswith('<author>') and i.endswith('</author>'):
                    i = i.replace('<author>', '').replace('</author>', '')
                    return i
                if i.startswith('</authors>'):
                    return a.removesuffix(', ')
                if i.startswith('<authors>'):
                    is_name = True
                    continue
                elif is_name is True:
                    i = i.replace('<li>', '').replace('</li>', '')
                    a += i + ', '
    except FileNotFoundError:
        print('Помилка функції write_to_file')
        return None


def get_supported_version(path):
    is_version = False
    a = str()
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for i in file.readlines():
                i = i.strip()
                if i.startswith('</supportedVersions>'):
                    return a.removesuffix(' ')
                if i.startswith('<supportedVersions>'):
                    is_version = True
                    continue
                elif is_version is True:
                    i = i.replace('<li>', '').replace('</li>', '')
                    a += i + ' '
    except FileNotFoundError:
        print('Помилка функції write_to_file')
        return None

# Функція ініціалізації об'єкта класу Mod з всіма атрибутами. Повертає кортеж об'єктів.
def create_mod_list():
    path_to_mod_folder = find_mod_folder()

    subdirs = list()
    for i in path_to_mod_folder.iterdir():
        if i.is_dir():
            subdirs.append(i.name)

    mods = list()
    for i in range(len(subdirs)):
        path = path_to_mod_folder/subdirs[i]
        path_to_about = path/'About'/'About.xml'
        mods.append(Mod(packageid=subdirs[i],
                        path=path,
                        name=get_mod_name(path=path_to_about),
                        author=get_mod_author(path=path_to_about),
                        supported_versions=get_supported_version(path=path_to_about),
                        published_file_id=path.name
                        )
                    )
    return mods


mod_list = create_mod_list()
print()
for i in range(len(mod_list)):
    print('Об\'єкт', i, mod_list[i].return_atribute())
