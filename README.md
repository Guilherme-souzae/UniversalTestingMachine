# 🔬 Interface de Ensaio com Arduino

Interface desktop em Python para controle de um sistema de ensaio mecânico com motor de passo e célula de carga, comunicando-se com um microcontrolador Arduino via porta Serial.

---

## 🚀 Como Rodar

### Pré-requisitos

- Python 3.10+
- Arduino com o firmware `firmware.ino` gravado
- Cabo USB conectado ao Arduino

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Executando

```bash
python main.py
```

---

## 📁 Estrutura do Projeto

```
interface/
├── backend/
│   ├── main_controller.py   # Lógica de controle e orquestração
│   └── serial_bridge.py     # Abstração da comunicação serial
│
├── frontend/
│   ├── tabs/
│   │   ├── configuration_tab.py  # Aba de configurações
│   │   └── test_tab.py           # Aba principal do ensaio
│   │
│   └── widgets/
│       ├── conection_widget.py   # Botão de conexão com o Arduino
│       ├── emergency_widget.py   # Botão de emergência
│       ├── graph_widget.py       # Gráfico em tempo real
│       ├── manual_widget.py      # Controle manual (subir/descer)
│       └── test_widget.py        # Controle do ensaio (iniciar/pausar/resetar)
│
├── main_window.py   # Janela principal — conecta sinais ao controller
├── styles.py        # Folha de estilos global (dark theme)
└── main.py          # Ponto de entrada da aplicação
```

---

## 🏛️ Arquitetura

O projeto segue um modelo em três camadas com comunicação por sinais Qt, mantendo o frontend completamente desacoplado do hardware.

```
┌─────────────────────────────────────────────────────┐
│                     FRONTEND                        │
│                                                     │
│  Widgets  ──pyqtSignal──▶  MainWindow               │
│  (UI pura, sem lógica)      (conecta sinais)        │
└────────────────────────┬────────────────────────────┘
                         │ chama métodos
┌────────────────────────▼────────────────────────────┐
│                     BACKEND                         │
│                                                     │
│  MainController  ──▶  SerialBridge                  │
│  (orquestra ações)    (escreve na porta serial)     │
└────────────────────────┬────────────────────────────┘
                         │ USB / Serial (9600 baud)
┌────────────────────────▼────────────────────────────┐
│                    FIRMWARE                         │
│                                                     │
│  Arduino  ──▶  Motor de Passo  +  Célula de Carga   │
└─────────────────────────────────────────────────────┘
```

### Camadas

**Widgets**
Cada widget é um componente visual independente que expõe `pyqtSignal`s públicos. Não conhecem o Arduino nem o controller — apenas emitem eventos (ex: `emergency_clicked`, `up_pressed`, `start_clicked`).

**MainWindow**
Instancia os widgets e o controller, e realiza todas as conexões `.connect()` entre os sinais dos widgets e os métodos do `MainController`. É o único ponto de acoplamento entre frontend e backend.

**MainController**
Recebe as chamadas da `MainWindow` e as traduz em comandos para o `SerialBridge`. Também gerencia o estado da conexão com o Arduino.

**SerialBridge**
Abstrai a porta serial. Converte os `Enum` de comando em bytes e os envia ao Arduino. Também é responsável por abrir e fechar a conexão corretamente.

---

## 🎮 Comandos

Os comandos trafegam como um único byte pela Serial e são definidos como `Enum` no Python e como `#define` no firmware:

| Comando      | Byte | Descrição                                      |
|--------------|------|------------------------------------------------|
| `SUBIR`      | `0`  | Liga o motor no sentido de subida              |
| `DESCER`     | `1`  | Liga o motor no sentido de descida             |
| `PARAR`      | `2`  | Para o motor imediatamente                     |
| `RESET`      | `3`  | Para o motor e reseta o estado                 |
| `ENSAIO`     | `4`  | Inicia o ensaio (motor + leitura da célula)    |

---

## ⚙️ Firmware (Arduino)

O firmware roda um loop não bloqueante baseado em estados:

| Estado      | Comportamento                                              |
|-------------|------------------------------------------------------------|
| `E_IDLE`    | Motor parado, aguardando comandos                          |
| `E_SUBINDO` | Pulsos contínuos no motor, sentido horário                 |
| `E_DESCENDO`| Pulsos contínuos no motor, sentido anti-horário            |
| `E_ENSAIO`  | Motor subindo + leitura da célula de carga a cada 50 ms    |

Durante o ensaio, o Arduino envia os valores de força lidos pela célula de carga de volta ao computador via `Serial.println()`, onde são capturados pelo `SerialBridge` e plotados no `GraphWidget`.

### Botão de Emergência (Hardware)

O pino 2 do Arduino é reservado para o botão de emergência físico. Ele é tratado via **interrupção de hardware** (`attachInterrupt`), garantindo parada imediata do motor independentemente do estado do loop principal.

---
