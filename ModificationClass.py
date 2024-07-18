from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Union, Tuple, Callable, Optional, Any


# Клас модифікації
class Mod:
    def __init__(self, root_path, package_id, name, author, supported_version, published_file_id):

        self.root_path = root_path
        self.package_id = package_id
        self.name = name
        self.author = author
        self.supported_version = supported_version
        self.published_file_Id = published_file_id

    def get_attribute(self, attribute):
        if attribute == 'RootPath':
            return self.root_path
        elif attribute == 'PackageId':
            return self.package_id
        elif attribute == 'Name':
            return self.name
        elif attribute == 'Author':
            return self.author
        elif attribute == 'SupportedVersion':
            return self.supported_version
        elif attribute == 'PublishedFileId':
            return self.published_file_Id
        elif attribute == 'All':
            return self.root_path, self.package_id, self.name, self.author, self.supported_version
        else:
            raise AttributeError(f'Атрибут "{attribute}" не вірний')

    def set_attribute(self, attribute: str, value: Union[str, Path]):
        if attribute == 'RootPath':
            if attribute is Path:
                self.root_path = value
            else:
                raise AttributeError(f'Значення "{value}" не вірний')
        elif attribute == 'PackageId':
            self.package_id = value
        elif attribute == 'Name':
            self.name = value
        elif attribute == 'Author':
            self.author = value
        elif attribute == 'SupportedVersion':
            self.supported_version = value
        elif attribute == 'PublishedFileId':
            self.published_file_Id = value


# Функція отримання істинного шляху до теки модів гри.
# Знаходить шлях незалежно від місця розташування теки.
# Зробити: Виправити впадання в нескінченну рекурсію пошуку, якщо файл не знайдено. Запитувати шлях, перевіряти його.
def search_294100_folder():
    volumes = ['/', 'A:', 'B:', 'C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:',]

    for volume in volumes:
        for path in Path(volume).rglob('Steam/steamapps/workshop/content/294100'):
            return path.resolve()


def get_attributes(element, path=None, test=None):
    attributes = dict()
    attributes['Path'] = path
    attributes['Id'] = test
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
        attributes = get_attributes(element=root, path=i, test=i.name)
        mods.append(Mod(root_path=attributes['Path'],
                        name=attributes['Name'],
                        author=attributes['Author'],
                        package_id=attributes['PackageId']))
    return mods


mod_object_list = create_mod_list(path_294100=search_294100_folder())
for mod in mod_object_list:
    print(mod)
