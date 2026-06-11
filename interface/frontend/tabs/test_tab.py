from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

from frontend.widgets.test_widget import TestWidget

class TestTab(QWidget):
    def __init__(self):
        super().__init__()

        self.test_widget = TestWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.test_widget)

        self.setLayout(layout)