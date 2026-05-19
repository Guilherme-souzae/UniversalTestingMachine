// Leds de teste
#define C_RED 2
#define C_GREEN 3
#define C_BLUE 4
#define E_RED 5
#define E_GREEN 6
#define E_BLUE 7
#define M_CCLOCKWISE 8
#define M_CLOCKWISE 9
#define B_INTERRUPT 10

// Comandos
#define C_SUBIR 0
#define C_DESCER 1
#define C_PARAR 2
#define C_RESET 3
#define C_ENSAIO 4
#define C_R_ENSAIO 5

// Estados
#define E_IDLE 0
#define E_SUBINDO 1
#define E_DESCENDO 2
#define E_ENSAIO 3


// Globais
unsigned long ensaioInterval = 50;
unsigned long ledSpinInterval = 50;
unsigned long ledSpinBuffer = 0;
bool ledSpinState = false;
unsigned long timeBuffer = 0;
unsigned int short state = 0;

// --- SETUP
void setup()
{
  // Iniciação
  Serial.begin(9600);

  // Pinagem
  pinMode(C_RED, OUTPUT);
  pinMode(C_GREEN, OUTPUT);
  pinMode(C_BLUE, OUTPUT);
  pinMode(E_RED, OUTPUT);
  pinMode(E_GREEN, OUTPUT);
  pinMode(E_BLUE, OUTPUT);
  pinMode(M_CCLOCKWISE, OUTPUT);
  pinMode(M_CLOCKWISE, OUTPUT);
  pinMode(B_INTERRUPT, OUTPUT);
}

// --- LOOP PRINCIPAL
void loop()
{
  if (Serial.available())
  {
    byte cmd = Serial.read();
    runCommand(cmd);
    ledComands(cmd);
  }

  runState();
  ledStates();
}

// --- PROCESSAMENTO DE COMANDOS
void runCommand(byte commando)
{
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
      digitalWrite(M_CLOCKWISE, ledSpinState);
      digitalWrite(M_CCLOCKWISE, LOW);
    }
    else
    {
      digitalWrite(M_CLOCKWISE, LOW);
      digitalWrite(M_CCLOCKWISE, ledSpinState);
    }
  }
}

void halt()
{
  digitalWrite(M_CLOCKWISE, LOW);
  digitalWrite(M_CCLOCKWISE, LOW);
}

void readLoad()
{
  Serial.print(100);
}

// --- LEDS DE TESTE
void ledComands(byte commando)
{
  switch (commando) 
  {
    case C_PARAR:
      digitalWrite(C_RED, LOW);
      digitalWrite(C_GREEN, LOW);
      digitalWrite(C_BLUE, LOW);
      break;

    case C_SUBIR:
      digitalWrite(C_RED, HIGH);
      digitalWrite(C_GREEN, LOW);
      digitalWrite(C_BLUE, LOW);
      break;

    case C_DESCER:
      digitalWrite(C_RED, LOW);
      digitalWrite(C_GREEN, HIGH);
      digitalWrite(C_BLUE, LOW);
      break;

    case C_ENSAIO:
      digitalWrite(C_RED, HIGH);
      digitalWrite(C_GREEN, HIGH);
      digitalWrite(C_BLUE, LOW);
      break;

    case C_R_ENSAIO:
      digitalWrite(C_RED, LOW);
      digitalWrite(C_GREEN, LOW);
      digitalWrite(C_BLUE, HIGH);
      break; 
  }
}

void ledStates()
{
  switch (state) 
  {
    case E_IDLE:
      digitalWrite(E_RED, LOW);
      digitalWrite(E_GREEN, LOW);
      digitalWrite(E_BLUE, LOW);
      break;

    case E_SUBINDO:
      digitalWrite(E_RED, HIGH);
      digitalWrite(E_GREEN, LOW);
      digitalWrite(E_BLUE, LOW);
      break;

    case E_DESCENDO:
      digitalWrite(E_RED, LOW);
      digitalWrite(E_GREEN, HIGH);
      digitalWrite(E_BLUE, LOW);
      break;
    
    case E_ENSAIO:
      digitalWrite(E_RED, HIGH);
      digitalWrite(E_GREEN, HIGH);
      digitalWrite(E_BLUE, HIGH);
      break;
  }
}