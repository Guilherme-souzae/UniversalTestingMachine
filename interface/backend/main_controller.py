from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from backend.serial_bridge import Comando, SerialBridge


class MainController(QObject):

    data_received = pyqtSignal(float)

    POLL_INTERVAL_MS = 20

    def __init__(self):
        super().__init__()
        self.arduino = None

        self._timer = QTimer(self)
        self._timer.setInterval(self.POLL_INTERVAL_MS)
        self._timer.timeout.connect(self._poll_serial)

    # ── conexão / desconexão ──────────────────────────────

    def link(self):
        self.arduino = SerialBridge()
        if self.arduino.conectado():
            print("Conexão estabelecida!")
        else:
            print("Falha na conexão!")

    def disconect(self):
        self._timer.stop()
        self.arduino.enviar_comando(Comando.PARAR)
        self.arduino.fechar_serial()
        self.arduino = None
        print("Conexão interrompida!")

    # ── controle manual ───────────────────────────────────

    def subir(self):
        self.arduino.enviar_comando(Comando.SUBIR)

    def descer(self):
        self.arduino.enviar_comando(Comando.DESCER)

    def parar(self):
        self.arduino.enviar_comando(Comando.PARAR)

    # ── ensaio ────────────────────────────────────────────

    def start(self):
        self.arduino.enviar_comando(Comando.ENSAIO)
        self._timer.start()

    def pause(self):
        self._timer.stop()
        self.arduino.enviar_comando(Comando.PARAR)

    def reset(self):
        self._timer.stop()
        self.arduino.enviar_comando(Comando.PARAR)

    # ── slot privado do timer ─────────────────────────────

    def _poll_serial(self):
        if not self.arduino or not self.arduino.conectado():
            self._timer.stop()
            return

        valor = self.arduino.ler_dados()
        if valor is not None:
            self.data_received.emit(valor)