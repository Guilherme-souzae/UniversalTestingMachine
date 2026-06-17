from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from backend.serial_bridge import Comando, SerialBridge


class MainController(QObject):

    data_received = pyqtSignal(float)

    POLL_INTERVAL_MS = 20

    def __init__(self):
        super().__init__()
        self.serial_bridge = SerialBridge()

        self._timer = QTimer(self)
        self._timer.setInterval(self.POLL_INTERVAL_MS)
        self._timer.timeout.connect(self._poll_serial)

    # ── conexão / desconexão ──────────────────────────────

    def link(self):
        self.serial_bridge.conectar()

        if self.serial_bridge.conectado():
            print("LOG: Conexão estabelecida!")
        else:
            print("WARNING: Falha na conexão!")

    def disconect(self):
        self._timer.stop()
        self.serial_bridge.enviar_comando(Comando.PARAR)
        self.serial_bridge.fechar_serial()
        print("LOG: Conexão interrompida!")

    # ── controle manual ───────────────────────────────────

    def subir(self):
        self.serial_bridge.enviar_comando(Comando.SUBIR)

    def descer(self):
        self.serial_bridge.enviar_comando(Comando.DESCER)

    def parar(self):
        self.serial_bridge.enviar_comando(Comando.PARAR)

    # ── ensaio ────────────────────────────────────────────

    def start(self):
        self.serial_bridge.enviar_comando(Comando.ENSAIO)
        self._timer.start()

    def pause(self):
        self._timer.stop()
        self.serial_bridge.enviar_comando(Comando.PARAR)

    def reset(self):
        self._timer.stop()
        self.serial_bridge.enviar_comando(Comando.PARAR)

    # ── slot privado do timer ─────────────────────────────

    def _poll_serial(self):
        if not self.serial_bridge or not self.serial_bridge.conectado():
            self._timer.stop()
            return

        valor = self.serial_bridge.ler_dados()
        if valor is not None:
            self.data_received.emit(valor)