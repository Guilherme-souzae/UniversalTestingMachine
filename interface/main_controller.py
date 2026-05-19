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
        self.arduino = None
        self.timer_leitura = QTimer()
        self.timer_leitura.timeout.connect(self._ler_dados)

        self._elapsed = QElapsedTimer()
        self._tempo_anterior_ms = 0
        self._tempo_total = 0.0
        self._contador_ref = 0

    def conectar_serial(self, porta: str, baud: int) -> bool:
        self.arduino = Arduino(porta, baud)
        if self.arduino == None:
            return False
        else:
            return True
        
    def desconectar_serial(self):
        if self.arduino != None:
            self.arduino.enviar_comando(Comando.PARAR)
            self.arduino.fechar_serial()
            self.arduino = None

    # --- Comandos de movimento ---
    def subir(self):
        if self.arduino == None: return
        print("enviando comando subir")
        self.arduino.enviar_comando(Comando.SUBIR)
    
    def descer(self):
        if self.arduino == None: return
        print("enviando comando descer")
        self.arduino.enviar_comando(Comando.DESCER)

    def parar(self):
        if self.arduino == None: return
        print("enviando comando parar")
        self.arduino.enviar_comando(Comando.PARAR)

    def reiniciar(self):
        if self.arduino == None: return
        print("enviando comando reiniciar")
        self.arduino.enviar_comando(Comando.RESET)

    ## --- Ensaio ---
    def iniciar_ensaio(self):
        if self.arduino == None: return
        print("enviando comando ensaio")
        self.arduino.enviar_comando(Comando.ENSAIO)
        self._elapsed.start()
        self._tempo_anterior_ms = 0
        self._tempo_total = 0.0
        self.timer_leitura.start(200)
        self.ensaio_iniciado.emit()

    def resetar_ensaio(self):
        if self.arduino == None: return
        print("enviando comando reiniciar ensaio")
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
        if self.arduino == None: return
        y = self.arduino.ler_dados()
        if y is not None:
            agora = self._elapsed.elapsed()
            delta = (agora - self._tempo_anterior_ms) / 1000.0
            self._tempo_anterior_ms = agora
            self._tempo_total += delta
            self.dados_recebidos.emit(self._tempo_total, y)
            print(f'recebendo leitura de dados x:{self._tempo_total} y:{y}')