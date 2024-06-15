# from UI import App
import os
from pathlib import Path


def get_data_from_file(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            return content
    except FileNotFoundError:
        print('Помилка функції get_data_from_file')
        return None


# Функція створення списку відфільтрованих даних отриманих від get_data_from_file
def get_filtered_data(obtained_data):
    data_strip = list()
    data = list()
    words_to_remove = ['<defName>', '</defName>', '<label>', '</label>', '<description>', '</description>']
    # Цикл видалення пробілів, табуляцій, переходів
    for i in obtained_data:
        data_strip.append(i.strip())
    #
    for i in data_strip:
        if '<defName>' in i or '<label>' in i or '<description>' in i:
            if '<label>point</label>' not in i and '<label>edge</label>' not in i:
                if '<defName>' in i:
                    def_name = i
                    for word in words_to_remove:
                        def_name = def_name.replace(word, "")
                if '<label>' in i:
                    label = i
                    for word in words_to_remove:
                        label = label.replace(word, "")
                    data.append('\n  ' + '<!--' + label + '-->' + '\n  <' + def_name + '.label>' + label + '</' + def_name + '.label>')
                if '<description>' in i:
                    description = i
                    for word in words_to_remove:
                        description = description.replace(word, "")
                    data.append('\n  ' + '<!--' + description + '-->' + '\n  <' + def_name + '.description>' + description + '</' + def_name + '.description>')
    return data


def write_to_file(path: str, data: list):
    try:
        with open(path, 'w+', encoding='utf-8') as file:
            file.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<LanguageData>')
            for i in data:
                file.write(i)
            file.write('\n</LanguageData>\n')
    except FileNotFoundError:
        print('Помилка функції write_to_file')
        return None


def run():
    # input_path_to_mod_file = (input('Вкажіть шлях до файлу моду: '))
    input_path_to_mod_file = 'Buildings_Temperature.xml'
    # input_path_to_translation_file = (input('Вкажіть шлях до файлу перекладу: '))
    input_path_to_translation_file = 'Test.xml'
    write_to_file(path=input_path_to_translation_file, data=get_filtered_data(get_data_from_file(path=input_path_to_mod_file)))


# run()

class Mod:
    def __init__(self, path=None, name=None, author=None, supported_versions=None, package_id=None, published_file_id=None):
        self.__Path = path
        self.__Name = name
        self.__Author = author
        self.__SupportedVersions = supported_versions
        self.__PackageId = package_id
        self.__PublishedFileId = published_file_id

    def return_atribute(self):
        return self.__Path, self.__Name, self.__Author, self.__SupportedVersions, self.__PackageId, self.__PublishedFileId


def find_mod_folder():
    for path in Path('/').rglob('Steam/steamapps/workshop/content/294100'):
        if path.is_dir():
            return path.resolve()


def get_path_to_mod(path_to_mod_folder):
    pass


def create_mod_list():
    path_to_mod_folder = find_mod_folder()

    subdirs = list()
    for i in path_to_mod_folder.iterdir():
        if i.is_dir():
            subdirs.append(i.name)

    mods = list()
    for i in range(len(subdirs)):
        mods.append(Mod(path=subdirs[i]))
    return mods


mod_list = create_mod_list()
print()
for i in range(len(mod_list)):
    print('Обє\'кт', i, mod_list[i].return_atribute())
