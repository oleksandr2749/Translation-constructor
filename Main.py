# from UI import App
import os
from pathlib import Path


def get_data_from_file(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.readlines()
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
