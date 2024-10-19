from pathlib import Path
from configparser import ConfigParser
import traceback
import shutil
import logging
import xml.etree.ElementTree as ET

import Testing.Debugging
import Process


class Modification:
    def __init__(self, name=None, package_id=None, author=None, description=None, mod_version=None,
                 published_file_id=None, about=None, root_path=None):

        # Про
        self.name = name
        self.package_id = package_id
        self.author = author
        self.description = description
        self.mod_version = mod_version
        self.published_file_id = published_file_id

        self.about = about

        # Службові
        self.root_path = root_path

    def about_xml_write(self, parameter: str, value: str, root):
        ET.SubElement(root, parameter).text = value
        tree = ET.ElementTree(root)
        ET.indent(root, level=0)
        tree.write(self.root_path / 'About/About.xml', encoding='utf-8', xml_declaration=True)
