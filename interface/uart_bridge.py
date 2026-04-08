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
        raw_data = self.arduino.readline()
        data_string = raw_data.decode('utf-8').strip()

        if data_string:
            value = float(data_string)
            return value
        else:
            pass