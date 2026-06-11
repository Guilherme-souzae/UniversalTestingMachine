from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class EmergencyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.btn_emergency = QPushButton("EMERGÊNCIA")
        self.btn_emergency.setObjectName("emergencyButton")

        self.btn_emergency.setMinimumHeight(60)

        layout = QHBoxLayout()
        layout.addWidget(self.btn_emergency)

        self.setLayout(layout)