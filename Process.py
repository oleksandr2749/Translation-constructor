from pathlib import Path
import shutil
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
        for defName in i.iter('defName'):
            pass
        for a in i.iter('label'):
            ET.SubElement(root, defName.text + '.label').text = a.text
        for a in i.iter('description'):
            ET.SubElement(root, defName.text + '.description').text = a.text
        ET.indent(root, level=0)
    return root


def process(file):
    mod_data = get_data(file)

    root = data_process(mod_data)
    tree = ET.ElementTree(root)
    save_path = Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian/DefInjected').joinpath(mod_data[0].tag)
    if not save_path.exists():
        save_path.mkdir()
    tree.write(file_or_filename=save_path.joinpath(file.name), encoding='utf-8', xml_declaration=True)


def get_all_defxml_path(path_to_defdir):
    defxml_path_list = list()
    for element in path_to_defdir.iterdir():
        if element.is_file():
            defxml_path_list.append(element)
        else:
            defxml_path_list.extend(get_all_defxml_path(element))
    return defxml_path_list


# Функція виконання
def run(modification):
    # словник шляхів тек моду перекладу
    mod_folder_paths = {'languages': Path('/home/oleksanlr/Стільниця/Програма/Languages'),
                'ukrainian': Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian'),
                'definjected': Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian/DefInjected'),
                'keyed': Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian/Keyed')}

    # Створення базових тек моду перекладу
    for i in mod_folder_paths.values():
        i.mkdir()

    defxml_path_list = get_all_defxml_path(path_to_defdir=Path(modification).joinpath('1.5/Defs'))

    for defxml in defxml_path_list:
        # print(defxml)
        process(file=defxml)


def delete_directory(directory_path):
    path = Path(directory_path)

    if path.exists():
        shutil.rmtree(directory_path)
        print(f"Тека '{directory_path}' успішно видалена\n")
    else:
        print(f"Тека '{directory_path}' не існує\n")


# Очищення теки
delete_directory('/home/oleksanlr/Стільниця/Програма')
Path('/home/oleksanlr/Стільниця/Програма').mkdir()

run(modification='/home/oleksanlr/.steam/steam/steamapps/workshop/content/294100/3202046258')
