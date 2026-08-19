from enum import Enum
import json
import serial
from serial.tools import list_ports


class Comando(str, Enum):
    SUBIR = "SUBIR"
    DESCER = "DESCER"
    PARAR = "PARAR"
    RESET = "RESET"
    ENSAIO = "ENSAIO"
    CONFIGURAR = "CONFIGURAR"


class SerialBridge:

    BAUDRATE = 9600

    def __init__(self):
        self.arduino = None
        self._buffer = ""

    def _encontrar_arduino(self):
        portas = list(list_ports.comports())

        for porta in portas:
            descricao = (porta.description or "").lower()
            if (
                "arduino" in descricao
                or "ch340" in descricao
                or "cp210" in descricao
                or "usb serial" in descricao
                or "usb single serial" in descricao
            ):
                return porta.device

        if len(portas) == 1:
            return portas[0].device

        return None

    def conectado(self):
        return self.arduino is not None and self.arduino.is_open

    def conectar(self):
        if self.arduino:
            try:
                self.arduino.close()
            except Exception:
                pass

        porta = self._encontrar_arduino()

        if porta is None:
            print("WARNING: Arduino não encontrado")
            self.arduino = None
            return False

        try:
            self.arduino = serial.Serial(porta, self.BAUDRATE, timeout=0)
            print(f"LOG: Arduino conectado em {porta}")
            return True

        except serial.SerialException as e:
            print(f"WARNING: Erro ao conectar: {e}")
            self.arduino = None
            return False

    def fechar_serial(self):
        if self.conectado():
            self.arduino.close()
            self.arduino = None

    def enviar_comando(self, comando, payload=None):
        if not self.conectado():
            print("WARNING: Arduino não conectado")
            return

        # CORREÇÃO 1: Trata 'comando' aceitando tanto a Enum Comando quanto uma String simples
        cmd_str = comando.value if isinstance(comando, Enum) else str(comando)

        mensagem = {"comando": cmd_str}

        # CORREÇÃO 2: Converte obrigatoriamente o payload para String para o C++ ler corretamente
        if payload is not None:
            mensagem["payload"] = str(payload)

        json_str = json.dumps(mensagem)

        # Envia a string terminada com '\n' como buffer UTF-8
        self.arduino.write((json_str + "\n").encode("utf-8"))

        print(f"LOG: Enviado -> {json_str}")

    def ler_dados(self):
        if not self.conectado():
            print("WARNING: Arduino não conectado")
            return None

        return 1.0

        raw = self.arduino.read(self.arduino.in_waiting or 1)

        self._buffer += raw.decode("utf-8", errors="ignore")

        if "\n" in self._buffer:
            linha, self._buffer = self._buffer.split("\n", 1)
            linha = linha.strip()

            if linha:
                try:
                    return float(linha)
                except ValueError:
                    pass

        return None