#include <LiquidCrystal.h>

LiquidCrystal lcd(2, 4, 10, 11, 12, 13);

String ultimoComando = "";

void setup() 
{
  lcd.begin(16, 2);
  Serial.begin(115200);

  lcd.setCursor(0,0);
  lcd.print("Aguardando...");
}

void loop()
{
  if (Serial.available())
  {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    // Evita atualizar se for o mesmo comando
    if (comando != ultimoComando)
    {
      ultimoComando = comando;

      lcd.clear();
      
      lcd.setCursor(0,0);
      lcd.print("Comando:");

      lcd.setCursor(0,1);
      lcd.print(comando);

      Serial.print("Recebido: ");
      Serial.println(comando);
    }
  }
}