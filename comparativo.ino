// Anexo de medicao nativa. A pratica principal permanece em main.py.
#include <Arduino.h>
#if defined(ARDUINO_ARCH_AVR)
#include <avr/interrupt.h>
const uint8_t PINOS[] = {8, 10, 9}; // vermelho, verde, amarelo
const uint8_t BOTAO = 2;
#else
#include <hardware/sync.h>
const uint8_t PINOS[] = {13, 15, 14};
const uint8_t BOTAO = 16;
#endif

enum Estado : uint8_t { VERMELHO, VERDE, AMARELO };
const uint32_t TEMPOS[] = {5000, 5000, 2000};
volatile bool evento = false;
Estado estado = VERMELHO;
uint32_t inicio, duracao = 5000, liberadoDesde;
bool armado = true, contandoLiberacao = false;
void pedestreISR() { evento = true; }

void exibir() {
#if defined(ARDUINO_ARCH_AVR)
  for (uint8_t i = 0; i < 3; ++i) digitalWrite(PINOS[i], LOW);
  digitalWrite(PINOS[estado], HIGH);
#else
  // SIO do RP2040, escritas CLR e SET sem leitura anterior.
  *reinterpret_cast<volatile uint32_t*>(0xD0000018) = (1u<<13)|(1u<<14)|(1u<<15);
  *reinterpret_cast<volatile uint32_t*>(0xD0000014) = 1u << PINOS[estado];
#endif
}

void entrar(Estado proximo, uint32_t agora, uint32_t tempo) {
  estado = proximo;
  inicio = agora;
  duracao = tempo;
}

void setup() {
  for (uint8_t i = 0; i < 3; ++i) pinMode(PINOS[i], OUTPUT);
  pinMode(BOTAO, INPUT_PULLUP);
  inicio = millis();
  exibir();
  attachInterrupt(digitalPinToInterrupt(BOTAO), pedestreISR, FALLING);
}

void loop() {
#if defined(ARDUINO_ARCH_AVR)
  uint8_t chave = SREG;
  cli();
#else
  uint32_t chave = save_and_disable_interrupts();
#endif
  bool recebido = evento;
  evento = false;
#if defined(ARDUINO_ARCH_AVR)
  SREG = chave;
#else
  restore_interrupts(chave);
#endif
  uint32_t agora = millis();
  bool pedido = recebido && armado;
  if (pedido) { armado = false; contandoLiberacao = false; }
  if (!armado) {
    if (digitalRead(BOTAO) == LOW) contandoLiberacao = false;
    else if (!contandoLiberacao) { liberadoDesde = agora; contandoLiberacao = true; }
    else if ((uint32_t)(agora - liberadoDesde) >= 50) armado = true;
  }
  Estado anterior = estado;
  if (pedido) {
    if (estado == VERDE) entrar(AMARELO, agora, 2000);
    else if (estado == VERMELHO) entrar(VERMELHO, agora, 5000);
    else {
      uint32_t decorrido = agora - inicio;
      uint32_t restante = decorrido >= duracao ? 0 : duracao - decorrido;
      entrar(AMARELO, agora, restante < 2000 ? restante : 2000);
    }
  }
  if ((uint32_t)(agora - inicio) >= duracao) {
    Estado proximo = estado == VERMELHO ? VERDE : estado == VERDE ? AMARELO : VERMELHO;
    entrar(proximo, agora, TEMPOS[proximo]);
  }
  if (estado != anterior) exibir();
}
