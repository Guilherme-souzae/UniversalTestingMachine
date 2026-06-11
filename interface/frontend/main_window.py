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

        self.conf_tab = ConfigurationTab()
        self.test_tab = TestTab()

        self.tabs.addTab(self.conf_tab, "Controle Manual")
        self.tabs.addTab(self.test_tab, "Ensaio")

        layout = QVBoxLayout()

        layout.addWidget(self.emergency_widget)
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        # Conexão de sinais

        # Dados do ensaio → gráfico
        self.controller.data_received.connect(self._on_data_received)

        # Botão de emergência
        self.emergency_widget.emergency_clicked.connect(self.controller.disconect)

        # Controle manual
        self.conf_tab.manual_widget.up_pressed.connect(self.controller.subir)
        self.conf_tab.manual_widget.down_pressed.connect(self.controller.descer)
        self.conf_tab.manual_widget.move_released.connect(self.controller.parar)

        #Controle de ensaio
        self.test_tab.test_widget.start_clicked.connect(self.controller.start)
        self.test_tab.test_widget.pause_clicked.connect(self.controller.pause)
        self.test_tab.test_widget.reset_clicked.connect(self.controller.reset)
        self.test_tab.test_widget.reset_clicked.connect(self.test_tab.force_graph.clear)

        # Conexão serial
        self.conf_tab.connection_widget.connect_requested.connect(self.controller.link)

    def _on_data_received(self, valor: float):
        n = len(self.test_tab.force_graph.x_data)
        self.test_tab.force_graph.add_point(n, valor)