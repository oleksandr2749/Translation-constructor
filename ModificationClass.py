from pathlib import Path


# Клас модифікації
class Mod:
    def __init__(self, path=None):
        self.__Path = path
        self.__PackageId = path.name
        self.__Name = str()
        self.__Author = str()
        self.__SupportedVersion = str()
        try:
            with open(path/'About'/'About.xml', 'r', encoding='utf-8') as file:
                name_is_set = False
                author_is_set = False
                is_author_str = False
                supported_version_is_set = False
                is_supported_version_str = False
                for i in file.readlines():
                    i = i.strip()
                    if (i.startswith('<name>') and i.endswith('</name>')) or (i.startswith('<displayName>') and i.endswith('</displayName>') and (name_is_set is False)):
                        self.__Name = i.replace('<displayName>', '').replace('</displayName>', '').replace('<name>', '').replace('</name>', '')
                        name_is_set = True
                        continue

                    if author_is_set is False:
                        if i.startswith('<author>') and i.endswith('</author>'):
                            self.__Author = i.replace('<author>', '').replace('</author>', '')
                            author_is_set = True
                            continue

                        if i.startswith('<authors>'):
                            is_author_str = True
                            continue
                        elif i.endswith('</authors>'):
                            self.__Author = self.__Author.removesuffix(', ')
                            author_is_set = True
                            is_author_str = False
                            continue
                        elif is_author_str is True:
                            self.__Author += i.replace('<li>', '').replace('</li>', '') + ', '
                            continue

                    if supported_version_is_set is False:
                        if i.startswith('<supportedVersions>'):
                            is_supported_version_str = True
                            continue
                        elif i.endswith('</supportedVersions>'):
                            self.__SupportedVersion = self.__SupportedVersion.removesuffix(' ')
                            supported_version_is_set = True
                            is_supported_version_str = False
                            continue
                        elif is_supported_version_str is True:
                            self.__SupportedVersion += i.replace('<li>', '').replace('</li>', '') + ' '
                            continue
        except FileNotFoundError:
            print('Помилка функції')

    def get_atribute(self):
        return 'Шлях -', self.__Path, 'Ід -', self.__PackageId, 'Назва -', self.__Name, 'Автор  -', self.__Author, 'Версії -', self.__SupportedVersion

    def get_name(self):
        return self.__Name

    def get_path(self):
        return self.__Path


# Функція отримання істинного шляху до теки модів гри.
# Знаходить шлях незалежно від місця розташування теки.
# Зробити: Виправити впадання в нескінченну рекурсію пошуку, якщо файл не знайдено. Запитувати шлях, перевіряти його.
def find_mod_folder():
    for path in Path('/').rglob('Steam/steamapps/workshop/content/294100'):
        if path.is_dir():
            return path.resolve()


# Функція ініціалізації об'єкта класу Mod. Повертає список об'єктів.
def create_mod_object_list():
    path_to_mod_folder = find_mod_folder()
    mods = list()

    for i in path_to_mod_folder.iterdir():
        if i.is_dir():
            mods.append(Mod(path=i))
    return mods
