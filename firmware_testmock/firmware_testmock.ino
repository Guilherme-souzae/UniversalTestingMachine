#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <ArduinoJson.h>

// --- Display LCD (Adafruit ST7735)
#define TFT_CS   5
#define TFT_DC   2
#define TFT_RST  4
// SCK = GPIO18 e MOSI = GPIO23 são fixos (SPI de hardware do ESP32)

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

// --- Botão de emergência
#define B_INTERRUPT 33

// Comandos
#define C_SUBIR    "SUBIR"
#define C_DESCER   "DESCER"
#define C_PARAR    "PARAR"
#define C_RESET    "RESET"
#define C_ENSAIO   "ENSAIO"
#define C_CONFIG   "CONFIGURAR"

// Estados
#define E_IDLE     0
#define E_SUBINDO  1
#define E_DESCENDO 2
#define E_ENSAIO   3

// Globais
unsigned long ensaioInterval = 50;
unsigned long timeBuffer = 0;
volatile unsigned int short state = 0;
byte lastCommand = 255; // força a primeira atualização de tela

// --- Auxiliares de texto para o display
const char* nomeComando(byte cmd)
{
  switch (cmd)
  {
    case C_SUBIR:    return "SUBIR";
    case C_DESCER:   return "DESCER";
    case C_PARAR:    return "PARAR";
    case C_RESET:    return "RESET";
    case C_ENSAIO:   return "ENSAIO";
    case C_R_ENSAIO: return "R.ENSAIO";
    default:         return "-";
  }
}

const char* nomeEstado(unsigned int st)
{
  switch (st)
  {
    case E_IDLE:     return "PARADO";
    case E_SUBINDO:  return "SUBINDO";
    case E_DESCENDO: return "DESCENDO";
    case E_ENSAIO:   return "ENSAIO";
    default:         return "-";
  }
}

// Redesenha a tela inteira (usado ao trocar de comando/estado)
void desenhaTela(byte cmd, unsigned int st)
{
  tft.fillScreen(ST7735_BLACK);

  tft.setTextColor(ST7735_WHITE);
  tft.setTextSize(1);
  tft.setCursor(5, 5);
  tft.print("Comando:");

  tft.setTextColor(ST7735_YELLOW);
  tft.setTextSize(2);
  tft.setCursor(5, 15);
  tft.print(nomeComando(cmd));

  tft.setTextColor(ST7735_WHITE);
  tft.setTextSize(1);
  tft.setCursor(5, 45);
  tft.print("Estado:");

  tft.setTextColor(corDoEstado(st));
  tft.setTextSize(2);
  tft.setCursor(5, 55);
  tft.print(nomeEstado(st));
}

uint16_t corDoEstado(unsigned int st)
{
  switch (st)
  {
    case E_IDLE:     return ST7735_WHITE;
    case E_SUBINDO:  return ST7735_RED;
    case E_DESCENDO: return ST7735_GREEN;
    case E_ENSAIO:   return ST7735_CYAN;
    default:         return ST7735_WHITE;
  }
}

// Atualiza só a área do "Estado" (chamado a cada troca de estado, sem redesenhar tudo)
void atualizaEstadoNaTela(unsigned int st)
{
  tft.fillRect(5, 55, 150, 16, ST7735_BLACK);
  tft.setTextColor(corDoEstado(st));
  tft.setTextSize(2);
  tft.setCursor(5, 55);
  tft.print(nomeEstado(st));
}

// --- EMERGENCIA
void emergenciaISR()
{
  state = E_IDLE;
  halt();
}

// --- SETUP
void setup()
{
  Serial.begin(9600);

  // Display
  tft.initR(INITR_BLACKTAB); // troque para INITR_GREENTAB se as cores saírem deslocadas
  tft.setRotation(2);
  desenhaTela(255, state);

  delay(1000);
}

// --- LOOP PRINCIPAL
void loop()
{
  if (Serial.available())
  {
    // decodificar Json
    StaticJsonDocument<256> doc;
    DeserializationError ermac = deserializeJson(doc, Serial);

    if (ermac == false)
    {
      const char* cmd = doc["comando"]

      runCommand(cmd);

      if (cmd != lastCommand)
      {
        desenhaTela(cmd, state);
        lastCommand = cmd;
      } 
    }
  }

  runState();
}

// --- PROCESSAMENTO DE COMANDOS
void runCommand(byte commando)
{
  unsigned int estadoAnterior = state;

  switch (commando)
  {
    case C_SUBIR:
      state = E_SUBINDO;
      break;

    case C_DESCER:
      state = E_DESCENDO;
      break;

    case C_PARAR:
      state = E_IDLE;
      halt();
      break;

    case C_ENSAIO:
      state = E_ENSAIO;
      break;

    case C_R_ENSAIO:
      state = E_IDLE;
      halt();
      break;
  }

  if (state != estadoAnterior)
    atualizaEstadoNaTela(state);
}

// --- PROCESSAMENTO DE ESTADOS
void runState()
{
  switch (state)
  {
    case E_SUBINDO:
      spin(true);
      break;

    case E_DESCENDO:
      spin(false);
      break;

    case E_ENSAIO:
      runEnsaio();
      break;
  }
}

// --- FUNÇÕES
void runEnsaio()
{
  unsigned long now = millis();
  if (now - timeBuffer >= ensaioInterval)
  {
    timeBuffer = now;
    spin(true);
    readLoad();
  }
}

void spin(bool clockwise)
{
  unsigned long now = millis();

  if (now - ledSpinBuffer >= ledSpinInterval)
  {
    ledSpinBuffer = now;
    ledSpinState = !ledSpinState;

    if (clockwise)
    {
      srDigitalWrite(M_CLOCKWISE, ledSpinState);
      srDigitalWrite(M_CCLOCKWISE, LOW);
    }
    else
    {
      srDigitalWrite(M_CLOCKWISE, LOW);
      srDigitalWrite(M_CCLOCKWISE, ledSpinState);
    }
  }
}

void readLoad()
{
    static float t = 0.0f;

    float valor =
        100.0f +
        50.0f * sin(t) +
        10.0f * sin(5.0f * t);

    Serial.println(valor);

    t += 0.05f;
}
