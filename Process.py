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

import logging
from pathlib import Path
import xml.etree.ElementTree as ET


def read_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root


def def_process(mod_data):
    root = ET.Element('LanguageData')
    def_name = None
    for element in mod_data.iter():
        if element.tag == 'defName':
            def_name = element
            continue
        if def_name is not None:
            if element.tag == 'label':
                root.append(ET.Comment(element.text))
                ET.SubElement(root, def_name.text + '.label').text = element.text
            elif element.tag == 'description':
                root.append(ET.Comment(element.text))
                ET.SubElement(root, def_name.text + '.description').text = element.text

    ET.indent(root, level=0)

    if len(root) == 0:
        return None
    else:
        return root


def xml_file_write(data, path, name):
    tree = ET.ElementTree(data)
    if not path.exists():
        path.mkdir()
    tree.write(file_or_filename=path / name, encoding='utf-8', xml_declaration=True)


def get_all_defxml_path(path_to_defdir):
    defxml_path_list = list()
    for element in path_to_defdir.iterdir():
        if element.is_file():
            defxml_path_list.append(element)
        else:
            defxml_path_list.extend(get_all_defxml_path(element))
    return defxml_path_list


# Функція виконання
def run(modification, export_path):
    logging.info('Розпочато обробку для %s', modification.get_attribute('Name'))
    # Словник шляхів тек моду перекладу
    mod_folder_paths = dict()
    mod_folder_paths['root'] = export_path / modification.get_attribute('Name')
    mod_folder_paths['languages'] = mod_folder_paths['root']/'Languages'
    mod_folder_paths['ukrainian'] = mod_folder_paths['languages']/'Ukrainian'
    mod_folder_paths['definjected'] = mod_folder_paths['ukrainian']/'DefInjected'
    mod_folder_paths['keyed'] = mod_folder_paths['ukrainian']/'Keyed'

    folder_to_create = (mod_folder_paths['root'], mod_folder_paths['languages'], mod_folder_paths['ukrainian'])

    # Створення базових тек моду перекладу
    logging.info('Розпочато створення базових тек моду перекладу в %s', export_path)
    for folder in folder_to_create:
        try:
            folder.mkdir()
        except FileExistsError:
            logging.warning('Тека %s вже існує', folder.name)
        except Exception:
            logging.error('Не вдалось створити теку %s', folder.name, exc_info=True)
        else:
            logging.info('Створено теку %s', folder.name)

    # Процес отримання Defs
    logging.info('Розпочато процес отримання Defs')
    defs_to_find = (modification.get_attribute('RootPath')/'1.5/Defs', modification.get_attribute('RootPath')/'Defs')

    found = False
    for defs_fonder in defs_to_find:
        if defs_fonder.exists():
            found = True
            defxml_path_list = get_all_defxml_path(path_to_defdir=defs_fonder)
            mod_folder_paths['definjected'].mkdir(exist_ok=True)
            for defxml in defxml_path_list:
                # print(defxml.name)
                def_data = read_xml(file=defxml)
                def_process_data = def_process(mod_data=def_data)

                if def_process_data is None:
                    continue
                else:
                    xml_file_write(data=def_process_data, path=mod_folder_paths['definjected'] / Path(def_data[0].tag),
                                   name=defxml.name[0:-4] + '_' + modification.get_attribute('PackageId') + '.xml')
    if found is True:
        pass
    if found is False:
        logging.error('Не знайдено теку Defs. Викликано функцію сповіщення!')

    # Процес отримання Keyed
    if (modification.get_attribute('RootPath')/'Languages/English/Keyed').exists():
        for file in Path(modification.get_attribute('RootPath')/'Languages/English/Keyed').iterdir():
            data = read_xml(file)

            root = ET.Element('LanguageData')
            for element in data:
                root.append(ET.Comment(element.text))
                root.append(element)
            ET.indent(root, level=0)

            xml_file_write(data=root, path=mod_folder_paths['keyed'],
                           name=file.name[0:-4] + '_' + modification.get_attribute('PackageId') + '.xml')
