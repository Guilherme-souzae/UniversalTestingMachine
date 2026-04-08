from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraficoCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.buffer_x = []
        self.buffer_y = []
        super().__init__(self.fig)

    def plotar(self):
        self.ax.clear()
        self.ax.plot(self.buffer_x, self.buffer_y)
        self.ax.set_ylim(0, 1023)
        self.draw()

    def adicionar_ponto(self, x , y):
        print(f'X: {type(x)} Y: {type(y)}')
        self.buffer_x.append(x)
        self.buffer_y.append(y)

    def resetar_grafico(self):
        self.buffer_x = []
        self.buffer_y = []