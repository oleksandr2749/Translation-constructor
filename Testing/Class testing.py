from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

app = QApplication([])

# Створюємо основний віджет
main_widget = QWidget()
main_widget.setWindowTitle('Main Widget')
main_widget.resize(300, 200)

# Створюємо перший QLabel (батьківський)
parent_label = QLabel('Parent Label')

# Створюємо другий QLabel (дочірній)
child_label = QLabel('Child Label')

# Створюємо контейнер для макету
container_widget = QWidget()
container_layout = QVBoxLayout(container_widget)
container_layout.addWidget(parent_label)
container_layout.addWidget(child_label)

# Додаємо контейнер до основного віджету
main_layout = QVBoxLayout(main_widget)
main_layout.addWidget(container_widget)

# Показуємо основний віджет
main_widget.show()

# Приховати батьківський QLabel через 2 секунди як приклад
from PySide6.QtCore import QTimer

def hide_parent_label():
    parent_label.setVisible(False)

QTimer.singleShot(2000, hide_parent_label)

app.exec()
