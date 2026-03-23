import serial
import time

class Arduino():
    def __init__(self, porta, baudrate):
        try:
            self.arduino = serial.Serial(porta, baudrate, timeout=1)
        except:
            self.arduino = None
            print("Arduino não encontrado.")

    def enviar_comando(self, comando):
        if self.arduino: self.arduino.write(bytes([comando.value]))

    def ler_dados(self, tempo):
        tempo_inicio = time.time()

        while time.time() - tempo_inicio < tempo:
            if self.arduino.in_waiting:
                data = self.arduino.readline().decode().strip()
                print(data)