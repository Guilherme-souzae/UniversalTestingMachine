from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from backend.serial_bridge import Comando, SerialBridge
from backend.firmware_configuration_entity import FirmwareConfiguration

class MainController(QObject):

    data_received = pyqtSignal(float)

    INTERVALO_LEITURA = 20 #MS
    VELOCIDADE_LINEAR = 0.0065 # M/S
    AREA_CORPO = 1 # M^2
    COMPRIMENTO_CORPO = 1

    def __init__(self):
        super().__init__()
        self.firmware_configuration = FirmwareConfiguration()
        self.serial_bridge = SerialBridge()

        self._timer = QTimer(self)
        self._timer.setInterval(self.INTERVALO_LEITURA)
        self._timer.timeout.connect(self._poll_serial)

    # ── configurações ─────────────────────────────────────

    def set_area_corpo(self, area_corpo):
        self.AREA_CORPO = area_corpo
        print(f"LOG: Area do corpo de prova = {area_corpo} m^2")

    def set_comprimento_corpo(self, comprimento_corpo):
        self.COMPRIMENTO_CORPO = comprimento_corpo
        print(f"LOG: Comprimento do corpo de prova = {comprimento_corpo} m")

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

    # ── envio de configurações ────────────────────────────

    def set_speed_configuracao(self, speed):
        self.firmware_configuration.speed = speed
        self._enviar_configuracao_callback()

    def _enviar_configuracao_callback(self):
        self.serial_bridge.enviar_comando(Comando.CONFIGURAR, self.firmware_configuration)

    # ── slot privado do timer ─────────────────────────────

    def _poll_serial(self):
        if not self.serial_bridge or not self.serial_bridge.conectado():
            self._timer.stop()
            return

        valor = self.serial_bridge.ler_dados()
        if valor is not None:
            self.data_received.emit(valor)
