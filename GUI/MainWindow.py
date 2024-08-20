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

from GUI.Widgets.MenuBar import MenuBar
from GUI.Widgets.TopBar import TopBar
from GUI.Widgets.ModList import ModList
from GUI.Widgets.StatusBar import StatusBar

from PySide6.QtWidgets import QWidget, QGridLayout, QMainWindow
from PySide6.QtGui import QIcon, QClipboard, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('MainWidget')

        self.widget_layout = QGridLayout()
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_layout.setVerticalSpacing(0)
        self.setLayout(self.widget_layout)

        self.top_bar = TopBar()
        self.widget_layout.addWidget(self.top_bar, 0, 0)

        self.mod_list = ModList()
        self.widget_layout.addWidget(self.mod_list, 1, 0)
        self.top_bar.search_bar.set_mod_list(self.mod_list)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Конструктор перекладу")

        self.setObjectName('MainWindow')
        self.resize(800, 600)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)

        self.menu_bar_widget = MenuBar()
        self.setMenuBar(self.menu_bar_widget)

        self.status_bar = StatusBar(mods_number=len(self.main_widget.mod_list.modlistdata))
        self.setStatusBar(self.status_bar)
