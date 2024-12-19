
#include <Arduino.h>

#define BUTTON_PIN D1  // O pino D1 conectado ao botão
#define LED_PIN    D7  // O pino D7 conectado ao LED

bool ledState = false;         // Estado atual do LED
bool lastButtonState = HIGH;   // Último estado do botão
bool currentButtonState;       // Estado atual do botão

void setup() {
  pinMode(LED_PIN, OUTPUT);     // Configura o pino do LED como saída
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // Configura o pino do botão como entrada com pull-up
  digitalWrite(LED_PIN, ledState);  // Inicializa o LED desligado
}

void loop() {
  // Lê o estado atual do botão
  currentButtonState = digitalRead(BUTTON_PIN);

  // Verifica se o botão foi pressionado (mudança de HIGH para LOW)
  if (lastButtonState == HIGH && currentButtonState == LOW) {
    // Alterna o estado do LED
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
    
    // Pequeno delay para evitar múltiplos acionamentos
    delay(50);
  }

  // Atualiza o último estado do botão
  lastButtonState = currentButtonState;
}