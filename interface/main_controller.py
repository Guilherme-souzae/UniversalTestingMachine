from PyQt6.QtCore import QTimer, QElapsedTimer, pyqtSignal, QObject
from uart_bridge import Arduino
from commands import Comando

class MainController(QObject):
    dados_recebidos = pyqtSignal(float, float)
    ensaio_iniciado = pyqtSignal()
    ensaio_resetado = pyqtSignal()
    referencia_salva = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.arduino = Arduino("COM12", 9600)
        self.timer_leitura = QTimer()
        self.timer_leitura.timeout.connect(self._ler_dados)

        self._elapsed = QElapsedTimer()
        self._tempo_anterior_ms = 0
        self._tempo_total = 0.0
        self._contador_ref = 0

    # --- Comandos de movimento ---
    def subir(self):
        self.arduino.enviar_comando(Comando.SUBIR)
    
    def descer(self):
        self.arduino.enviar_comando(Comando.DESCER)

    def reiniciar(self):
        self.arduino.enviar_comando(Comando.RESET)

    ## --- Ensaio ---
    def iniciar_ensaio(self):
        self.arduino.enviar_comando(Comando.ENSAIO)
        self._elapsed.start()
        self._tempo_anterior_ms = 0
        self._tempo_total = 0.0
        self.timer_leitura.start(200)
        self.ensaio_iniciado.emit()

    def resetar_ensaio(self):
        self.arduino.enviar_comando(Comando.R_ENSAIO)
        self.timer_leitura.stop()
        self.ensaio_resetado.emit()

    # --- Referências ---
    def salvar_referencia(self):
        self._contador_ref += 1
        nome = f"Referência {self._contador_ref}"
        self.referencia_salva.emit(nome)

    # --- Leitura periódica (privado) ---
    def _ler_dados(self):
        y = self.arduino.ler_dados()
        if y is not None:
            agora = self._elapsed.elapsed()
            delta = (agora - self._tempo_anterior_ms) / 1000.0
            self._tempo_anterior_ms = agora
            self._tempo_total += delta
            self.dados_recebidos.emit(self._tempo_total, y)