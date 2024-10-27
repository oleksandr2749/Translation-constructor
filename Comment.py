import pathlib
import xml.etree.ElementTree as ET
from pathlib import Path


# Функція коментування оригінальних рядків файлу-перекладу.
# Приймає tree, root, Path або рядок
# Повертає root
def comment_original_string(element):
    if type(element) is ET.ElementTree:
        root = element.getroot()
    elif type(element) is ET.Element:
        root = element
    elif type(element) is pathlib.PosixPath or type(element) is str:
        root = ET.ElementTree(element).getroot()
    else:
        print('Отримано неправильний тип елементу')
        return

    for child in root:
        new_root = ET.Element('LanguageData')
        new_root.append(ET.Comment(child.text))
        new_root.append(child)
    return new_root
