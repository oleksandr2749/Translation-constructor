from PySide6.QtWidgets import QMenuBar, QMenu, QComboBox, QWidgetAction, QGridLayout, QWidget, QLabel, QSizePolicy, QLineEdit, QMainWindow
from PySide6.QtCore import QRect, Qt, QPoint
from PySide6.QtGui import QIcon, QFont, QAction, QPalette, QColor

from GUI.Widgets.SearchBar import SearchBar


class TopBar(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName('TopBarWidget')

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.search_bar = SearchBar()
        self.layout.addWidget(self.search_bar, 0, 0)
