from pathlib import Path
import xml.etree.ElementTree as ET
# import Main


# Клас модифікації
class Mod:
    def __init__(self, root_path=None, package_id=None, name=None, author=None, supported_version=None):
        self.__RootPath = root_path
        self.__PackageId = package_id
        self.__Name = name
        self.__Author = author
        self.__SupportedVersion = supported_version

    def get_attribute(self, attribute_name):
        if attribute_name == 'RootPath':
            return self.__RootPath
        elif attribute_name == 'PackageId':
            return self.__PackageId
        elif attribute_name == 'Name':
            return self.__Name
        elif attribute_name == 'Author':
            return self.__Author
        elif attribute_name == 'SupportedVersion':
            return self.__SupportedVersion
        elif attribute_name == 'All':
            return  self.__RootPath, self.__PackageId, self.__Name, self.__Author, self.__SupportedVersion
        else:
            raise AttributeError(f'Атрибут "{attribute_name}" не вірний')


# Функція отримання істинного шляху до теки модів гри.
# Знаходить шлях незалежно від місця розташування теки.
# Зробити: Виправити впадання в нескінченну рекурсію пошуку, якщо файл не знайдено. Запитувати шлях, перевіряти його.
def search_294100_folder():
    for path in Path('/').rglob('Steam/steamapps/workshop/content/294100'):
        return path.resolve()


def get_attributes(element, path=None, id=None):
    attributes = {'Path': None,
                  'Id': None,
                  'Name': None,
                  'Author': None,
                  'PackageID': None}
    attributes['Path'] = path
    attributes['Id'] = id
    for child in element:
        if child.tag == 'name':
            if child.text:
                attributes['Name'] = child.text.strip()
        elif child.tag == 'author':
            if child.text:
                attributes['Author'] = child.text.strip()
        elif child.tag == 'authors':
            if child.text:
                authors = str()
                for author in child.findall('li'):
                    authors += author.text + ', '
                authors = authors[:-2]
                attributes['Author'] = authors
        elif child.tag == 'packageId':
            if child.text:
                attributes['PackageId'] = child.text.strip()
        else:
            get_attributes(child)
    return attributes


# Функція ініціалізації об'єкта класу Mod. Повертає список об'єктів.
def create_mod_list(path_294100):
    mods = list()
    for i in path_294100.iterdir():
        tree = ET.parse(i/'About/About.xml')
        root = tree.getroot()
        attributes = get_attributes(element=root, path=i, id=i.name)
        mods.append(Mod(root_path=attributes['Path'],
                        name=attributes['Name'],
                        author=attributes['Author'],
                        package_id=attributes['PackageId']))
    return mods
