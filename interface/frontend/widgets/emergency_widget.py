from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class EmergencyWidget(QWidget):

    emergency_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.btn_emergency = QPushButton("EMERGÊNCIA")
        self.btn_emergency.setObjectName("emergencyButton")

        self.btn_emergency.setMinimumHeight(60)

        self.btn_emergency.clicked.connect(self.emergency_clicked.emit)

        layout = QHBoxLayout()
        layout.addWidget(self.btn_emergency)

        self.setLayout(layout)