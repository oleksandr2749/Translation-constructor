from PySide6.QtWidgets import (QMenuBar, QComboBox, QGridLayout, QWidget, QLabel, QSizePolicy, QLineEdit, QSpacerItem,
                               QRadioButton, QButtonGroup, QPushButton, QMenu, QToolButton, QToolBox, QVBoxLayout,
                               QTreeView, QFileSystemModel, QFileDialog, QToolTip,QStatusBar)
from PySide6.QtCore import Qt, QPoint, QDir
from PySide6.QtGui import QIcon, QAction


class StatusBar(QStatusBar):
    def __init__(self, mods_number, parent=None):
        super().__init__(parent)
        self.setObjectName('StatusBar')

        mods_number = mods_number
        mods_number_label = QLabel()
        mods_number_label.setText(f'Кількість модифікацій: {mods_number}')
        self.addWidget(mods_number_label)
