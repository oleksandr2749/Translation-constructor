from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QSizePolicy, QScrollBar,
                               QScrollArea, QSpacerItem, QFrame, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt, QSize, Signal, QRect, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QPixmap, QColor, QImage, QMouseEvent

from pathlib import Path
import xml.etree.ElementTree as ET
from configparser import ConfigParser

from Project import Project
from GUI.Widgets.MyBaseWidgets import MyLabel


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

        self.setWidget(self.widget)

    def delete_button_click(self):
        index = self.layout.indexOf(self.delete_button)
        row, _, _, _ = self.layout.getItemPosition(index)
        project = self.layout.itemAtPosition(row, 0).widget()
        project.setParent(None)
        self.delete_button.setParent(None)

    def add_project_to_list(self, project):
        if project.name is None:
            project_label = MyLabel('Помилка відображення назви')
        else:
            project_label = MyLabel(project.name)
        project_label.doubleClicked.connect(self.print_project)
        self.layout.addWidget(project_label)

    def print_project(self):
        print('Натиснуто')

    def show_button(self, row):
        print('кнопку показано')
        self.layout.addWidget(self.delete_button, row, 1)

    def hide_button(self):
        print('кнопку приховано')
        self.layout.removeWidget(self.delete_button)
        self.delete_button.setParent(None)


class CreateProjectWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 500)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.name = QLabel('Назва')
        self.name.setToolTip('Назва вашого проекту та моду')
        self.name_input = QLineEdit()
        self.name_input.setMaximumWidth(200)

        self.packageId = QLabel('Ідентифікатор')
        self.packageId.setToolTip('Унікальна "справжня" назва модифікації'
                                  '\n\n Хорошою практикою є подібний вигляд ідентифікатору \'author.shortNameOfMod\''
                                  '\n Це гарантує унікальність ідентифікатору задля відсутності конфлікту між'
                                  'модифікаціями')
        self.packageId_input = QLineEdit()
        self.packageId_input.setMaximumWidth(200)

        self.author = QLabel('Автор')
        self.author.setToolTip('Внутрішньоігрова інформація про автора модифікації. Це не впливає на сторінку моду в '
                               'майстерні стім'
                               '\nНатисніть Enter щоб додати автора.'
                               '\nМоже містити безліч авторів')
        self.author_input = QLineEdit()
        self.author_input.setMaximumWidth(200)

        self.root_path = QLabel('Місце збереження')
        self.root_path_input = QLineEdit()
        self.root_path.setMaximumWidth(200)

        self.description = QLabel('Опис')
        self.description.setToolTip('Опис вашої модифікації-перекладу.\nЗалиште пустим щоб не додавати опис')
        self.description_input = QTextEdit()

        self.create_button = QPushButton('Створити')
        self.create_button.clicked.connect(self.create_button_click)

        self.cancel_button = QPushButton('Назад')
        self.cancel_button.clicked.connect(self.cancel_button_click)

        self.logo_label = QLabel('Логотип')
        self.logo = QLabel()
        self.logo_pixmap = QPixmap('/home/oleksandr/PycharmProjects/Translation-Constructor/GUI/Icons and style'
                                   '/logo.png')
        self.logo_pixmap.fill('#404040')
        self.logo_pixmap = self.logo_pixmap.scaled(300, 150, Qt.AspectRatioMode.KeepAspectRatio)
        self.logo.setPixmap(self.logo_pixmap)
        self.logo_input = QLineEdit()
        self.logo_input.setPlaceholderText('Шлях до логотипу:')

        # Схема
        self.parameters_layout = QVBoxLayout()
        self.parameters_layout.addWidget(self.name)
        self.parameters_layout.addWidget(self.name_input)
        self.parameters_layout.addWidget(self.author)
        self.parameters_layout.addWidget(self.author_input)
        self.parameters_layout.addWidget(self.packageId)
        self.parameters_layout.addWidget(self.packageId_input)

        self.layout_logo = QGridLayout()
        self.layout_logo.addWidget(self.logo_label, 0, 0)
        self.layout_logo.addWidget(self.logo, 1, 0)
        self.layout_logo.addWidget(self.logo_input, 2, 0)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.button_layout.addWidget(self.create_button)

        self.layout.addLayout(self.parameters_layout, 0, 0)
        self.layout.addLayout(self.layout_logo, 0, 1)
        self.layout.addWidget(self.description, 1, 0)
        self.layout.addWidget(self.description_input, 2, 0, 1, 2)
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), 3, 0)
        self.layout.addLayout(self.button_layout, 4, 0, 1, 2)

    def create_button_click(self):
        project = Project()

        # Атрибути проекту
        project.root_path = Path('/home/oleksandr/Desktop/MyProgram') / self.name_input.text()
        project.name = self.name_input.text()
        project.author = self.author_input.text()
        project.package_id = self.packageId_input.text()
        project.description = self.description_input.toPlainText()

        # Створення тек модифікації
        project.create_folder(path=project.root_path)
        project.create_folder(path=project.root_path / 'About')

        # Створення About.xml
        root = ET.Element('ModMetaData')

        tree = ET.ElementTree(root)
        tree.write(project.root_path / 'About/About.xml', encoding='utf-8', xml_declaration=True)

        # Запис About.xml
        project.about_xml_write(parameter='name', value=self.name_input.text(), root=root)
        project.about_xml_write(parameter='author', value=self.author_input.text(), root=root)
        project.about_xml_write(parameter='packageID', value=self.packageId_input.text(), root=root)
        if self.description_input.toPlainText() != '':
            project.about_xml_write(parameter='description', value=self.description_input.toPlainText(), root=root)

        # Збереження
        project.save_config(attributes={'root_path': str(project.root_path),
                                        'name': project.name,
                                        'author': project.author,
                                        'description': project.description,
                                        'mod_version': project.mod_version,
                                        'package_id': project.package_id,
                                        'published_file_id': project.published_file_id})

        self.close()

    def cancel_button_click(self):
        self.close()


class ProjectMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout()

        self.setLayout(self.layout)

        create_project_button = QPushButton()
        create_project_button.setText('Створити проект')
        create_project_button.setStyleSheet('font: bold 24px')
        create_project_button.clicked.connect(self.create_click)

        self.project_list = ProjectList()

        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding), 0, 0)
        self.layout.addWidget(create_project_button, 1, 0)
        self.layout.addWidget(self.project_list, 2, 0)
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding), 3, 0)

        self.create_project = CreateProjectWidget()

    def create_click(self):
        self.create_project.show()
