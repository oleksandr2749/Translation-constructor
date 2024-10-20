# This file is part of Translation Constructor.
#
# Translation Constructor is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Translation Constructor is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with Translation Constructor. If not,
# see <https://www.gnu.org/licenses/>.

import logging
from pathlib import Path
import xml.etree.ElementTree as ET


def def_process(mod_data):
    root = ET.Element('LanguageData')
    file_type = None
    for i in mod_data:
        def_name = i.find('defName')

        if def_name is not None:
            label = i.find('label')
            if label is not None:
                root.append(ET.Comment(label.text))
                ET.SubElement(root, def_name.text + '.label').text = label.text
            description = i.find('description')
            if description is not None:
                root.append(ET.Comment(description.text))
                ET.SubElement(root, def_name.text + '.description').text = description.text
            if label is not None or description is not None:
                if file_type is None:
                    file_type = i.tag

    ET.indent(root, level=0)

    if len(root) == 0:
        return None, None
    else:
        return root, file_type


def xml_file_write(data, path, name):
    tree = ET.ElementTree(data)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    tree.write(file_or_filename=path / name, encoding='utf-8', xml_declaration=True)


# Функція виконання в режимі модулів
def processing_modular_mode(source_mod, language, export_path, version):
    export_path = Path(export_path)
    language = language.capitalize()

    (export_path / source_mod.about.find('name').text / 'Languages' / language).mkdir(parents=True, exist_ok=True)

    for element in Path(source_mod.root_path / version).glob('**/*.xml'):
        cooked_defs, def_type = def_process(ET.parse(element).getroot())
        if def_type is not None:
            xml_file_write(data=cooked_defs,
                           name=element.stem + '_' + source_mod.about.find('packageId').text + '.xml',
                           path=export_path / source_mod.about.find('name').text / 'Languages' / language / 'DefInjected' / def_type)

    if (source_mod.root_path / 'Languages/English/Keyed').exists():
        for keyed in Path(source_mod.root_path / 'Languages/English/Keyed').glob('**/*.xml'):
            destination = export_path / source_mod.about.find('name').text / 'Languages' / language / 'Keyed' / keyed.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(keyed.read_bytes())
            root = ET.parse(keyed).getroot()
            for element in list(root):
                root.insert(list(root).index(element), ET.Comment(element.text))
