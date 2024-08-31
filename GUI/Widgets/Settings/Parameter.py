from PySide6.QtWidgets import QRadioButton


class RadioButton(QRadioButton):
    def __init__(self):
        super().__init__()
        self.importance = False

    def setImportance(self, value: bool):
        self.importance = value
