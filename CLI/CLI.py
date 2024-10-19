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

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET
import Process
from Modification import Modification

parser = argparse.ArgumentParser()
parser.add_argument('action')
parser.add_argument('target_mod')
parser.add_argument('export_mod')
parser.add_argument('version')
parser.add_argument('language')
# parser.add_argument('destination_mod')
args = parser.parse_args()


def construct(path_to_mod_dir):
    Process.processing_modular_mode(source_mod=Modification(root_path=path_to_mod_dir,
                                                            about=ET.parse(path_to_mod_dir/'About/About.xml').getroot()),
                                    export_path=args.export_mod,
                                    language=args.language,
                                    version=args.version)


if args.action == 'construct':
    construct(path_to_mod_dir=Path(args.target_mod))
else:
    print(f'Помилка: відсутня команда \"{args.action}\"\nСкористайтесь командою -h або --help для перегляду довідки.')
