import serial
import threading
import matplotlib.pyplot as plt

# Ajuste a porta para o seu Arduino
porta = "COM3"
baudrate = 9600
ser = serial.Serial(porta, baudrate, timeout=1)

# Listas para armazenar dados
tempos = []
pesos = []

# Flag para controle da coleta
medindo = False

# Thread para enviar comandos pelo teclado
def enviar_comando():
    while True:
        cmd = input("Digite comando (f=frente, b=tras, s=stop): ").strip()
        if cmd in ['f', 'b', 's']:
            ser.write(cmd.encode())

threading.Thread(target=enviar_comando, daemon=True).start()

print("Aguardando comandos...")

# Loop principal para receber dados do Arduino
while True:
    try:
        linha = ser.readline().decode().strip()
        if not linha:
            continue

        # Detecta marcadores do Arduino
        if linha == "START":
            print("Coleta iniciada")
            tempos.clear()
            pesos.clear()
            medindo = True
        elif linha == "STOP":
            print("Coleta finalizada")
            medindo = False
            break
        elif linha == "BACK":
            print("Motor girando para trás")
            medindo = False  # não coleta no modo "b"
        else:      
            # Recebe dados de tempo,peso
            if medindo and "," in linha:
                try:
                    t, p = linha.split(",")
                    tempos.append(int(t)/1000)  # ms → s
                    pesos.append(float(p))
                except:
                    pass
    except KeyboardInterrupt:
        break

ser.close()

# Plota gráfico força x tempo
plt.plot(tempos, pesos, marker='o')
plt.xlabel("Tempo (s)")
plt.ylabel("Peso (g)")
plt.title("Variação de Peso vs Tempo")
plt.grid(True)
plt.show()