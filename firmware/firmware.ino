#include "HX711.h"
#include <ArduinoJson.h>

// ── Pinos - Botão de emergência ────────────────────────
// ── NÃO ALTERAR, Pino 2 reservado para interrupções ────
#define EMERGENCIA_BTN 2

// ── Pinos - Motor de passo ─────────────────────────────
#define DIR_PIN   3
#define STEP_PIN  4

// ── Pinos - Célula de carga ────────────────────────────
#define CLK_PIN  5
#define DOUT_PIN 6

// ── Configs ────────────────────────────────────────────
#define STEP_INTERVAL_US  200UL
#define ENSAIO_INTERVAL   20
#define TIMEOUT_SENSOR    5000
#define TEMPO_ESTABILIZACAO 300
const float fator_calibracao = 23.0;

// ── Estados ────────────────────────────────────────────
#define E_IDLE     0
#define E_SUBINDO  1
#define E_DESCENDO 2
#define E_ENSAIO   3

// ── Globais ────────────────────────────────────────────
HX711 scale;
volatile unsigned short int state = E_IDLE;

unsigned long timeBuffer = 0;

bool stepState = false;
unsigned long lastStepUs = 0;
bool motorDir = true;

bool estabilizado = true;
unsigned long inicioEstabilizacao = 0;

// -------------------------------------------------------

void setup()
{
  Serial.begin(9600);

  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(EMERGENCIA_BTN, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(EMERGENCIA_BTN),[]() {state = E_IDLE; runState();},FALLING);

  scale.begin(DOUT_PIN, CLK_PIN);

  unsigned long t = millis();

  while (!scale.is_ready())
  {
    if (millis() - t > TIMEOUT_SENSOR) return;
    delay(10);
  }

  for (int i = 0; i < 5; i++)
  {
    scale.read();
    delay(50);
  }

  scale.set_scale(fator_calibracao);
  scale.tare(10);
}

void loop()
{
  if (Serial.available())
  {
    String linha = Serial.readStringUntil('\n');

    JsonDocument doc;

    DeserializationError erro =
        deserializeJson(doc, linha);

    if (!erro)
    {
      runCommand(doc);
    }
  }

  runState();
}

// -------------------------------------------------------
// COMANDOS
// -------------------------------------------------------

void runCommand(JsonDocument &doc)
{
  const char *comando = doc["comando"];

  if (comando == nullptr)
    return;

  if (strcmp(comando, "SUBIR") == 0)
  {
    motorDir = true;
    state = E_SUBINDO;
  }

  else if (strcmp(comando, "DESCER") == 0)
  {
    motorDir = false;
    state = E_DESCENDO;
  }

  else if (strcmp(comando, "PARAR") == 0)
  {
    state = E_IDLE;
    halt();
  }

  else if (strcmp(comando, "RESET") == 0)
  {
    state = E_IDLE;
    scale.tare(10);
    halt();
  }

  else if (strcmp(comando, "ENSAIO") == 0)
  {
    motorDir = false;
    state = E_ENSAIO;

    estabilizado = false;
    inicioEstabilizacao = millis();

    timeBuffer = millis();
  }

  else if (strcmp(comando, "CONFIGURAR") == 0)
  {
    if (doc["payload"].is<JsonObject>())
    {
      readPayload(doc["payload"]);
    }
  }
}

void readPayload(JsonObject payload)
{
  // Implementar posteriormente
}

// -------------------------------------------------------
// ESTADOS
// -------------------------------------------------------

void runState()
{
  switch (state)
  {
  case E_SUBINDO:
    spin();
    break;

  case E_DESCENDO:
    spin();
    break;

  case E_ENSAIO:
    runEnsaio();
    break;
  }
}

// -------------------------------------------------------
// MOTOR
// -------------------------------------------------------

void runEnsaio()
{
  spin();

  unsigned long now = millis();

  if (estabilizado == false)
  {
    if (now - inicioEstabilizacao >= TEMPO_ESTABILIZACAO)
    {
      estabilizado = true;
      timeBuffer = now;
    }

    return;
  }

  if (now - timeBuffer >= ENSAIO_INTERVAL)
  {
    timeBuffer = now;
    readLoad();
  }
}

void spin()
{
  digitalWrite(DIR_PIN, motorDir ? HIGH : LOW);

  unsigned long now = micros();

  if (now - lastStepUs < STEP_INTERVAL_US)
    return;

  lastStepUs = now;

  stepState = !stepState;

  digitalWrite(STEP_PIN, stepState);
}

void halt()
{
  stepState = false;
  digitalWrite(STEP_PIN, LOW);
}

// -------------------------------------------------------
// HX711
// -------------------------------------------------------

void readLoad()
{
  if (scale.is_ready()) Serial.println(scale.get_units(1));
}