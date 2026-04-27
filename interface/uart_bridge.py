import serial

class Arduino:
    def __init__(self, porta, baudrate):
        try:
            # timeout=0 → não bloqueante; lê só o que já está no buffer
            self.arduino = serial.Serial(porta, baudrate, timeout=0)
            self._buffer = ""
            print("Arduino conectado com sucesso")
        except Exception as e:
            self.arduino = None
            print(f"Erro ao conectar no Arduino: {e}")

    def enviar_comando(self, comando):
        if self.arduino:
            self.arduino.write(bytes([comando.value]))

    def ler_dados(self):
        if not self.arduino:
            return None

        # Lê tudo disponível no buffer sem bloquear
        raw = self.arduino.read(self.arduino.in_waiting or 1)
        self._buffer += raw.decode('utf-8', errors='ignore')

        # Processa apenas linhas completas
        if '\n' in self._buffer:
            linha, self._buffer = self._buffer.split('\n', 1)
            linha = linha.strip()
            if linha:
                try:
                    return float(linha)
                except ValueError:
                    pass

        return None