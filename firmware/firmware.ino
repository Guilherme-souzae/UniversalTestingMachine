#include "HX711.h"

// Pinos
#define DOUT_PIN 2 // pino de dados
#define CLK_PIN 3 // pino de clock
#define DIR_PIN 4 // pino direcional do motor
#define STEP_PIN 5 // pino de passo do motor 

// Configs
#define DELAY_SENSOR 50 // ms entre leituras
#define DURACAO_ENSAIO 10000 // ms
#define TIMEOUT_SENSOR 5000 // ms aguardando o sensor antes de desistir
#define STEPS_PER_REV 200 // passos para uma volta completa
const float fator_calibracao = 420.0; // fato de calibração do modulo

// Comandos
#define C_SUBIR 0
#define C_DESCER 1
#define C_RESET 2
#define C_ENSAIO 3
#define C_R_ENSAIO 4

// Estados
#define E_IDLE 0
#define E_MOVENDO 1
#define E_ENSAIO 2

// Globals
HX711 scale;
unsigned short int STATE;

void setup()
{
  // inicialização
  STATE = E_IDLE;
  Serial.begin(9600);
  scale.begin(DOUT_PIN, CLK_PIN);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);

  // Aguarda o sensor ficar pronto antes de tarar
  unsigned long t = millis();
  while (!scale.is_ready())
  {
    if (millis() - t > TIMEOUT_SENSOR) return; // failsafe
    delay(10);
  }

  scale.set_scale(fator_calibracao); // aplica fator de calibracao
  scale.tare(); // zera o modulo
}

void loop()
{
  lerComando();
  executarEstado();
}

void lerComando()
{
  if (!Serial.available()) return;
  
  byte cmd = Serial.read();

  switch(cmd)
  {
    case C_SUBIR:
      STATE = E_IDLE;
      break;

    case C_DESCER:
      STATE = E_IDLE;
      break;
      
    case C_ENSAIO:
      STATE = E_ENSAIO;
      break;
   }
}

void executarEstado()
{
  switch(STATE)
  {
    case E_ENSAIO:
      runEnsaio();
      break;
  }
}

void rotacionar(bool horario)
{
  
}
}

void runEnsaio() { }
