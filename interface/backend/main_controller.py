from serial_bridge import Comando, SerialBridge

class MainController:
    def __init__(self):
        self.arduino = SerialBridge(9600, "COM3")

    def subir(self):
        print("Subir")
        self.arduino.enviar_comando(Comando.SUBIR)

    def descer(self):
        print("Descer")
        self.arduino.enviar_comando(Comando.DESCER)

    def parar(self):
        print("Parar")
        self.arduino.enviar_comando(Comando.PARAR)

    def start(self):
        print("Start")
        self.arduino.enviar_comando(Comando.ENSAIO)

    def pause(self):
        print("Pause")
        self.arduino.enviar_comando(Comando.PARAR)

    def reset(self):
        print("Reset")
        self.arduino.enviar_comando(Comando.R_ENSAIO)