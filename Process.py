from pathlib import Path
import xml.etree.ElementTree as ET


def get_data(file):
    tree = ET.parse(file)
    root = tree.getroot()
    data = list()

    for tag in root:
        if tag.find('label') is not None or tag.find('description') is not None:
            data.append(tag)
    if not data:
        raise Exception('Помилка витягування')
    return data


def data_process(data):
    root = ET.Element('LanguageData')
    for i in data:
        for defName in i.iter('defName'):
            pass
        for a in i.iter('label'):
            root.append(ET.Comment(a.text))
            ET.SubElement(root, defName.text + '.label').text = a.text
        for a in i.iter('description'):
            root.append(ET.Comment(a.text))
            ET.SubElement(root, defName.text + '.description').text = a.text
    ET.indent(root, level=0)
    return root


def process(file, def_path):
    mod_data = get_data(file)

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
def run(modification, mod_name):
    # словник шляхів тек моду перекладу
    mod_folder_paths = {'folder': Path('/home/oleksanlr/Стільниця/Програма').joinpath(mod_name),
                        'languages': Path('/home/oleksanlr/Стільниця/Програма').joinpath(mod_name, 'Languages'),
                        'ukrainian': Path('/home/oleksanlr/Стільниця/Програма').joinpath(mod_name, 'Languages//Ukrainian'),
                        'definjected': Path('/home/oleksanlr/Стільниця/Програма').joinpath(mod_name, 'Languages/Ukrainian/DefInjected'),
                        'keyed': Path('/home/oleksanlr/Стільниця/Програма').joinpath(mod_name, 'Languages/Ukrainian/Keyed')}

    # Створення базових тек моду перекладу
    mod_folder_paths['folder'].mkdir(exist_ok=True)
    mod_folder_paths['languages'].mkdir(exist_ok=True)
    mod_folder_paths['ukrainian'].mkdir(exist_ok=True)

    if modification.joinpath('1.5/Defs').exists():
        defxml_path_list = get_all_defxml_path(path_to_defdir=modification.joinpath('1.5/Defs'))
        if defxml_path_list:
            mod_folder_paths['definjected'].mkdir()
            for defxml in defxml_path_list:
                process(file=defxml, def_path=mod_folder_paths['definjected'])
    if modification.joinpath('Languages/English/Keyed').exists():
        keyed_path_list = get_all_keyed_path(path_to_keyed=modification.joinpath('Languages/English/Keyed'))
        if keyed_path_list:
            mod_folder_paths['keyed'].mkdir()
            for keyedxml in keyed_path_list:
                keyed_process(file=keyedxml, xml_path=mod_folder_paths['keyed'])
