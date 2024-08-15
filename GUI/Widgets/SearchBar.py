from PySide6.QtWidgets import QMenuBar, QMenu, QComboBox, QWidgetAction, QGridLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QSizePolicy
from PySide6.QtCore import QRect, Qt, QPoint
from PySide6.QtGui import QIcon, QFont, QAction


class SearchBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('SearchBarWidget')
        self.setMinimumHeight(50)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 30, 0)
        self.setLayout(self.layout)

        self.sb_label = QLabel('Пошук за')
        self.sb_label.setObjectName('SearchLabel')

        self.sb_filter = QComboBox()
        self.sb_filter.setMinimumWidth(120)
        self.sb_filter.setObjectName('SearchFilterComboBox')
        self.sb_filter.addItem('назвою')
        self.sb_filter.addItem('авторством')
        self.sb_filter.addItem('айді')

        self.sb_separator = QLabel(':')
        self.sb_separator.setObjectName('SearchSeparatorLabel')

        self.sb_input_line = QLineEdit(clearButtonEnabled=True)
        self.sb_input_line.setObjectName('SearchLineEditor')
        self.sb_input_line.textChanged.connect(self.get_text)

        self.layout.addWidget(self.sb_label)
        self.layout.addSpacing(-5)
        self.layout.addWidget(self.sb_filter)
        self.layout.addWidget(self.sb_separator)
        self.layout.addWidget(self.sb_input_line)

        self.mod_list = None

    def get_text(self):
        self.mod_list.filtering(self.sb_input_line.text())

    def set_mod_list(self, mod_list):
        self.mod_list = mod_list
