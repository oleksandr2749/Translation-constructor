import sys
from pathlib import Path
from PyQt6.QtCore import (
    Qt
)
from PyQt6.QtGui import (
    QPalette, QColor, QPixmap, QPainter, QFont
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QHBoxLayout, QComboBox,
    QSizePolicy, QSpacerItem, QVBoxLayout, QScrollArea, QListWidget
)
from PyQt6.QtSvgWidgets import QSvgWidget
import ModificationClass


class ModList(QWidget):
    def __init__(self):
        super().__init__()

        modlistdata = ModificationClass.create_mod_list(ModificationClass.search_294100_folder())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.mod_list = list()
        self.list_filling(modlistdata)
        self.layout.addStretch(1)

    def list_filling(self, mods):
        font = QFont()
        font.setPointSize(14)
        for mod in mods:
            test_mod = QLabel(mod.name)
            test_mod.setFont(font)

            self.layout.addWidget(test_mod)
            self.mod_list.append(test_mod)

    def filtering(self, test_filter):
        for i in self.findChildren(QWidget):
            i.show()
        for mod in self.findChildren(QWidget):
            if test_filter.lower() not in mod.text().lower():
                mod.hide()
            elif test_filter.lower() in mod.text().lower():
                continue


class TopButtonBar(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.author = QSvgWidget(str(Path('UI icons and style/user.svg')))
        self.author.setFixedSize(25, 25)
        self.layout.addWidget(self.author)


class SearchBar(QWidget):
    def __init__(self, mod_list):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.sb_label = QLabel('Пошук за')
        self.sb_label.setObjectName('Label')

        self.sb_filter = QComboBox()
        self.sb_filter.setObjectName('Filter')
        self.sb_filter.addItem('назвою')
        self.sb_filter.addItem('авторством')
        self.sb_filter.addItem('айді')
        self.sb_filter.setMinimumWidth(120)

        self.sb_separator = QLabel(':')
        self.sb_separator.setObjectName('Separator')

        self.sb_input_line = QLineEdit(clearButtonEnabled=True)
        self.sb_input_line.setObjectName('InputLine')
        self.sb_input_line.textChanged.connect(self.get_text)

        self.layout.addWidget(self.sb_label)
        self.layout.addSpacing(-5)
        self.layout.addWidget(self.sb_filter)
        self.layout.addWidget(self.sb_separator)
        self.layout.addWidget(self.sb_input_line)

        self.mod_list = mod_list

    def get_text(self):
        self.mod_list.filtering(self.sb_input_line.text())


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Конструктор перекладу")
        self.setObjectName('MainWindow')
        self.resize(800, 600)
        self.setStyleSheet(Path('UI icons and style/UIStyle.qss').read_text())
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setVerticalSpacing(0)
        self.setLayout(self.layout)

        self.top_bar = QWidget()
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar.setLayout(self.top_bar_layout)
        self.top_bar_palette = self.top_bar.palette()
        self.top_bar_palette.setColor(QPalette.ColorRole.Window, QColor("#3B3F44"))
        self.top_bar.setPalette(self.top_bar_palette)
        self.top_bar.setAutoFillBackground(True)
        self.top_bar.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.mod_list = ModList()
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mod_list)

        self.search_bar = SearchBar(self.mod_list)
        self.top_bar_layout.addWidget(self.search_bar)

        top_bar_button = TopButtonBar()
        #top_bar_layout.addWidget(top_bar_button)

        self.layout.addWidget(self.top_bar, 0, 0)
        self.layout.addWidget(self.scroll, 1, 0)
        self.layout.setRowStretch(1, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(Path('UI icons and style/UIStyle.qss').read_text())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
