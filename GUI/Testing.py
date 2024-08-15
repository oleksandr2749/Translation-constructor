class TopButtonBar(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.author = QSvgWidget(str(Path('GUI/Icons and style/user.svg')))
        self.author.setFixedSize(25, 25)
        self.layout.addWidget(self.author)