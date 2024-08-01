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
    QSizePolicy, QSpacerItem, QVBoxLayout, QScrollArea
)
from PyQt6.QtSvgWidgets import QSvgWidget
import ModificationClass


class ModList(QWidget):
    def __init__(self):
        super().__init__()

        modlistdata = ModificationClass.create_mod_list(ModificationClass.search_294100_folder())

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.list_filling(modlistdata)

    def list_filling(self, mods):
        font = QFont()
        font.setPointSize(16)
        for mod in mods:
            test_mod = QLabel(mod.name)
            test_mod.setFont(font)

            self.layout.addWidget(test_mod)

    def filtering(self, test_filter):
        if not test_filter.strip():
            return

        for mod in self.findChildren(QLabel):
            if test_filter not in mod.text():
                mod.hide()
            else:
                continue


class TopButtonBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        author = QSvgWidget(str(Path('UI icons and style/user.svg')))
        author.setFixedSize(25, 25)
        layout.addWidget(author)


class SearchBar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        sb_label = QLabel('Пошук за')
        sb_label.setObjectName('Label')

        sb_filter = QComboBox()
        sb_filter.setObjectName('Filter')
        sb_filter.addItem('назвою')
        sb_filter.addItem('авторством')
        sb_filter.addItem('айді')
        sb_filter.setMinimumWidth(120)

        sb_separator = QLabel(':')
        sb_separator.setObjectName('Separator')

        sb_input_line = QLineEdit(clearButtonEnabled=True)
        sb_input_line.setObjectName('InputLine')
        sb_input_line.textChanged.connect(self.get_text)

        layout.addWidget(sb_label)
        layout.addSpacing(-5)
        layout.addWidget(sb_filter)
        layout.addWidget(sb_separator)
        layout.addWidget(sb_input_line)

    def get_text(self):
        test = self.findChildren(QLineEdit)
        print(f'{test[0].text()}')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Конструктор перекладу")
        self.setObjectName('MainWindow')
        self.resize(800, 600)
        self.setStyleSheet(Path('UI icons and style/UIStyle.qss').read_text())
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setVerticalSpacing(0)
        self.setLayout(main_layout)

        top_bar = QWidget()
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(0, 0, 0, 0)
        top_bar.setLayout(top_bar_layout)
        top_bar_palette = top_bar.palette()
        top_bar_palette.setColor(QPalette.ColorRole.Window, QColor("#2B2D30"))
        top_bar.setPalette(top_bar_palette)
        top_bar.setAutoFillBackground(True)
        top_bar.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        search_bar = SearchBar()
        top_bar_layout.addWidget(search_bar)

        top_bar_button = TopButtonBar()
        # top_bar_layout.addWidget(top_bar_button)

        mod_list = ModList()
        scroll = QScrollArea()
        scroll.setWidget(mod_list)

        main_layout.addWidget(top_bar, 0, 0)
        main_layout.addWidget(scroll, 1, 0)
        # main_layout.setRowStretch(1, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(Path('UI icons and style/UIStyle.qss').read_text())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
