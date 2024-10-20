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
# You should have received a copy of the GNU General Public License along with Translation Constructor.
# If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import QMainWindow

from GUI.Widgets.MenuBar import MenuBar
from GUI.Widgets.MainWidget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # Параметри вікна
        self.setObjectName('MainWindow')
        self.setWindowTitle('Конструктор перекладу 1.0.1')
        self.resize(800, 600)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.menu_bar_widget = MenuBar()
        self.setMenuBar(self.menu_bar_widget)
