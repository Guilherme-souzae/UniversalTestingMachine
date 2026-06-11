from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
)

class ConnectionWidget(QWidget):

    connect_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        group = QGroupBox("Conexão")

        self.btn_connect = QPushButton(
            "CONECTAR AO ARDUINO"
        )

        self.btn_connect.setObjectName("connectButton")

        self.btn_connect.setMinimumHeight(60)

        self.btn_connect.clicked.connect(
            self.connect_requested.emit
        )

        group_layout = QVBoxLayout()
        group_layout.addWidget(self.btn_connect)

        group.setLayout(group_layout)

        layout = QVBoxLayout()
        layout.addWidget(group)

        self.setLayout(layout)