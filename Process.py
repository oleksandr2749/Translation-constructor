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


def get_data(file):
    tree = ET.parse(file)
    root = tree.getroot()
    data = list()

    for tag in root:
        if tag.find('label') is not None or tag.find('description') is not None:
            data.append(tag)
    return data


def data_process(data):
    root = ET.Element('LanguageData')
    for i in data:
        # defName = 'RWTC: ПОМИЛКА ОТРИМАННЯ defName'
        for defName_element in i.iter('defName'):
            defName = defName_element
            '''print('Тип - ', type(defName))
            print('Тег - ', defName.tag)
            print('Текст - ', defName.text)'''
        for a in i.iter('label'):
            root.append(ET.Comment(a.text))
            ET.SubElement(root, defName.text + '.label').text = a.text
        for a in i.iter('description'):
            try:
                root.append(ET.Comment(a.text))
                ET.SubElement(root, defName.text + '.description').text = a.text
            except:
                root.append(ET.Comment('RWTC:ПОМИЛКА ОТРИМАННЯ defName. ЕЛЕМЕНТ ПРОПУЩЕНО'))
    ET.indent(root, level=0)
    return root


def process(file, def_path):
    mod_data = get_data(file)
    if not mod_data:
        return

    # print(file.name)
    root = data_process(mod_data)
    tree = ET.ElementTree(root)
    save_path = Path(def_path).joinpath(mod_data[0].tag)
    save_path.mkdir(exist_ok=True)
    tree.write(file_or_filename=save_path.joinpath(file.name), encoding='utf-8', xml_declaration=True)


def get_keyed_data(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root


def keyed_data_process(data):
    root = ET.Element('LanguageData')
    for element in data:
        root.append(ET.Comment(element.text))
        ET.SubElement(root, element.tag).text = element.text
    ET.indent(root, level=0)
    return root


def keyed_process(file, xml_path):
    root = keyed_data_process(get_keyed_data(file))
    tree = ET.ElementTree(root)
    tree.write(file_or_filename=xml_path.joinpath(file.name), encoding='utf-8', xml_declaration=True)


def get_all_defxml_path(path_to_defdir):
    defxml_path_list = list()
    for element in path_to_defdir.iterdir():
        if element.is_file():
            defxml_path_list.append(element)
        else:
            defxml_path_list.extend(get_all_defxml_path(element))
    return defxml_path_list


def get_all_keyed_path(path_to_keyed):
    keyedxml_path_list = list()
    for element in path_to_keyed.iterdir():
        if element.is_file():
            keyedxml_path_list.append(element)
        else:
            keyedxml_path_list.extend(get_all_defxml_path(element))
    return keyedxml_path_list


# Функція виконання
def run(modification, save_path):
    print(f'змінна save_path типу {type(save_path)} = {save_path}')
    # словник шляхів тек моду перекладу
    mod_folder_paths = dict()
    mod_folder_paths['folder'] = save_path/modification.get_attribute('Name')
    mod_folder_paths['languages'] = mod_folder_paths['folder']/'Languages'
    mod_folder_paths['ukrainian'] = mod_folder_paths['languages']/'Ukrainian'
    mod_folder_paths['definjected'] = mod_folder_paths['ukrainian']/'DefInjected'
    mod_folder_paths['keyed'] = mod_folder_paths['ukrainian']/'Keyed'

    for i in mod_folder_paths:
        print(f'елемент словника mod_folder_paths {i} типу {type(mod_folder_paths[i])} = {mod_folder_paths[i]}')

    # Створення базових тек моду перекладу
    mod_folder_paths['folder'].mkdir(exist_ok=True)
    mod_folder_paths['languages'].mkdir(exist_ok=True)
    mod_folder_paths['ukrainian'].mkdir(exist_ok=True)

    print(modification.get_attribute('RootPath')/'1.5/Defs')
    if (modification.get_attribute('RootPath')/'1.5/Defs').exists():
        defxml_path_list = get_all_defxml_path(path_to_defdir=modification.get_attribute('RootPath')/'1.5/Defs')
        mod_folder_paths['definjected'].mkdir()
        for defxml in defxml_path_list:
            process(file=defxml, def_path=mod_folder_paths['definjected'])
    if (modification.get_attribute('RootPath')/'Languages/English/Keyed').exists():
        keyed_path_list = get_all_keyed_path(path_to_keyed=modification.get_attribute('RootPath')/'Languages/English/Keyed')
        mod_folder_paths['keyed'].mkdir()
        for keyedxml in keyed_path_list:
            keyed_process(file=keyedxml, xml_path=mod_folder_paths['keyed'])
