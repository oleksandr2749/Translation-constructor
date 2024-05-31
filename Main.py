from UI import App
import os
import pathlib


def get_data_from_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.readlines()
            return content
    except FileNotFoundError:
        print("Помилка функції get_data_from_file")
        return None


# Функція створення списку відфільтрованих даних отриманих від get_data_from_file
def get_filtered_data(obtained_data):
    data_strip = list()
    data = list()
    words_to_remove = ["<defName>", "</defName>", "<label>", "</label>", "<description>", "</description>"]
    # Цикл видалення пробілів, табуляцій, переходів
    for i in obtained_data:
        data_strip.append(i.strip())
    #
    for i in data_strip:
        if "<defName>" in i or "<label>" in i or "<description>" in i:
            if "<label>point</label>" not in i and "<label>edge</label>" not in i:
                if "<defName>" in i:
                    def_name = i
                    for word in words_to_remove:
                        def_name = def_name.replace(word, "")
                if "<label>" in i:
                    label = i
                    for word in words_to_remove:
                        label = label.replace(word, "")
                    data.append("\n  " + "<!--" + label + "-->" + "\n  <" + def_name + ".label>" + label + "</" + def_name + ".label>")
                if "<description>" in i:
                    description = i
                    for word in words_to_remove:
                        description = description.replace(word, "")
                    data.append("\n  " + "<!--" + description + "-->" + "\n  <" + def_name + ".description>" + description + "</" + def_name + ".description>")
    return data


def write_to_file(path: str, data: list):
    try:
        with open(path, "w+", encoding="utf-8") as file:
            file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<LanguageData>")
            for i in data:
                file.write(i)
            file.write("\n</LanguageData>\n")
    except FileNotFoundError:
        print("Помилка функції write_to_file")
        return None


def run():
    # input_path_to_mod_file = (input("Вкажіть шлях до файлу моду: "))
    input_path_to_mod_file = "Buildings_Temperature.xml"
    # input_path_to_translation_file = (input("Вкажіть шлях до файлу перекладу: "))
    input_path_to_translation_file = "Test.xml"
    write_to_file(path=input_path_to_translation_file, data=get_filtered_data(get_data_from_file(path=input_path_to_mod_file)))


#run()


def get_path_to_about_xml(path_to_mods_folder):
    list_path = list()
    with os.scandir(path_to_mods_folder) as entries:
        for entry in entries:
            list_path.append(entry.name)
    path_to_about_xml = []
    for i in list_path:
        path_to_about_xml.append("C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\294100\\" + i +
                                 "\\About\\About.xml")
    return path_to_about_xml


def find_file(file_name, search_directory):
    for root, dirs, files in os.walk(search_directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def get_mod_names():
    path_to_mods_folder = "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\294100"
    mod_names = list()

    for i in range(len(list_of_path_to_about_xml)):
        path_to_about_xml = str(list_of_path_to_about_xml[i])
        try:
            with open(path_to_about_xml, "r", encoding="utf-8") as file:
                test = file.readlines()
        except FileNotFoundError:
            print("Помилка обробки шляху моду")
            return None
        for a in test:
            if "<name>" in a:
                test2 = a
                test3 = test2.replace("<name>", "")
                test4 = test3.replace("</name>", "")
                test5 = test4.strip()
                mod_names.append(test5)
        mod_names.sort()
    return mod_names


#get_mod_names()

# ModNames = ["Тестова назва", "Тестова назва 2"]
# ModId = ["00001", "00002"]
# ModAuthors = ["Тестовий автор", "Тестовий автор 2"]
