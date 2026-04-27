#include <HX711.h>

// Pinos
#define DOUT_PIN 2 // pino de dados
#define CLK_PIN 3 // pino de clock

// Configs
#define DELAY_SENSOR 50 // ms entre leituras
#define DURACAO_ENSAIO 10000 // ms
#define TIMEOUT_SENSOR 5000 // ms aguardando o sensor antes de desistir

// Comandos
#define C_SUBIR 0
#define C_DESCER 1
#define C_RESET 2
#define C_ENSAIO 3
#define C_R_ENSAIO 4

HX711 scale;
const float fator_calibracao = 420.0;

void setup()
{
  Serial.begin(9600);
  scale.begin(DOUT_PIN, CLK_PIN);

  // Aguarda o sensor ficar pronto antes de tarar
  unsigned long t = millis();
  while (!scale.is_ready())
  {
    if (millis() - t > TIMEOUT_SENSOR)
    {
      return;
    }
    delay(10);
  }

  scale.set_scale(fator_calibracao); // aplica fator de calibracao
  scale.tare();

  runEnsaio();
}

void loop()
{
  if (Serial.available()) {
    byte cmd = Serial.read();
    runCommand(cmd);
  }
}

void runCommand(byte commando)
{
  switch (commando) {
    case C_ENSAIO:
      runEnsaio();
      break;
  }
}

void runEnsaio()
{
  unsigned long inicio = millis();

  while (millis() - inicio < DURACAO_ENSAIO)
  {
    // Aguarda o sensor ficar pronto (com timeout)
    unsigned long t = millis();
    while (!scale.is_ready())
    {
      if (millis() - t > TIMEOUT_SENSOR)
      {
        return;
      }
      delay(5);
    }

    float peso = scale.get_units(10);
    peso = map(peso,-1023,1023,-100,100);
    Serial.println(peso);
    delay(DELAY_SENSOR);
  }
}
