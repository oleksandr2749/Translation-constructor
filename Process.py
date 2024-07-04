from pathlib import Path


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


def run(path_to_mod=None):
    path_to_mod = Path(path_to_mod)
    path_for_folder_creation = Path('C:/Users/Олександр/Desktop/Тека файлів перекладу')
    # path_for_folder_creation.mkdir()
    # file_from_dir = get_file_from_dir(path_to_mod)
    # print(test2[1])

    for x in path_to_mod.iterdir():
        for a in x.iterdir():
            type = type_checking(a)
            path_for_create_new_folder = path_for_folder_creation / a.parent.name
            if type is True:
                test1 = path_for_folder_creation / 'ThingDef'
                if test1.exists() is False:
                    test1.mkdir(parents=True)
                write_to_file(path=str(test1 / a.name),
                              data=get_filtered_data(get_data_from_file(a)))
            else:
                if path_for_create_new_folder.exists() is False:
                    path_for_create_new_folder.mkdir(parents=False)
                write_to_file(path=str(path_for_create_new_folder / a.name),
                              data=get_filtered_data(get_data_from_file(a)))


def type_checking(file):
    is_defname = True
    data = get_data_from_file(file)
    for i in data:
        if 'ThingDef' in i:
            return is_defname


def get_file_from_dir(path):
    pass


def get_all_in_dir(path):
    test = list()
    for x in path.iterdir():
        if x.is_file():
            test.append(x)
        elif x.is_dir():
            test.append(x)
            test.extend(get_all_in_dir(x))
    return test


def get_data_from_file(path):
    try:
        with open(path.absolute(), 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(path)
        return None


run(path_to_mod='C:/Program Files (x86)/Steam/steamapps/workshop/content/294100/1718190143/1.5/Defs')
