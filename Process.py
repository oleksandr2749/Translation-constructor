from pathlib import Path
import shutil


# функція повернення даних з файлу у вигляді списку рядків
def get_data_from_file(path):
    try:
        with open(path.absolute(), 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f'Помилка виконання функції get_data_from_file! Не коректний шлях {path}')
        return None


# Функція створення списку відфільтрованих даних отриманих від get_data_from_file
# Потребує вдосконалення: спрощення
def get_filtered_data(obtained_data):
    data_strip = list()
    data = list()
    words_to_remove = ['<defName>', '</defName>', '<label>', '</label>', '<description>', '</description>']
    # Цикл видалення пробілів, табуляцій, переходів
    for i in obtained_data:
        data_strip.append(i.strip())
    # Цикл фільтрування та формування готових рядків назв, описів
    # та коментарів над ними, що містять оригінальний текст рядка
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


# Функція створення та запису даних у файл
def write_to_file(path: str, data: list):
    try:
        with open(path, 'w+', encoding='utf-8') as file:
            # Запис першого рядка
            file.write('<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<LanguageData>')
            # Цикл запису рядків зі списку
            for i in data:
                file.write(i)
            # Запис останнього рядка
            file.write('\n</LanguageData>\n')
    except FileNotFoundError:
        print(f'Помилка виконання функції write_to_file! Не коректний шлях {path}')
        return None


# Функція виконання
def run(test1=None):
    path_to_defs_folder = Path(test1)

    path_to_languages_f = Path('/home/oleksanlr/Стільниця/Програма/Languages')
    path_to_ukrainian_f = Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian')
    path_to_definjected_f = Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian/DefInjected')
    path_to_keyed_f = Path('/home/oleksanlr/Стільниця/Програма/Languages/Ukrainian/Keyed')
    path_to_languages_f.mkdir()
    path_to_ukrainian_f.mkdir()
    path_to_definjected_f.mkdir()
    path_to_keyed_f.mkdir()
    paths = {'languages': path_to_languages_f, 'ukrainian': path_to_ukrainian_f, 'definjected': path_to_definjected_f,
             'keyed': path_to_keyed_f}

    # отримання всіх файлів моду
    def_file_list = process(path_to_defs_folder)
    # створення теки, створення файлу, запис у файл, визначення типу файлу
    for i in def_file_list:
        if not paths['definjected'].joinpath(test2(i)).exists():
            paths['definjected'].joinpath(test2(i)).mkdir()
        write_to_file(str(paths['definjected'].joinpath(test2(i)).joinpath(i.name)), data=get_filtered_data(get_data_from_file(i)))


def path_to_folder():
    pass


def test2(file):
    data = get_data_from_file(file)
    file_type = str()
    for i in data:
        if 'ThingDef' in i:
            file_type = 'ThingDef'
            break
    return file_type


def process(path_to_defs):
    test = list()
    for i in list(path_to_defs.iterdir()):
        if i.is_file():
            if 'ThingDef' == test2(i):
                test.append(i)
        elif i.is_dir():
            test.extend(process(i))
    return test


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

run(test1='/home/oleksanlr/.local/share/Steam/steamapps/workshop/content/294100/1888705256/1.5/Defs')
