import serial

class Arduino():
    def __init__(self, porta, baudrate):
        try:
            self.arduino = serial.Serial(porta, baudrate, timeout=1)
        except:
            self.arduino = None
            print("Arduino não encontrado.")

    def enviar_comando(self, comando):
        if self.arduino: self.arduino.write(bytes([comando.value]))