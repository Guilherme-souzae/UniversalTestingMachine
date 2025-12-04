#include "HX711.h"

// Motor
#define IN1 7
#define IN2 8

// Célula de carga HX711
#define DOUT  13
#define CLK   12

HX711 scale;
float calibration_factor = 21.5;

// Controle
char comando;
float peso;
bool medindo = false;
unsigned long startTime = 0;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  Serial.begin(9600);

  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor);

  Serial.println("\n--- Sistema Motor + Célula de Carga ---");
  Serial.println("Zerando balança (tare)...");
  delay(2000);
  scale.tare(); // zera balança

  // Faz média inicial para estabilizar
  float peso_inicial = scale.get_units(10);
  Serial.print("Offset inicial (g): ");
  Serial.println(peso_inicial, 2);

  Serial.println("Pronto!");
  Serial.println("Comandos: f=frente, b=tras, s=stop");
}

void loop() {
  // Se estiver no modo medindo, envia tempo e peso
  if (medindo) {
    peso = scale.get_units(); // leitura direta
    unsigned long tempoAtual = millis() - startTime;
    Serial.print(tempoAtual);   // tempo em ms
    Serial.print(",");
    Serial.println(peso, 2);    // peso em g
  }

  // Recebe comandos do Python
  if (Serial.available() > 0) {
    comando = Serial.read();

    if (comando == 'f') {        // Frente
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      Serial.println("START");   // marcador de início
      medindo = true;
      startTime = millis();      // reseta contador de tempo
    }
    else if (comando == 'b') {   // Trás
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      Serial.println("BACK");
      medindo = false;           // não mede no modo "b"
    }
    else if (comando == 's') {   // Stop
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      Serial.println("STOP");    // marcador de fim
      medindo = false;
    }
  }

  delay(200);
}
