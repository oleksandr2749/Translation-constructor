from PySide6.QtWidgets import (QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy, QFileDialog, QScrollArea,
                               QHBoxLayout, QVBoxLayout)
from PySide6.QtCore import Qt

from pathlib import Path


class RecentList(QScrollArea):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def add(self, path):
        label = QLabel(Path(path).name)
        self.layout.addWidget(label)
