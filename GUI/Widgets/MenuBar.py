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

from PySide6.QtWidgets import (QMenuBar, QComboBox, QGridLayout, QWidget, QLabel, QLineEdit, QRadioButton, QPushButton,
                               QVBoxLayout, QTreeView, QFileSystemModel, QFileDialog, QGroupBox, QSlider, QHBoxLayout)
from PySide6.QtCore import Qt, QPoint, QDir
from PySide6.QtGui import QIcon, QAction

import Main


class Mode(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setToolTip(f'Пояснення вибору режимів')
        layout = QGridLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        self.setLayout(layout)

        title_label = QLabel()
        title_label.setObjectName('ModeTitle')
        title_label.setText('')


class PlacementMode(QGroupBox):
    def __init__(self, title='Режим розміщення рядків *'):
        super().__init__(title)

        self.placement_mode_accordance = QRadioButton()
        self.placement_mode_accordance.setObjectName('PlacementModeAccordance')
        self.placement_mode_accordance.setText('Відповідність')
        self.placement_mode_accordance.setToolTip('Рядки перекладу будуть розміщені відповідно\n до розміщення в '
                                                  'оригінальному моді.')
        self.placement_mode_accordance.toggled.connect(self.limit_hide)

        self.placement_mode_single = QRadioButton()
        self.placement_mode_single.setObjectName('PlacementModeSingle')
        self.placement_mode_single.setText('В одному файлі')
        self.placement_mode_single.setToolTip(
            'Рядки перекладу елементів одного типу будуть розміщені в одному файлі.\nЯкщо досягнуто ліміт рядків, буде '
            'створено наступний файл.\nУвага! Це може призвести до відокремлення опису від назви одного\n елемента в'
            'інший файл, що погіршує читабельність.')
        self.placement_mode_single.toggled.connect(self.limit_show)

        self.limit = QLabel('Ліміт рядків в файлі: ')
        self.limit.hide()

        self.placement_mode_single_limit = QSlider(Qt.Horizontal)
        self.placement_mode_single_limit.setMinimum(30)
        self.placement_mode_single_limit.setMaximum(300)
        self.placement_mode_single_limit.setTickPosition(QSlider.TicksBelow)
        self.placement_mode_single_limit.valueChanged.connect(self.print_value)
        self.placement_mode_single_limit.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.placement_mode_accordance)
        layout.addWidget(self.placement_mode_single)
        layout.addWidget(self.limit)
        layout.addWidget(self.placement_mode_single_limit)

        self.setLayout(layout)

    def print_value(self, value):
        self.limit.setText('Максимальна кількість рядків в файлі: ' + str(value))

    def limit_show(self):
        self.limit.show()
        self.placement_mode_single_limit.show()

    def limit_hide(self):
        self.limit.hide()
        self.placement_mode_single_limit.hide()



class PathInputLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        layout.setContentsMargins(0, 5, 0, 5)
        self.setLayout(layout)

        title_label = QLabel()
        title_label.setObjectName('PatchInputLineTitle')
        title_label.setText('Місце збереження *')

        self.input_line = QLineEdit()
        self.input_line.setObjectName('PatchInputLine')
        self.input_line.setPlaceholderText('Вкажіть шлях до місця збереження')
        self.input_line.setText(self.path_from_config())
        self.input_line.textChanged.connect(self.input_path)

        layout.addWidget(title_label, 0, 0)
        layout.addWidget(self.input_line, 1, 0)

    def input_path(self):

        if self.input_line.text() != '':
            Main.config.set('Settings', 'export_path', self.input_line.text())
        else:
            Main.config.set('Settings', 'export_path', 'NotSet')

        try:
            with open('config.ini', 'w') as configfile:
                Main.config.write(configfile)
        except FileNotFoundError:
            print('Помилка обробки конфігураційного файла')

    def path_from_config(self):
        try:
            with open('config.ini', 'r') as configfile:
                if Main.config.get('Settings', 'export_path') != 'NotSet':
                    return Main.config.get('Settings', 'export_path')
                else:
                    return

        except FileNotFoundError:
            print('Помилка обробки конфігураційного файла')


class LocalizationSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        self.setObjectName('LocalizationSettings')
        self.setFixedSize(200, 115)
        self.setStyleSheet('''#LocalizationSettings {
        background: #1A1D20;
        }
        #LocalizationList {
        border: none;
        background: transparent;
        }''')

        layout = QGridLayout()

        label = QLabel('Долучайтесь до проек\nту на GitHub та додай\nсвою мову.')
        layout.addWidget(label, 1, 0)

        self.localization_list = QComboBox()
        self.localization_list.setObjectName('LocalizationList')
        self.localization_list.addItem(QIcon('GUI/Icons and style/flag-UA.svg'), 'Українська')
        self.localization_list.addItem(QIcon('GUI/Icons and style/flag-UK.svg'), 'English')
        layout.addWidget(self.localization_list, 0, 0)

        self.setLayout(layout)


class ToggleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.button = QPushButton(icon=QIcon('GUI/Icons and style/question.svg'))
        self.button.setObjectName('QuestionButton')
        self.button.setFixedSize(16, 16)
        self.button.setStyleSheet('#QuestionButton { border: none; }')
        self.text_widget = QLabel(f'Цей текст розгортається і згортатиметься при натисканні на кнопку.'
                                  f' Можна додати більше тексту або інші віджети тут.')

        self.text_widget.setWordWrap(True)
        self.text_widget.setMaximumHeight(0)  # Спочатку приховано

        self.button.clicked.connect(self.toggle_text_widget)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.text_widget)

        self.setLayout(self.layout)

    def toggle_text_widget(self):
        if self.text_widget.maximumHeight() == 0:
            # Розгортаємо текстовий віджет
            self.text_widget.setMaximumHeight(200)  # Встановлюємо висоту за потребою
        else:
            # Згортаємо текстовий віджет
            self.text_widget.setMaximumHeight(0)


class FileExplorer(QWidget):
    def __init__(self):
        super().__init__()

        # Створюємо макет
        layout = QVBoxLayout(self)

        # Створюємо модель файлової системи
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(QDir.rootPath())  # Встановлюємо кореневу директорію

        # Створюємо QTreeView і налаштовуємо модель
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setRootIndex(self.file_system_model.index(QDir.rootPath()))

        # Додаємо QTreeView в макет
        layout.addWidget(self.tree_view)

        # Налаштовуємо віджет
        self.setLayout(layout)
        self.setWindowTitle("Файловий провідник")
        self.resize(800, 600)


class FileSelector(QWidget):
    def __init__(self):
        super().__init__()

        # Створюємо макет
        layout = QVBoxLayout(self)

        # Створюємо кнопку для вибору файлу
        self.button = QPushButton("Вибрати файл")
        self.button.clicked.connect(self.open_file_dialog)

        # Створюємо QLabel для відображення вибраного файлу
        self.label = QLabel("Вибраний файл не вибрано")

        # Додаємо віджети в макет
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        # Налаштовуємо віджет
        self.setLayout(layout)
        self.setWindowTitle("Вибір файлу")
        self.resize(300, 150)

    def open_file_dialog(self):
        # Відкриваємо діалог для вибору файлу
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)  # Дозволяє вибирати один або кілька файлів
        file_dialog.setViewMode(QFileDialog.List)  # Відображає файли в списковому вигляді

        if file_dialog.exec():  # Показує діалог і перевіряє, чи натиснуто "ОК"
            selected_files = file_dialog.selectedFiles()  # Отримуємо вибрані файли
            if selected_files:
                self.label.setText(f"Вибрано файл: {selected_files[0]}")  # Відображаємо вибраний файл


class ExecutiveSettingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout()
        self.setLayout(layout)

        note = QLabel()
        note.setObjectName('SettingNote')
        note.setText(f'Обов\'язкові налаштування відмічені *\nНаведіться на параметр щоб побачити пояснення')

        back = QPushButton()
        back.setText('Назад')
        back.setFixedWidth(100)
        back.clicked.connect(self.button_back)

        self.path_input_line = PathInputLine()

        layout.addWidget(note, 0, 0)
        layout.addWidget(self.path_input_line, 1, 0)
        # layout.addWidget(Mode(), 2, 0)
        # layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), 3, 0)
        layout.setRowStretch(4, 1)
        layout.addWidget(back, 5, 0)

        placement_mode = PlacementMode()
        layout.addWidget(placement_mode, 2, 0)

    def button_back(self):
        self.hide()


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName('MenuBar')
        self.settings_menu = self.addMenu("Налаштування")

        self.localization_action = QAction(QIcon('GUI/Icons and style/language.svg'), 'Локалізація')
        self.settings_menu.addAction(self.localization_action)
        self.localization_action.triggered.connect(self.localization_widget)
        self.localization_settings_widget = LocalizationSettingsWidget(self)

        self.execution_action = QAction('Виконання')
        self.settings_menu.addAction(self.execution_action)
        self.execution_action.triggered.connect(self.execution_widget)
        self.execution_settings_widget = ExecutiveSettingWidget()
        self.execution_settings_widget.hide()

    def localization_widget(self):
        self.localization_settings_widget.move(self.mapToGlobal(self.actionGeometry(self.localization_action).bottomRight() + QPoint(130, 22)))
        # self.settings_menu.show()
        self.localization_settings_widget.show()

    def execution_widget(self):
        self.execution_settings_widget.show()
