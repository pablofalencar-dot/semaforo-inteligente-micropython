# Semáforo inteligente em MicroPython

Projeto de Sistemas Digitais e Microprocessadores, com Raspberry Pi Pico RP2040 e Wokwi.

**[Abrir e executar no Wokwi](https://wokwi.com/projects/479241493679592449)**

**[Ler o relatório](relatorio.pdf)** · [Diagrama de estados](diagrama_estados.svg) · [Roteiro da apresentação](roteiro_apresentacao.md)

## Como executar

1. Abra o link do Wokwi e clique no botão verde **Play**.
2. Observe o ciclo: vermelho por 5 segundos, verde por 5 segundos e amarelo por 2 segundos.
3. Durante o verde, aperte o botão azul **PEDESTRE**. O amarelo inicia antecipadamente e depois vem o vermelho.
4. Para editar uma cópia própria, use **Save a copy** no Wokwi e salve na sua conta.

Os segundos são os do simulador. Em computadores lentos, a simulação pode avançar mais devagar que o relógio real.

## Código principal

### Para o professor copiar e testar

1. Abra um [novo projeto MicroPython para Pico no Wokwi](https://wokwi.com/projects/new/micropython-pi-pico).
2. Abra [main.py neste GitHub](main.py), use o botão de copiar o arquivo e substitua todo o conteúdo de `main.py` no Wokwi.
3. Faça o mesmo com [diagram.json](diagram.json), na aba `diagram.json` do Wokwi. Esse arquivo monta os LEDs, resistores e botão.
4. Clique em Play. Não é necessário instalar bibliotecas. Se preferir, use a simulação pronta no topo desta página.

O projeto prático está em **Python com MicroPython**, em [main.py](main.py). [diagram.json](diagram.json) contém o circuito completo. Use Pico RP2040, não Pico 2 nem Uno, para esse código Python.

| Componente | Pino |
| --- | --- |
| LED vermelho com resistor de 330 Ω | GP13 |
| LED amarelo com resistor de 330 Ω | GP14 |
| LED verde com resistor de 330 Ω | GP15 |
| Botão ao GND, com pull-up interno | GP16 |

O programa usa máquina de estados, `ticks_ms()` e `ticks_diff()`, sem `delay()` ou `sleep()`. O botão gera interrupção por borda de descida, e o rearme exige 50 ms de soltura estável. As saídas são alteradas pelos registradores SIO do RP2040 por `machine.mem32`.

O botão no vermelho renova a janela de parada. No amarelo, não prolonga a espera. O amarelo é a resposta imediata ao pedido; a transição ao vermelho ocorre após o intervalo de alerta e a latência do programa.

## Verificação

Execute `python testar_logica.py` no computador para verificar estados, limites, retorno do contador, interrupção simulada, debounce e exclusividade das cores. Os testes usam hardware simulado e não substituem a execução do projeto Wokwi.

O circuito foi aberto e executado no Wokwi. Foram observados o vermelho, o verde, o amarelo normal e a antecipação do amarelo por botão durante o verde, seguida de vermelho. O ambiente escolhido no diagrama é `micropython-20260406-v1.28.0`.

## Anexo exigido de comparação AVR e ARM

O professor também pede comparar dois firmwares compilados. [comparativo.ino](comparativo.ino) é um **anexo de medição em C++**, não substitui a prática Python. Ele implementa o mesmo comportamento para Uno AVR e Pico ARM: no AVR usa a abstração Arduino; no ARM usa registradores SIO para as saídas.

[GitHub Actions](https://github.com/pablofalencar-dot/semaforo-inteligente-micropython/actions/workflows/comparar-binarios.yml) compila as duas versões e publica os binários, tamanhos e relatório de medição. A compilação usa Arduino CLI 1.3.1, Arduino AVR Boards 1.8.6 e Arduino-Pico 6.1.0, com opções padrão. Os resultados incluem as bibliotecas de cada plataforma e não isolam apenas a arquitetura da CPU.

A [primeira execução passou](https://github.com/pablofalencar-dot/semaforo-inteligente-micropython/actions/runs/40933590494). Flash estimada pelo GNU size: **1764 bytes no AVR** e **327276 bytes no ARM**. RAM estática: **44 bytes** e **18684 bytes**, respectivamente. O firmware completo inclui os cores e bibliotecas; esses números não são o tamanho do programa Python e não permitem concluir que ARM é inerentemente menos eficiente.

No anexo AVR, os LEDs vermelho, amarelo e verde usam D8, D9 e D10; o botão usa D2. Copie o anexo para um projeto Arduino Uno separado para demonstrá-lo. Não substitua o `main.py` do projeto Python por esse anexo.

## Entrega

- Código e relatório: https://github.com/pablofalencar-dot/semaforo-inteligente-micropython
- Simulação executável: https://wokwi.com/projects/479241493679592449
- Preencha nomes, RAs, curso e turma na versão editável do relatório antes da entrega.
- As fotos informam entrega em 09/11 e postagem na pasta da disciplina; o ano deve ser confirmado com o professor.

O GitHub contém os arquivos e o histórico; a execução interativa acontece no Wokwi. Os dois links estão no relatório.
