#include "HX711.h"

// ── Pinos - Botão de emergência ────────────────────────
// ── NÃO ALTERAR, Pino 2 reservado para interrupções ────
#define EMERG_PIN 2

// ── Pinos - Motor de passo ─────────────────────────────
#define DIR_PIN   3
#define STEP_PIN  4

// ── Pinos - Célula de carga ────────────────────────────
#define DOUT_PIN  5
#define CLK_PIN   6

// ── Configs ────────────────────────────────────────────
#define STEP_INTERVAL_US  1000UL
#define ENSAIO_INTERVAL   50
#define TIMEOUT_SENSOR    5000
const float fator_calibracao = 420.0;

// ── Comandos ───────────────────────────────────────────
#define C_SUBIR    0
#define C_DESCER   1
#define C_PARAR    2
#define C_RESET    3
#define C_ENSAIO   4
#define C_R_ENSAIO 5

// ── Estados ────────────────────────────────────────────
#define E_IDLE     0
#define E_SUBINDO  1
#define E_DESCENDO 2
#define E_ENSAIO   3

// ── Globais ────────────────────────────────────────────
HX711 scale;
volatile unsigned short int state = E_IDLE;

// Timer da leitura do ensaio
unsigned long timeBuffer = 0;

// Motor não bloqueante
bool          stepState   = false;
unsigned long lastStepUs  = 0;
bool          motorDir    = true;


// ── INTERRUPÇÃO ────────────────────────────────────────
void emergencyISR()
{
  state = E_IDLE;
  halt();
}

// ── SETUP ──────────────────────────────────────────────
void setup()
{
  // Inicializar Serial
  Serial.begin(9600);

  // Inicializando pinos
  pinMode(DIR_PIN,  OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(EMERG_PIN, INPUT);

  // Inicializar hx711
  scale.begin(DOUT_PIN, CLK_PIN);
  unsigned long t = millis();
  while (!scale.is_ready())
  {
    if (millis() - t > TIMEOUT_SENSOR) return;
    delay(10);
  }
  for (int i = 0; i < 5; i++) { scale.read(); delay(50); }
  scale.set_scale(fator_calibracao);
  scale.tare(10);

  // atribuir interrupção
  attachInterrupt(digitalPinToInterrupt(EMERG_PIN), emergencyISR, FALLING);
}

// ── LOOP PRINCIPAL ─────────────────────────────────────
void loop()
{
  if (Serial.available())
  {
    byte cmd = Serial.read();
    runCommand(cmd);
  }
  runState();
}

// ── PROCESSAMENTO DE COMANDOS ──────────────────────────
void runCommand(byte commando)
{
  switch (commando)
  {
    case C_SUBIR:
      motorDir = true;
      state = E_SUBINDO;
      break;
    case C_DESCER:
      motorDir = false;
      state = E_DESCENDO;
      break;
    case C_PARAR:
    case C_RESET:
      state = E_IDLE;
      halt();
      break;
    case C_ENSAIO:
      motorDir = true;
      state = E_ENSAIO;
      timeBuffer = millis();
      break;
    case C_R_ENSAIO:
      state = E_IDLE;
      halt();
      break;
  }
}

// ── PROCESSAMENTO DE ESTADOS ───────────────────────────
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

// ── FUNÇÕES ────────────────────────────────────────────

void runEnsaio()
{
  spin();   // pulsos contínuos, não bloqueante

  unsigned long now = millis();
  if (now - timeBuffer >= ENSAIO_INTERVAL)
  {
    timeBuffer = now;
    readLoad(); // get_units(1) para não bloquear o loop por muito tempo
  }
}

void spin()
{
  digitalWrite(DIR_PIN, motorDir ? HIGH : LOW);

  unsigned long now = micros();
  if (now - lastStepUs < STEP_INTERVAL_US) return;

  lastStepUs = now;
  stepState  = !stepState;
  digitalWrite(STEP_PIN, stepState ? HIGH : LOW);
}

void halt()
{
  stepState = false;
  digitalWrite(STEP_PIN, LOW);
}

void readLoad()
{
  if (!scale.is_ready()) return;
  float peso = scale.get_units(1);
  Serial.println(peso);
}
