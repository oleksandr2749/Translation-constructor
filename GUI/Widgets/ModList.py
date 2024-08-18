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

        self.i = QPackageId(mod)
        self.a = QAuthor(mod)

    def show(self):
        super().show()
        self.i.show()
        self.a.show()

    def hide(self):
        super().hide()
        self.i.hide()
        self.a.hide()

    def mousePressEvent(self, event: QMouseEvent):
        self.on_label_clicked()
        super().mousePressEvent(event)

    def on_label_clicked(self):
        Process.run(modification=self.mod, export_path=pathlib.Path(Main.config.get('Settings', 'export_path')))


class QAttribute(QLabel):
    def __init__(self, text, parent=None, object_name=None, color='gray'):
        super().__init__(text=text, parent=parent)
        self.setObjectName(object_name)
        self.setStyleSheet(f'#{object_name} {{ color: {color};}}')


class QPackageId(QAttribute):
    def __init__(self, mod, parent=None):
        super().__init__(text=mod.published_file_Id, parent=parent, object_name='PackageId')


class QAuthor(QAttribute):
    def __init__(self, mod, parent=None):
        super().__init__(text=mod.author, parent=parent, object_name='Author')


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
            mod_list.append(test_mod.i)
            mod_list.append(test_mod.a)

        #mod_list.sort(key=lambda mod: mod.mod.name)

        for mod in mod_list:
            self.layout.addWidget(mod)

    def filtering(self, test_filter):
        for i in self.findChildren(QModLabel):
            if (test_filter != ' ') and (test_filter.lower() in i.mod.name.lower()):
                i.show()
            else:
                i.hide()

    def mods_group(self, mod_list):
        for previous, current in zip(mod_list[:-1], mod_list[1:]):
            # print(f'Поточний:{current} Попередній: {previous}')
            # print(current.mod.name)
            for current_first_word, previous_first_word in zip(current.mod.name, previous.mod.name):
                # print(f'{previous.mod.name} {previous_first_word} та {current.mod.name} {current_first_word}')

                if current_first_word != previous_first_word:
                    # print(f'{previous.mod.name} та {current.mod.name} моди не однієї групи')
                    break
                elif (current_first_word == ' ') and (previous_first_word == ' '):
                    QLabel(f'{previous.mod.name}------------------------------------------')
                    print(f'{previous.mod.name} та {current.mod.name} моди однієї групи')
                    break
