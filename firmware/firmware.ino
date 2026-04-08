// pinos
#define LED_TESTE 2
#define SENSOR_TESTE A0

// configs
#define DELAY_SENSOR 50 // ms
#define DURACAO_ENSAIO 10000 // ms

// comandos
#define C_SUBIR 0
#define C_DESCER 1
#define C_RESET 2
#define C_ENSAIO 3
#define C_R_ENSAIO 4

void setup() 
{
  Serial.begin(9600);
  pinMode(LED_TESTE,OUTPUT);
  pinMode(SENSOR_TESTE,INPUT);
}

void loop()
{
  if (Serial.available())
  {
    byte cmd = Serial.read();
    runCommand(cmd);
  }
}

void runCommand(byte commando)
{
  switch (commando)
  {
    case C_SUBIR:
      blink(LED_TESTE, 1);
      break;

    case C_DESCER:
      blink(LED_TESTE, 2);
      break;
    
    case C_RESET:
      blink(LED_TESTE, 3);
      break;

    case C_ENSAIO:
      runEnsaio();
      break;

    case C_R_ENSAIO:
      blink(LED_TESTE, 5);
      break;
  }
}

void runEnsaio()
{
  unsigned long timeBuffer = millis();

  while (true)
  {
    if (millis() - timeBuffer >= DURACAO_ENSAIO) break;

    int sensor = analogRead(SENSOR_TESTE);
    Serial.println(sensor);

    delay(DELAY_SENSOR);
  }
}

// teste 
void blink(int port, int times)
{
  for (int i = 0; i < times; i++)
  {
    digitalWrite(port, LOW);
    delay(100);
    digitalWrite(port,HIGH);
    delay(100);
  }
}