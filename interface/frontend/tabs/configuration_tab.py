from PyQt6.QtWidgets import QWidget, QVBoxLayout

from frontend.widgets.manual_widget import ManualWidget
from frontend.widgets.conection_widget import ConnectionWidget

class ConfigurationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.manual_widget = ManualWidget()
        self.connection_widget = ConnectionWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.manual_widget)
        layout.addWidget(self.connection_widget)

        self.setLayout(layout)