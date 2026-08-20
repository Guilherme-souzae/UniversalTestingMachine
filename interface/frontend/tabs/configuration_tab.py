from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from frontend.widgets.manual_widget import ManualWidget
from frontend.widgets.conection_widget import ConnectionWidget
from frontend.widgets.geometry_widget import GeometryWidget


class ConfigurationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.manual_widget = ManualWidget()
        self.connection_widget = ConnectionWidget()
        self.geometry_widget = GeometryWidget()

        # ==========================================================
        # Coluna esquerda
        # ==========================================================

        left_column = QVBoxLayout()
        left_column.setSpacing(15)

        left_column.addWidget(self.manual_widget)
        left_column.addWidget(self.connection_widget)
        left_column.addStretch()

        # ==========================================================
        # Coluna direita
        # ==========================================================

        right_column = QVBoxLayout()
        right_column.setSpacing(15)

        right_column.addWidget(self.geometry_widget)
        right_column.addStretch()

        # ==========================================================
        # Layout principal
        # ==========================================================

        layout = QHBoxLayout()

        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addLayout(left_column, 1)
        layout.addLayout(right_column, 1)

        self.setLayout(layout)