from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy, QFileDialog, QListWidget,
                               QListWidgetItem, QSpacerItem)
from PySide6.QtCore import Qt

from GUI.Widgets.TopBar import TopBar
from GUI.Widgets.ModList import ModList
from GUI.Widgets.RecntList import RecentList

import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET

from Modification import Modification

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('MainWidget')

        # Розмітка
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        # Кнопка створити мод
        self.create_mod_button = QPushButton('Створити модифікацію')
        self.create_mod_button.setObjectName('create_mod_button')
        # self.create_mod_button.setMaximumSize(300, 60)
        self.create_mod_button.setMaximumWidth(300)
        # Кнопка відкрити мод
        self.open_mod_button = QPushButton('Відкрити')
        self.open_mod_button.setObjectName('open_mod_button')
        # self.open_mod_button.setMaximumSize(300, 60)
        self.open_mod_button.clicked.connect(self.open_mod_click)

        # Нещодавні моди
        self.recent_list = RecentList()
        self.recent_list.add('/path/Mod')

        self.list = QListWidget()

        self.mod = QListWidgetItem()
        self.mod.setText('Модифікація')

        self.list.insertItem(0, self.mod)
        self.mod2 = QListWidgetItem()
        self.mod2.setText('qwerty')
        self.list.insertItem(1, self.mod2)


        # Розмітка віджетів
        self.layout.setRowStretch(0, 1)
        self.layout.addWidget(self.create_mod_button, 1, 0)
        # self.layout.setRowStretch(1, 0)
        self.layout.addWidget(self.open_mod_button, 2, 0)
        # self.layout.setRowStretch(2, 0)
        self.layout.setRowStretch(3, 3)
        # self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), 1, 0)

        # self.layout.addWidget(self.list, 2, 0)

    def open_mod_click(self):
        # Вікно вибору теки моду
        dialog = QFileDialog(self)
        dialog.setDirectory('/home')

        open_mod_path = Path(str(dialog.getExistingDirectory()))
        mod = Modification()
        tree = ET.parse(open_mod_path / 'About/About.xml')
        root = tree.getroot()

        mod.root_path = open_mod_path
        mod.name = root.find('name').text
        mod.author = root.find('author').text
        mod.description = root.find('description').text
        mod.package_id = root.find('packageId').text
        mod.mod_version = root.find('modVersion').text
