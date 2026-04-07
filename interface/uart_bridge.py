import serial

class Arduino():
    def __init__(self, porta, baudrate):
        try:
            self.arduino = serial.Serial(porta, baudrate, timeout=1)
        except Exception as e:
            self.arduino = None
            print(f"Erro ao conectar no Arduino: {e}")

    def enviar_comando(self, comando):
        if self.arduino: self.arduino.write(bytes([comando.value]))

    def ler_dados(self):
        data = self.arduino.readline().decode().strip()
        print(data)