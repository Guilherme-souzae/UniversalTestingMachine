from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

class ManualWidget(QWidget):

    # Sinais
    up_pressed = pyqtSignal()
    down_pressed = pyqtSignal()
    move_released = pyqtSignal()

    def __init__(self):
        super().__init__()

        group = QGroupBox("Controle Manual")

        self.btn_up = QPushButton("▲ SUBIR")
        self.btn_down = QPushButton("▼ DESCER")

        self.btn_up.setObjectName("upButton")
        self.btn_down.setObjectName("downButton")

        self.btn_up.pressed.connect(self.up_pressed.emit)
        self.btn_down.pressed.connect(self.down_pressed.emit)
        self.btn_up.released.connect(self.move_released.emit)
        self.btn_down.released.connect(self.move_released.emit)

        self.btn_up.setMinimumHeight(60)
        self.btn_down.setMinimumHeight(60)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.btn_up)
        buttons_layout.addWidget(self.btn_down)

        group_layout = QVBoxLayout()
        group_layout.addLayout(buttons_layout)

        group.setLayout(group_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group)

        self.setLayout(main_layout)