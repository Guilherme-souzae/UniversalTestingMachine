import serial
from serial.tools import list_ports
from enum import IntEnum


class Comando(IntEnum):
    SUBIR = 0
    DESCER = 1
    PARAR = 2
    RESET = 3
    ENSAIO = 4


class SerialBridge:

    BAUDRATE = 9600

    def __init__(self):
        self.arduino = None
        self._buffer = ""

        porta = self._encontrar_arduino()

        if porta is None:
            print("WARNING: Arduino não encontrado")
            return

        try:
            self.arduino = serial.Serial(
                porta,
                self.BAUDRATE,
                timeout=0
            )

            print(
                f"LOG: Arduino conectado com sucesso em {porta}"
            )

        except Exception as e:
            print(
                f"WARNING: Erro ao conectar ao Arduino: {e}"
            )

    def _encontrar_arduino(self):
        portas = list(list_ports.comports())

        # Tenta identificar por descrição
        for porta in portas:

            descricao = (
                porta.description or ""
            ).lower()

            if (
                "arduino" in descricao
                or "ch340" in descricao
                or "cp210" in descricao
                or "usb serial" in descricao
            ):
                return porta.device

        # Fallback:
        # se existe apenas uma serial, assume que é ela
        if len(portas) == 1:
            return portas[0].device

        return None

    def conectado(self):
        return (
            self.arduino is not None
            and self.arduino.is_open
        )

    def conectar(self):
        if self.arduino:
            try:
                self.arduino.close()
            except:
                pass

        porta = self._encontrar_arduino()

        if porta is None:
            print("WARNING: Arduino não encontrado")
            self.arduino = None
            return False

        try:
            self.arduino = serial.Serial(
                porta,
                self.BAUDRATE,
                timeout=0
            )

            print(
                f"LOG: Arduino conectado em {porta}"
            )

            return True

        except serial.SerialException as e:
            print(
                f"WARNING: Erro ao conectar: {e}"
            )
            self.arduino = None
            return False

    def fechar_serial(self):
        if self.conectado():
            self.arduino.close()
            self.arduino = None

    def enviar_comando(self, comando):
        if self.conectado():
            self.arduino.write(
                bytes([comando.value])
            )
        else:
            print("WARNING: Arduino não conectado")

    def ler_dados(self):
        if not self.conectado():
            print("WARNING: Arduino não conectado")
            return None

        raw = self.arduino.read(
            self.arduino.in_waiting or 1
        )

        self._buffer += raw.decode(
            "utf-8",
            errors="ignore"
        )

        if "\n" in self._buffer:

            linha, self._buffer = (
                self._buffer.split("\n", 1)
            )

            linha = linha.strip()

            if linha:
                try:
                    return float(linha)
                except ValueError:
                    pass

        return None