from PyQt6.QtWidgets import QWidget, QVBoxLayout

from frontend.widgets.manual_widget import ManualWidget

class ConfigurationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.manual_widget = ManualWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.manual_widget)

        self.setLayout(layout)