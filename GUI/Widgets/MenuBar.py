from PySide6.QtWidgets import (QMenuBar, QComboBox, QGridLayout, QWidget, QLabel, QSizePolicy, QLineEdit, QSpacerItem,
                               QRadioButton, QButtonGroup, QPushButton, QMenu, QToolButton, QToolBox, QVBoxLayout,
                               QTreeView, QFileSystemModel, QFileDialog, QToolTip)
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
        title_label.setText('Режим виконання *')

        mode1 = QRadioButton()
        mode1.setObjectName('Mode1')
        mode1.setText('Звичайний (Лінукс сумісний)')

        mode2 = QRadioButton()
        mode2.setObjectName('Mode2')
        mode2.setText('Повний')
        mode2.setEnabled(False)

        layout.addWidget(title_label, 0, 0)
        layout.addWidget(mode1, 1, 0)
        layout.addWidget(mode2, 2, 0)


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
        self.setFixedSize(200, 100)

        layout = QGridLayout()

        label = QLabel('Долучайтесь до GitHub та\nробіть внесок щоб додати\nбільше мов')
        layout.addWidget(label, 1, 0)

        self.localization_list = QComboBox()
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
        layout.addWidget(Mode(), 2, 0)
        # layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), 3, 0)
        layout.setRowStretch(4, 1)
        layout.addWidget(back, 5, 0)

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
