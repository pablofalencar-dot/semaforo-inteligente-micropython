# Semáforo em Python no Wokwi

Projeto para **Raspberry Pi Pico RP2040 com MicroPython**.

**[Executar a simulação pronta no Wokwi](https://wokwi.com/projects/479241493679592449)**

## Copiar do GitHub e testar

1. Abra um [novo projeto MicroPython para Raspberry Pi Pico no Wokwi](https://wokwi.com/projects/new/micropython-pi-pico).
2. Abra [main.py](main.py) neste GitHub, copie o arquivo inteiro e substitua todo o conteúdo da aba `main.py` no Wokwi.
3. Abra [diagram.json](diagram.json), copie o arquivo inteiro e substitua todo o conteúdo da aba `diagram.json` no Wokwi. Isso monta a placa, três LEDs, resistores e botão.
4. Clique no botão verde **Play**. Não é necessário instalar bibliotecas.

Use o **Pico RP2040**, pois os endereços de registradores deste código são específicos dessa placa. O programa não é para ESP32, Uno ou Pico 2.

## Funcionamento

- Vermelho por **5 segundos**.
- Verde por **5 segundos**.
- Amarelo por **2 segundos**, voltando ao vermelho.
- Durante o verde, o botão azul **PEDESTRE** antecipa o amarelo. Depois do alerta vem o vermelho.
- No amarelo, um pedido não prolonga a espera. No vermelho, renova a janela de parada.
- Manter o botão pressionado gera um atendimento; para rearmar, solte por pelo menos 50 ms.

Os tempos são os do simulador. Para alterar os tempos normais, edite `X` no começo de `main.py`; mantenha `X = 1` para 5 s, 5 s e 2 s.

| Componente | GPIO |
| --- | --- |
| Vermelho com resistor de 330 Ω | GP13 |
| Amarelo com resistor de 330 Ω | GP14 |
| Verde com resistor de 330 Ω | GP15 |
| Botão ligado ao GND com pull-up interno | GP16 |

## Implementação e verificação

Máquina de estados com `ticks_ms()` e `ticks_diff()`, sem `delay()` ou `sleep()`. O botão usa interrupção de hardware e as saídas usam `machine.mem32` nos registradores SIO do RP2040. O amarelo é a resposta imediata ao pedido; o vermelho vem após o intervalo de alerta mais a latência do programa.

O circuito e o botão foram testados no Wokwi. Oito testes locais da lógica passaram; para repeti-los no computador, execute `python testar_logica.py`.

## Anexo de comparação AVR e ARM

[comparativo.ino](comparativo.ino) é um anexo nativo de medição; **o código Python a copiar para a prática é main.py**. O anexo foi compilado para Uno AVR e Pico ARM. A [execução no GitHub Actions passou](https://github.com/pablofalencar-dot/semaforo-inteligente-micropython/actions/runs/40933590494) e os valores estão em [medicoes_nativas.json](medicoes_nativas.json).

O repositório reúne os arquivos de código e as instruções de execução. O relatório será entregue impresso, separadamente.
