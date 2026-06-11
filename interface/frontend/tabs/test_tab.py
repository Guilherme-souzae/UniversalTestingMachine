from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from frontend.widgets.graph_widget import GraphWidget
from frontend.widgets.test_widget import TestWidget


class TestTab(QWidget):
    def __init__(self):
        super().__init__()

        self.force_graph = GraphWidget(
            "Força × Deslocamento"
        )

        self.stress_graph = GraphWidget(
            "Tensão × Deformação"
        )

        self.test_widget = TestWidget()

        graphs_layout = QHBoxLayout()

        graphs_layout.addWidget(
            self.force_graph,
            1
        )

        graphs_layout.addWidget(
            self.stress_graph,
            1
        )

        layout = QVBoxLayout()

        # gráficos ocupam a maior parte da tela
        layout.addLayout(graphs_layout, 1)

        # controles ficam no rodapé
        layout.addWidget(self.test_widget)

        self.setLayout(layout)