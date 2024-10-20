from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QSizePolicy, QScrollBar,
                               QScrollArea, QSpacerItem, QFrame, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt, Signal


class MyLabel(QLabel):
    doubleClicked = Signal()

    def __init__(self, text='', parent=None):
        super().__init__(text, parent)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit()
