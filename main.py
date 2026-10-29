"""Semaforo inteligente - Raspberry Pi Pico RP2040 - MicroPython.
Vermelho GP13, amarelo GP14, verde GP15, botao GP16 para GND.
Sem delay/sleep: a maquina de estados consulta o contador de tempo.
"""
from time import ticks_ms, ticks_diff

# Altere os tempos aqui. X=2 dobra as duracoes; X deve ser inteiro >= 1.
X = 1
T_VERMELHO_MS = 5000 * X
T_AMARELO_MS = 2000 * X
T_VERDE_MS = 5000 * X
# O atendimento do pedestre usa no maximo 2 s de amarelo, mesmo com X>1.
T_ALERTA_PEDESTRE_MS = 2000
T_LIBERACAO_MS = 50

VERMELHO, VERDE, AMARELO = 0, 1, 2
NOMES = ("VERMELHO", "VERDE", "AMARELO")
PINOS = (13, 15, 14)  # na mesma ordem dos estados


class Semaforo:
    """Logica independente dos GPIOs, para permitir testes com tempo virtual."""

    def __init__(self, agora):
        self.estado = VERMELHO
        self.inicio = agora
        self.duracao = T_VERMELHO_MS

    def entrar(self, estado, agora, duracao):
        self.estado = estado
        self.inicio = agora
        self.duracao = duracao

    def atualizar(self, agora, pedido=False):
        anterior = self.estado
        if pedido:
            if self.estado == VERDE:
                self.entrar(AMARELO, agora, T_ALERTA_PEDESTRE_MS)
            elif self.estado == AMARELO:
                # Nunca alongar um amarelo em andamento.
                decorrido = ticks_diff(agora, self.inicio)
                restante = max(0, self.duracao - decorrido)
                self.inicio = agora
                self.duracao = min(restante, T_ALERTA_PEDESTRE_MS)
            else:
                # Garante uma janela completa de travessia a partir do pedido.
                self.entrar(VERMELHO, agora, T_VERMELHO_MS)

        if ticks_diff(agora, self.inicio) >= self.duracao:
            if self.estado == VERMELHO:
                self.entrar(VERDE, agora, T_VERDE_MS)
            elif self.estado == VERDE:
                self.entrar(AMARELO, agora, T_AMARELO_MS)
            else:
                self.entrar(VERMELHO, agora, T_VERMELHO_MS)
        return self.estado != anterior


_evento_irq = 0


def interrupcao_pedestre(pino):
    # ISR curta: sem print, espera, listas ou alteracoes dos LEDs.
    global _evento_irq
    _evento_irq = 1


def executar():
    global _evento_irq
    import machine
    import micropython
    from machine import Pin, mem32

    micropython.alloc_emergency_exception_buf(100)
    leds = tuple(Pin(pino, Pin.OUT, value=0) for pino in PINOS)
    botao = Pin(16, Pin.IN, Pin.PULL_UP)

    # RP2040 datasheet, SIO: GPIO_OUT_SET e GPIO_OUT_CLR.
    # Estes enderecos pertencem ao RP2040, nao ao STM32 nem ao Pico 2.
    GPIO_OUT_SET = 0xD0000014
    GPIO_OUT_CLR = 0xD0000018
    MASCARA_LEDS = (1 << 13) | (1 << 14) | (1 << 15)

    def exibir(estado):
        # Apaga os tres antes de acender um: nunca ha duas cores ligadas.
        mem32[GPIO_OUT_CLR] = MASCARA_LEDS
        mem32[GPIO_OUT_SET] = 1 << PINOS[estado]

    controle = Semaforo(ticks_ms())
    exibir(controle.estado)
    armado = True
    liberado_desde = None
    botao.irq(trigger=Pin.IRQ_FALLING, handler=interrupcao_pedestre, hard=True)

    while True:
        # Consome o sinal sem corrida entre leitura e limpeza da flag.
        chave = machine.disable_irq()
        evento = _evento_irq
        _evento_irq = 0
        machine.enable_irq(chave)
        agora = ticks_ms()
        pedido = bool(evento and armado)

        if pedido:
            armado = False
            liberado_desde = None

        # Debounce sem espera: rearma so apos 50 ms de nivel alto estavel.
        if not armado:
            if botao.value() == 0:
                liberado_desde = None
            elif liberado_desde is None:
                liberado_desde = agora
            elif ticks_diff(agora, liberado_desde) >= T_LIBERACAO_MS:
                armado = True

        if controle.atualizar(agora, pedido):
            exibir(controle.estado)


if __name__ == "__main__":
    executar()
