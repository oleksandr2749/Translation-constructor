from pathlib import Path
import xml.etree.ElementTree as ET


def get_data():
    tree = ET.parse('/home/oleksanlr/.steam/steam/steamapps/workshop/content/294100/3202046258/1.5/Defs/ThingDefs_Buildings/Buildings_Temperature.xml')
    root = tree.getroot()
    return get_data_process(root)


def get_data_process(element):
    data = list()
    for testDef in element:
        data.append(testDef)
    return data


def data_process(data):
    root = ET.Element('LanguageData')
    for i in data:
        for defName in i.iter('defName'):
            pass
        for a in i.iter('label'):
            ET.Comment(a.text)
            ET.SubElement(root, defName.text + '.label').text = a.text
        for a in i.iter('description'):
            ET.SubElement(root, defName.text + '.description').text = a.text
        ET.indent(root, level=0)
    return root


print(get_data())
root = data_process(get_data())
print(ET.tostring(root, encoding='utf8').decode('utf8'))
tree = ET.ElementTree(root)
tree.write('test.xml', encoding='utf-8', xml_declaration=True)


# Функція виконання
def run():
    # словник шляхів тек моду перекладу
    mod_folder_paths = {'languages': Path('/home/oleksanlr/Стільниця/Програма/Languages'),
                'ukrainian': Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian'),
                'definjected': Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian/DefInjected'),
                'keyed': Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian/Keyed')}

    # Створення базових тек моду перекладу
    for i in mod_folder_paths.values():
        i.mkdir()

    '''
    # отримання всіх файлів моду
    def_file_list = process(mod_folder)
    # створення теки, створення файлу, запис у файл, визначення типу файлу
    for i in def_file_list:
        if not paths['definjected'].joinpath(file_type_check(i)).exists():
            paths['definjected'].joinpath(file_type_check(i)).mkdir()
        write_to_file(str(paths['definjected'].joinpath(file_type_check(i)).joinpath(i.name)),
                      data=get_filtered_data(get_data_from_file(i)))
    '''


run()
