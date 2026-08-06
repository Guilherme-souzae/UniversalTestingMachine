from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class GraphWidget(QWidget):
    def __init__(self, title: str):
        super().__init__()

        self.x_data = []
        self.y_data = []

        self.x_data.append(0)
        self.y_data.append(0)

        self.graph = pg.PlotWidget()
        self.graph.setTitle(title)

        self.curve = self.graph.plot()

        layout = QVBoxLayout()
        layout.addWidget(self.graph)

        self.setLayout(layout)

    def clear(self):
        self.x_data.clear()
        self.y_data.clear()

        self.curve.setData([], [])

    def add_point(self, x, y):
        x1 = self.x_data[-1]
        x2 = x1 + x
        self.x_data.append(x2)
        self.y_data.append(y)

        self.update_plot()

    def set_data(self, x_data, y_data):
        self.x_data = list(x_data)
        self.y_data = list(y_data)

        self.update_plot()

    def update_plot(self):
        self.curve.setData(self.x_data, self.y_data)