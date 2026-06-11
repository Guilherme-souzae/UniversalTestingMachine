from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget
)

from frontend.widgets.emergency_widget import EmergencyWidget

from frontend.tabs.configuration_tab import ConfigurationTab
from frontend.tabs.test_tab import TestTab

from backend.main_controller import MainController

class MainWindow(QWidget):
    def __init__(self, main_controller: MainController):
        super().__init__()
        self.controller = main_controller

        # Montagem da interface
        self.setWindowTitle("Máquina de Ensaio")
        self.resize(1000, 700)

        self.emergency_widget = EmergencyWidget()

        self.tabs = QTabWidget()

        self.manual_tab = ConfigurationTab()
        self.test_tab = TestTab()

        self.tabs.addTab(self.manual_tab, "Controle Manual")
        self.tabs.addTab(self.test_tab, "Ensaio")

        layout = QVBoxLayout()

        layout.addWidget(self.emergency_widget)
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        # Conexão de sinais
        self.manual_tab.manual_widget.up_pressed.connect(self.controller.subir)
        self.manual_tab.manual_widget.down_pressed.connect(self.controller.descer)
        self.manual_tab.manual_widget.move_released.connect(self.controller.parar)

        self.test_tab.test_widget.start_clicked.connect(self.controller.start)
        self.test_tab.test_widget.pause_clicked.connect(self.controller.pause)
        self.test_tab.test_widget.reset_clicked.connect(self.controller.reset)