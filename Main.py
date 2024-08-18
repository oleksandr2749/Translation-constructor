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

from GUI import MainWindow
import sys
import configparser
import pathlib
import logging

from PySide6.QtWidgets import QApplication

# Журнал подій
logging.addLevelName(logging.DEBUG, 'НАЛАГОДЖЕННЯ')
logging.addLevelName(logging.INFO, 'ІНФ.')
logging.addLevelName(logging.WARNING, 'УВАГА')
logging.addLevelName(logging.ERROR, 'ПОМИЛКА')
logging.addLevelName(logging.CRITICAL, 'КРИТИЧНА ПОМИЛКА')
logging.basicConfig(
    filename='program.log',
    encoding='utf-8',
    filemode='w',

    format='{asctime} {levelname} - {message}',
    style='{',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.DEBUG
)

# Файл налаштувань
config = configparser.ConfigParser()
if not pathlib.Path('config.ini').exists():
    config['Settings'] = {'export_path': 'NotSet'}
    try:
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    except FileNotFoundError:
        print('Помилка обробки конфігураційного файла')
else:
    config.read('config.ini')
    '''try:
        with open('config.ini', 'r') as configfile:
            config.read(configfile)
    except FileNotFoundError:
        print('Помилка обробки конфігураційного файла')'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow.MainWindow()
    window.show()
    with open("GUI/Icons and style/style", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    sys.exit(app.exec())
