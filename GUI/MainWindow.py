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

from PySide6.QtWidgets import (QWidget, QGridLayout, QMainWindow, QLabel, QStatusBar, QGroupBox, QPushButton,
                               QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem)
from PySide6.QtGui import QIcon, QClipboard, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer, QtSvg
from PySide6.QtCore import Qt, QSize, Signal


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('MainWidget')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        self.top_bar = TopBar()

        self.notifications = QLabel('Перед початком роботи виконайте налаштування')
        self.notifications.setAlignment(Qt.AlignCenter)
        self.notifications.setObjectName('Notification')
        self.notifications.hide()


        self.mod_list = ModList()
        self.top_bar.search_bar.set_mod_list(self.mod_list)

        self.layout.addWidget(self.top_bar, 0, 0)
        self.layout.addWidget(self.notifications, 1, 0)
        self.layout.addWidget(self.mod_list, 2, 0)

    def notificationVisibility(self, value: bool):
        if value is True:
            self.notifications.show()
        else:
            self.notifications.hide()


class ProjectLabel(QLabel):
    hovered = Signal()
    left = Signal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def enterEvent(self, event):
        self.hovered.emit()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.left.emit()
        super().leaveEvent(event)


class ProjectList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMaximumSize(300, 150)
        self.setWidgetResizable(True)

        self.layout = QGridLayout()
        self.layout.setSpacing(0)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.delete_button = QPushButton('Видалити')
        self.delete_button.setStyleSheet('background: #972127;')
        self.delete_button.clicked.connect(self.delete_button_click)

        self.fill_list()
        self.setWidget(self.widget)
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

    def delete_button_click(self):
        index = self.layout.indexOf(self.delete_button)
        row, _, _, _ = self.layout.getItemPosition(index)
        project = self.layout.itemAtPosition(row, 0).widget()
        project.setParent(None)
        self.delete_button.setParent(None)

    def fill_list(self):
        for i in range(1, 11):
            project_label = ProjectLabel(f'Проект {i}')
            project_label.setStyleSheet('background: #065A7C;')
            self.layout.addWidget(project_label)
            project_label.hovered.connect(lambda row=i-1: self.show_button(row))
            project_label.left.connect(self.hide_button)

    def show_button(self, row):
        print('кнопку показано')
        self.layout.addWidget(self.delete_button, row, 1)

    def hide_button(self):
        print('кнопку приховано')
        self.layout.removeWidget(self.delete_button)
        self.delete_button.setParent(None)


class ProjectMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        parent_window = self.parentWidget()
        layout = QGridLayout()
        self.setLayout(layout)

        create_project_button = QPushButton()
        create_project_button.setText('Створити проект')
        create_project_button.setFixedSize(300, 64)
        create_project_button.setIcon(QIcon('GUI/Icons and style/add-project.svg'))
        create_project_button.setStyleSheet('font: bold 20px')
        create_project_button_icon = QSize(64, 64)
        create_project_button.setIconSize(create_project_button_icon)

        layout.addWidget(create_project_button)
        layout.addWidget(ProjectList())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Конструктор перекладу")

        self.setObjectName('MainWindow')
        self.resize(800, 600)

        self.main_widget = MainWidget()
        # self.project_main_widget = ProjectMainWidget(parent=self)
        self.setCentralWidget(self.main_widget)

        self.menu_bar_widget = MenuBar()
        self.setMenuBar(self.menu_bar_widget)
