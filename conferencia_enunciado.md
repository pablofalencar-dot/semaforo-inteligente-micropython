# Conferência das três fotos do enunciado

| Exigência | Onde foi atendida | Evidência ou limite |
| --- | --- | --- |
| Comparar AVR 8 bits e ARM Cortex-M 32 bits | Relatório seção 1 | ATmega328P, Cortex-M0+ RP2040 e Cortex-M3 STM32F103 |
| Inteiros de 32 bits e ponto flutuante | Relatório seção 1 | Operações multibyte e ausência de FPU nos dispositivos |
| Evolução ARM com características e aplicações | Relatório seção 1 | Tabela de arquiteturas e aplicações |
| RAM e Flash típicas | Relatório seção 2 | Tabela e distinção chip/placa |
| Execução e acesso à memória | Relatório seções 1 e 2 | Harvard, barramentos, SRAM e XIP |
| Clock, ADC, DMA, timers e CAN | Relatório seção 2 | Tabela e diferenças de recursos |
| Arduino IDE/C++ versus registradores, CMSIS e HAL | Relatório seção 3 | Níveis de abstração explicados |
| Simulador com três LEDs | main.py e diagram.json | Projeto salvo e executado no Wokwi |
| Vermelho 5 s, amarelo 2 s, verde 5 s | main.py | Tempos configuráveis por X |
| Não usar delay e consultar contador | main.py | ticks_ms e ticks_diff; nenhuma chamada delay/sleep |
| Comparar implementação AVR e ARM | comparativo.ino e relatório seção 6 | Anexo compilado para as duas CPUs; prática principal em Python |
| Diagrama FSM com transições temporais | Relatório seção 4 e diagrama_estados.svg | Tempos, início e efeito do botão |
| Tamanho do código compilado | Relatório seção 6 e medicoes_nativas.json | Dois ELF compilados; GNU size; link da execução bem-sucedida |
| Registradores como BSRR versus digitalWrite | Relatório seção 3 | Exemplo STM32 BSRR e RP2040 SET/CLR |
| Botão por interrupção e resposta em até 2 s | main.py e relatório seções 4 e 5 | Amarelo no próximo ciclo; vermelho após alerta de 2 s mais latência; sem garantia formal de tempo real do interpretador |
| Pitch do código e simulador | roteiro_apresentacao.md | Roteiro de cinco minutos; apresentação oral é realizada pelo grupo |
| Entrega em 09/11 e pasta da disciplina | README | Ano e pasta são definidos pela turma; não foi feita postagem em nome do aluno |
| Identificação | Primeira página do relatório | Nomes, RAs, curso, turma e cidade precisam ser preenchidos pelo grupo |

## Pontuação

| Critério | Pontos |
| --- | ---: |
| Etapa 01 | 500 |
| Etapa 02 diagrama e relatório | 300 |
| Etapa 02 pitch com cenário | 500 |
| Desafio | 200 |
| Total | 1500 |

A prática principal usa MicroPython no Pico, conforme pedido do aluno. A comparação AVR/ARM foi acrescentada em anexo nativo para cumprir a medição de binários. As fotos citam Arduino/C++ e C embarcado; a aceitação da linguagem Python na demonstração segue as orientações do professor.
