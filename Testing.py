from pathlib import Path

# Клас модифікації
class Mod:
    NameIsSet = False
    AuthorIsSet = False

    def __init__(self, path=None):
        self.__Path = path
        self.__PackageId = path.name
        self.__Name = None
        self.__Author = None
        self.__SupportedVersion = None
        try:
            with open(path/'About'/'About.xml', 'r', encoding='utf-8') as file:
                for i in file.readlines():
                    i = i.strip()
                    if (i.startswith('<name>') and i.endswith('</name>')) or (i.startswith('<displayName>') and i.endswith('</displayName>') and (self.NameIsSet is False)):
                        self.__Name = self.__get_name(i)
                        self.NameIsSet = True
                        continue
                    if i.startswith('<author>') and i.endswith('</author>') and self.NameIsSet is False:
                        self.__Author = self.__get_author(i)
                        continue
                    if i.startswith('</supportedVersions>'):
                        self.__SupportedVersion = self.__get_supported_version(i)
                        continue
        except FileNotFoundError:
            print('Помилка функції')

    @staticmethod
    def __get_name(i):
        name = i.replace('<displayName>', '').replace('</displayName>', '').replace('<name>', '').replace('</name>', '')
        return name

    @staticmethod
    def __get_author(i):
        is_name = False
        a = str()
        if i.startswith('</authors>'):
            self.AuthorIsSet = True
            return a.removesuffix(', ')
        if i.startswith('<authors>'):
            is_name = True
            continue
        elif is_name is True:
            i = i.replace('<li>', '').replace('</li>', '')
            a += i + ', '
        author = i.replace('<author>', '').replace('</author>', '')


    @staticmethod
    def __get_supported_version( i):
        is_version = False
        a = str()
        if i.startswith('</supportedVersions>'):
            return a.removesuffix(' ')
        if i.startswith('<supportedVersions>'):
            is_version = True
        elif is_version is True:
            i = i.replace('<li>', '').replace('</li>', '')
            a += i + ' '

    def return_atribute(self):
        return 'Шлях -', self.__Path, 'Ід -', self.__PackageId, 'Назва -', self.__Name, 'Автор  -', self.__Author, 'Версії -', self.__SupportedVersion

'''
is_version = False
a = str()
if i.startswith('</supportedVersions>'):
    return a.removesuffix(' ')
if i.startswith('<supportedVersions>'):
    is_version = True
    continue
elif is_version is True:
    i = i.replace('<li>', '').replace('</li>', '')
    a += i + ' '

'''

'''
is_name = False
a = str()
if i.startswith('</authors>'):
    return a.removesuffix(', ')
if i.startswith('<authors>'):
    is_name = True
    continue
elif is_name is True:
    i = i.replace('<li>', '').replace('</li>', '')
    a += i + ', '
'''
# Функція отримання істинного шляху до теки модів гри.
# Знаходить шлях незалежно від місця розташування теки.
# Зробити: Виправити впадання в нескінченну рекурсію пошуку, якщо файл не знайдено. Запитувати шлях, перевіряти його.
def find_mod_folder():
    for path in Path('/').rglob('Steam/steamapps/workshop/content/294100'):
        if path.is_dir():
            return path.resolve()


Mod = Mod(path=find_mod_folder()/'3237638097')
print(Mod.return_atribute())

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

        mods.append(Mod(packageid=subdirs[i],
                        path=path,
                        name=get_mod_name(path=path_to_about),
                        author=get_mod_author(path=path_to_about),
                        supported_versions=get_supported_version(path=path_to_about),
                        published_file_id=path.name
                        )
                    )
    return mods
