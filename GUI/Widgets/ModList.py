import GUI.Widgets.MenuBar
import Main
import ModificationClass
import Process
import pathlib

from PySide6.QtWidgets import QMenuBar, QMenu, QComboBox, QWidgetAction, QGridLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QVBoxLayout, QScrollArea
from PySide6.QtCore import QRect, Qt, QPoint
from PySide6.QtGui import QIcon, QFont, QAction, QMouseEvent, QPalette, QColor


class QModLabel(QLabel):
    def __init__(self, mod, parent=None):
        super().__init__(text=mod.name, parent=parent)
        self.mod = mod

    def mousePressEvent(self, event: QMouseEvent):
        self.on_label_clicked()
        super().mousePressEvent(event)

    def on_label_clicked(self):
        Process.run(modification=self.mod, save_path=pathlib.Path(Main.config.get('Settings', 'export_path')))

    def __repr__(self):
        return f'Mod({self.mod})'


class ModList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName('ScrollArea')
        self.setStyleSheet('''QScrollBar:vertical {
                                margin: 8px 5px 8px 0px;
                                border: none;
                                border-radius: 4;
                                background: #222327;
                            }
                            QScrollBar::handle:vertical {
                                border: none;
                                border-radius: 3px;
                                background: #888888;
                            }
                            QScrollBar::add-line:vertical,
                            QScrollBar::sub-line:vertical {
                                border: none;
                            }
                            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                                border: none;
                            }''')

        self.modlistdata = ModificationClass.create_mod_list(ModificationClass.search_294100_folder())

        self.widget = QWidget()
        self.widget.setObjectName('ModList')
        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)
        self.setWidgetResizable(True)

        self.list_filling()
        self.layout.addStretch(1)

    def list_filling(self):
        font = QFont()
        font.setPointSize(14)
        mod_list = list()
        for mod in self.modlistdata:
            test_mod = QModLabel(mod=mod)
            test_mod.setObjectName('ListModLabel')
            test_mod.setFont(font)

            mod_list.append(test_mod)

        mod_list.sort(key=lambda mod: mod.mod.name)
        for mod in mod_list:
            self.layout.addWidget(mod)

    def filtering(self, test_filter):
        for i in self.findChildren(QLabel):
            '''i.show()
            print(f'{i} відображено')'''
            if (test_filter != ' ') and (test_filter.lower() in i.mod.name.lower()):
                i.show()
            else:
                i.hide()
