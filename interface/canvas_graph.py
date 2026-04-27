from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraficoCanvas(FigureCanvas):
    def __init__(self, minY=-100, maxY=100):
        self.fig = Figure(tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        self.minY = minY
        self.maxY = maxY

        self.buffer_x = []
        self.buffer_y = []

        # Cria a linha UMA vez — só atualiza os dados depois
        (self.linha,) = self.ax.plot([], [])
        self.ax.set_ylim(self.minY, self.maxY)

        super().__init__(self.fig)

    def plotar(self):
        self.linha.set_data(self.buffer_x, self.buffer_y)

        # Ajusta eixo X automaticamente conforme os dados crescem
        if self.buffer_x:
            self.ax.set_xlim(0, max(self.buffer_x) * 1.05 or 1)

        # Redesenha só o necessário (muito mais rápido que draw())
        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.linha)
        self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.flush_events()

    def adicionar_ponto(self, x, y):
        self.buffer_x.append(x)
        self.buffer_y.append(y)

    def resetar_grafico(self):
        self.buffer_x = []
        self.buffer_y = []
        self.linha.set_data([], [])
        self.draw()  # redesenho completo só no reset