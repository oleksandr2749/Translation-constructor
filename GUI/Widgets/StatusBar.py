# This file is part of Translation Constructor.
#
# Translation Constructor is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Translation Constructor is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with Translation Constructor.
# If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import QLabel, QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, mods_number, parent=None):
        super().__init__(parent)
        self.setObjectName('StatusBar')

        mods_number = mods_number
        mods_number_label = QLabel()
        mods_number_label.setText(f'Кількість модифікацій: {mods_number}')
        self.addWidget(mods_number_label)
