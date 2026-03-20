#define C_SUBIR 0
#define C_DESCER 1
#define C_RESET 2
#define C_ENSAIO 3
#define C_R_ENSAIO 4

void setup() 
{
  Serial.begin(9600);
  pinMode(2,OUTPUT);
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
      blink(2, 1);
      break;

    case C_DESCER:
      blink(2, 2);
      break;
    
    case C_RESET:
      blink(2, 3);
      break;

    case C_ENSAIO:
      blink(2, 4);
      break;

    case C_R_ENSAIO:
      blink(2, 5);
      break;
  }
}

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