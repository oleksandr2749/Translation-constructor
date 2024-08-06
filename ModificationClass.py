# This file is part of Translation Constructor.
#
# Translation Constructor is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Translation Constructor is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with Translation Constructor. If not,
# see <https://www.gnu.org/licenses/>.

from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Union, Tuple, Callable, Optional, Any


# Клас модифікації
class Mod:
    def __init__(self, root_path, package_id, name, author, supported_versions, published_file_id):

        self.root_path = root_path
        self.package_id = package_id
        self.name = name
        self.author = author
        self.supported_version = supported_versions
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


# Функція ініціалізації об'єкта класу Mod. Повертає список об'єктів.
def create_mod_list(path_294100):
    mods = list()
    for i in path_294100.iterdir():
        tree = ET.parse(i/'About/About.xml')
        root = tree.getroot()
        mod_data = {
            'root_path': i,
            'published_file_id': i.name
        }
        for child in root:
            if child.tag == 'name':
                mod_data['name'] = child.text
            elif child.tag == 'author':
                mod_data['author'] = child.text
            elif child.tag == 'authors':
                authors = str()
                for author in child.findall('li'):
                    authors += author.text + ', '
                authors = authors[:-2]
                mod_data['author'] = authors
            elif child.tag == 'supportedVersions':
                sv = str()
                for test in child.findall('li'):
                    sv += test.text + ', '
                sv = sv[:-2]
                mod_data['supported_versions'] = sv
            elif child.tag == 'packageId':
                mod_data['package_id'] = child.text

        mods.append(Mod(**mod_data))
    return mods
