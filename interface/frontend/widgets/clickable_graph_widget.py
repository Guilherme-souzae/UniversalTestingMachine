from PyQt6.QtCore import Qt, pyqtSignal
import pyqtgraph as pg

from .graph_widget import GraphWidget


class ClickableGraphWidget(GraphWidget):

    young_modulus_calculated = pyqtSignal(float)

    def __init__(self, title: str):
        super().__init__(title)

        self.selected_points = []
        self.markers = []

        self.graph.scene().sigMouseClicked.connect(
            self._on_mouse_clicked
        )

    def _on_mouse_clicked(self, event):

        if event.button() != Qt.MouseButton.LeftButton:
            return

        if len(self.x_data) == 0:
            return

        mouse_position = event.scenePos()

        graph_position = self.graph.plotItem.vb.mapSceneToView(
            mouse_position
        )

        clicked_x = graph_position.x()

        index = min(
            range(len(self.x_data)),
            key=lambda i: abs(self.x_data[i] - clicked_x)
        )

        x = self.x_data[index]
        y = self.y_data[index]

        self._select_point(index, x, y)

    def _select_point(self, index, x, y):

        if len(self.selected_points) >= 2:
            self.clear_selection()

        self.selected_points.append((index, x, y))

        marker = pg.ScatterPlotItem(
            x=[x],
            y=[y],
            size=12,
            brush="red",
            pen="white"
        )

        self.graph.addItem(marker)
        self.markers.append(marker)

        if len(self.selected_points) == 2:
            young_modulus = self._calculate_young_modulus()

            if young_modulus is not None:
                self.young_modulus_calculated.emit(
                    young_modulus
                )

    def _calculate_young_modulus(self):

        index1 = self.selected_points[0][0]
        index2 = self.selected_points[1][0]

        start = min(index1, index2)
        end = max(index1, index2)

        x = self.x_data[start:end + 1]
        y = self.y_data[start:end + 1]

        n = len(x)

        if n < 2:
            return None

        sum_x = sum(x)
        sum_y = sum(y)

        sum_x_squared = sum(value ** 2 for value in x)
        sum_xy = sum(
            x[i] * y[i]
            for i in range(n)
        )

        denominator = (
            n * sum_x_squared
            - sum_x ** 2
        )

        if denominator == 0:
            return None

        slope = (
            n * sum_xy
            - sum_x * sum_y
        ) / denominator

        return slope

    def clear_selection(self):

        self.selected_points.clear()

        for marker in self.markers:
            self.graph.removeItem(marker)

        self.markers.clear()

    def get_selected_points(self):

        return [
            (x, y)
            for _, x, y in self.selected_points
        ]