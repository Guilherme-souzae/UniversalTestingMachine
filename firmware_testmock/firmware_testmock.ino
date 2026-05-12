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

void setup()
{
  Serial.begin(9600);
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
    float peso = 50;
    Serial.println(peso);
    delay(DELAY_SENSOR);
  }
}