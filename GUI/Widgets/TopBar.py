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

from PySide6.QtWidgets import QGridLayout, QWidget, QHBoxLayout
from PySide6.QtGui import QMouseEvent
from PySide6.QtSvgWidgets import QSvgWidget

import Main
from GUI.Widgets.SearchBar import SearchBar


class SVGButton(QSvgWidget):
    def mousePressEvent(self, event: QMouseEvent):
        self.on_label_clicked()
        super().mousePressEvent(event)

    def test(self):
        print(self)


class TopButtonBar(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.author = SVGButton('GUI/Icons and style/user.svg')
        self.author.setFixedSize(32, 32)

        self.layout.addWidget(self.author)

class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('TopBarWidget')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.search_bar = SearchBar()
        self.button = TopButtonBar()
        self.layout.addWidget(self.search_bar, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
