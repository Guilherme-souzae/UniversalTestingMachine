from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from frontend.widgets.manual_widget import ManualWidget
from frontend.widgets.conection_widget import ConnectionWidget
from frontend.widgets.halting_widget import HaltingWidget
from frontend.widgets.report_widget import ReportWidget
from frontend.widgets.geometry_widget import GeometryWidget


class ConfigurationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.manual_widget = ManualWidget()
        self.halting_widget = HaltingWidget()
        self.connection_widget = ConnectionWidget()
        self.report_widget = ReportWidget()
        self.geometry_widget = GeometryWidget()

        # --- Coluna esquerda ---
        left_column = QVBoxLayout()
        left_column.addWidget(self.manual_widget)
        left_column.addWidget(self.halting_widget)
        left_column.addWidget(self.connection_widget)
        left_column.addStretch()

        # --- Coluna direita ---
        right_column = QVBoxLayout()
        right_column.addWidget(self.geometry_widget)
        right_column.addWidget(self.report_widget)
        right_column.addStretch()

        # --- Layout principal (duas colunas lado a lado) ---
        layout = QHBoxLayout()
        layout.addLayout(left_column)
        layout.addLayout(right_column)

        self.setLayout(layout)