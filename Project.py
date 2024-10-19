from pathlib import Path
from configparser import ConfigParser
import traceback
import shutil
import logging
import xml.etree.ElementTree as ET

import Testing.Debugging
import Process


class Project:
    def __init__(self):

        # Про
        self.name = None
        self.package_id = None
        self.author = None
        self.published_file_id = None
        self.description = None
        self.mod_version = None

        self.logo = None

        # Службові
        self.root_path = None

        self.config = ConfigParser()
        self.config['Project'] = {}

    # Метод створення тек модифікації
    def create_folder(self, path):
        logging.info(f'Викликано метод створення директорії проекту')
        try:
            Path(path).mkdir(exist_ok=True)
        except OSError:
            logging.error(f'Невірний шлях \'{path}\'')
            return

    def about_xml_write(self, parameter: str, value: str, root):
        ET.SubElement(root, parameter).text = value
        tree = ET.ElementTree(root)
        ET.indent(root, level=0)
        tree.write(self.root_path / 'About/About.xml', encoding='utf-8', xml_declaration=True)

    def save_config(self, attributes):
        for attribute in attributes:
            if attributes[attribute] is not None:
                self.config['Project'][attribute] = attributes[attribute]
        with open(self.root_path / 'Project.ini', 'w') as configfile:
            self.config.write(configfile)

    def load_config(self, path, attributes):
        self.config.read(path)
        for key in attributes:
            if key in self.config['Project']:
                setattr(self, key, self.config['Project'][key])

    def add_translation(self):
        pass

    def add_logo(self, logo):
        if type(logo) is str:
            logo = Path(logo)

        if logo.suffix == '.png':
            if self.check_logo(logo)['size'] < 1048576:
                shutil.copyfile(logo, '/home/oleksandr/Desktop/logo.png')
            else:
                print(f'Розмір логотипу більше 1МБ: {self.check_logo(logo)['size']/1024}МБ')
        else:
            print('Помилковий шлях')

    def delete_logo(self):
        pass

    def check_logo(self, logo=None):
        if logo is None:
            result = {'size': self.__logo.stat().st_size,
                      'resolution': None}
        elif logo is not None:
            result = {'size': Path(logo).stat().st_size,
                      'resolution': None}
        return result
