from UI import App
import os

def get_data_from_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.readlines()
            return content
    except FileNotFoundError:
        print("Файл не знайдено")
        return None

def crate_directory():
    pass

def get_comment(line):
    comment = "<!--" + line + "-->"
    return comment


def get_def_name(def_line):
    stage1 = def_line.replace("<defName>", "")
    stage2 = stage1.replace("</defName>", "")
    return stage2


def get_label(def_name, label_line):
    stage1 = label_line.replace("<label>", "")
    stage2 = stage1.replace("</label>", "")
    comment = get_comment(line=stage2)
    label = "\n  " + comment + "\n  <" + def_name + ".label>" + stage2 + "</" + def_name + ".label>"
    return label


def get_description(def_name, description_line):
    stage1 = description_line.replace("<description>", "")
    stage2 = stage1.replace("</description>", "")
    comment = get_comment(line=stage2)
    description = "\n  " + comment + "\n  <" + def_name + ".description>" + stage2 + "</" + def_name + ".description>"
    return description


def data_filter(obtained_data):
    data_filtering_stage1 = [item.strip() for item in obtained_data]
    data_filtering_stage2 = []
    for i in data_filtering_stage1:
        if "<defName>" in i or "<label>" in i or "<description>" in i:
            if "<label>point</label>" not in i and "<label>edge</label>" not in i:
                data_filtering_stage2.append(i)
    data = []
    def_name = None
    for i in data_filtering_stage2:
        if "<defName>" in i:
            def_name = get_def_name(i)
        if "<label>" in i:
            data.append(get_label(def_name, i))
        if "description" in i:
            data.append(get_description(def_name, i))
    return data


def write_to_file(path, data):
    try:
        with open(path, "w+", encoding="utf-8") as file:
            file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<LanguageData>")
            for i in data:
                file.write(i)
            file.write("\n</LanguageData>")
    except FileNotFoundError:
        print("Файл не знайдено")
        return None


def run():
    input_path_to_mod_file = (input("Вкажіть шлях до файлу моду: "))
    obtained_data = get_data_from_file(input_path_to_mod_file)
    filtered_data = data_filter(obtained_data)
    input_path_to_translation_file = (input("Вкажіть шлях до файлу перекладу: "))
    write_to_file(input_path_to_translation_file, filtered_data)


def get_path_to_about_xml(path_to_mods_folder):
    list_path = list()
    with os.scandir(path_to_mods_folder) as entries:
        for entry in entries:
            list_path.append(entry.name)
    path_to_about_xml = []
    for i in list_path:
        path_to_about_xml.append("C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\294100\\" + i + "\\About\\About.xml")
    return path_to_about_xml



def get_mod_names():
    path_to_mods_folder = "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\294100"
    list_of_path_to_about_xml = get_path_to_about_xml(path_to_mods_folder)
    list_of_path_to_about_xml.sort(reverse=True)
    mod_names = list()

    for i in range(len(list_of_path_to_about_xml)):
        path_to_about_xml = str(list_of_path_to_about_xml[i])
        try:
            with open(path_to_about_xml, "r", encoding="utf-8") as file:
                test = file.readlines()
        except FileNotFoundError:
            print("Помилка обробки шляху моду")
            print(path_to_about_xml)
            return None
        for a in test:
            if "<name>" in a:
                test2 = a
                test3 = test2.replace("<name>", "")
                test4 = test3.replace("</name>", "")
                test5 = test4.strip()
                mod_names.append(test5)
    return mod_names


# path = get_path_to_about_xml("C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\294100")
# path.sort(reverse=True)
# print(path, "\n", len(path))

# print(get_mod_names())
# об'єкт класу, вікно програми
App(title="Конструктор перекладу", size=(800, 600), mod_names=get_mod_names())

# run()
