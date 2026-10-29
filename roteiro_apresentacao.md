# Roteiro de apresentacao de aproximadamente cinco minutos

## 1 Abertura e objetivo — 40 segundos

“Nosso projeto e um semaforo inteligente implementado em Python, na versao MicroPython, em um Raspberry Pi Pico com RP2040. O objetivo e demonstrar uma maquina de estados, temporizacao sem bloqueio e atendimento de pedestre por interrupcao de hardware. No relatorio, comparamos esse ARM de 32 bits com o ATmega328P de 8 bits do Arduino Uno.”

## 2 Circuito — 40 segundos

Mostre o diagrama no Wokwi. “Usamos tres LEDs com resistores de 330 ohms. Os pinos GP13, GP14 e GP15 acionam vermelho, amarelo e verde. O botao liga GP16 ao terra; o pull-up interno mantem a entrada alta quando ele esta solto. Os LEDs mostram o sinal dos veiculos.”

## 3 Funcionamento e codigo — um minuto

“O estado inicial e vermelho por cinco segundos. Depois vem verde por cinco segundos e amarelo por dois segundos, voltando ao vermelho. A classe Semaforo guarda o estado atual, o instante de entrada e a duracao. O programa consulta ticks_ms e usa ticks_diff para verificar o intervalo, inclusive quando o contador retorna a zero. Nao usamos delay nem sleep para contar o tempo. O laco fica disponivel para processar eventos.”

Mostre as constantes de tempo e `atualizar`. Mostre o diagrama de estados do PDF.

## 4 Demonstracao do bonus — um minuto

Espere o verde e aperte o botao. “O evento eletrico dispara uma interrupcao na borda de descida. A rotina de interrupcao apenas sinaliza o pedido. O programa principal muda para amarelo imediatamente e depois para vermelho. Durante o amarelo, outro pedido nao aumenta a espera. Durante o vermelho, um pedido renova a janela de travessia. O botao precisa ficar solto por 50 milissegundos para rearmar, evitando varios pedidos por ruido mecanico.”

Mantenha o botao pressionado; solte e pressione novamente. Use os segundos do simulador, nao o relogio da gravacao, se o navegador estiver lento.

## 5 Comparacao tecnica — um minuto

“O Uno trabalha com dados de oito bits, enquanto o Cortex-M0+ possui registradores de 32 bits. Uma soma de 32 bits exige varias operacoes no AVR. Isso nao significa que todo programa ARM sera quatro vezes mais rapido. Nenhuma das duas CPUs tem FPU; calculos de ponto flutuante dependem de software. No Pico, escrevemos nos registradores GPIO_OUT_CLR e GPIO_OUT_SET por machine.mem32. No STM32 o exemplo equivalente e BSRR, mas os enderecos sao diferentes. Python continua tendo o custo do interpretador, por isso nao afirmamos que essas duas linhas viram apenas duas instrucoes da CPU.”

## 6 Encerramento e limites — 40 segundos

“A solucao demonstra a logica nao bloqueante e o atendimento ao pedestre. Oito testes locais passaram e o projeto foi executado no Wokwi. O tamanho de main.py mede o fonte, nao o firmware ARM completo. Por isso compilamos um anexo nativo para as duas plataformas: a estimativa de Flash foi 1764 bytes no AVR e 327276 bytes no ARM, incluindo os respectivos cores e bibliotecas. Esses numeros comparam os firmwares completos e nao isolam apenas a arquitetura.”

## Perguntas que podem aparecer

- Por que nao Python no Uno? Os 2 KiB de SRAM do ATmega328P nao comportam a implementacao usual do MicroPython; a plataforma indicada para este projeto Python e o Pico.
- O que significa FSM? Maquina de Estados Finitos; cada cor e um estado, e tempo e botao determinam as transicoes.
- Por que ticks_diff? Porque a contagem e modular, e subtrair diretamente pode falhar no retorno a zero.
- Por que nao realizar todo o trabalho na interrupcao? Para reduzir a duracao da ISR e evitar bloqueios e alocacoes em contexto de interrupcao.
- O botao chega ao vermelho em exatamente 2 s? A resposta amarela e imediata na logica; o vermelho vem apos o intervalo amarelo mais a latencia do programa. Nao existe garantia formal de prazo estrito no interpretador.
- Harvard e sinonimo de AVR? Nao. E uma organizacao de memoria; o Cortex-M3 tambem utiliza caminhos separados para instrucoes e dados, com mapa de enderecos unificado.
- Qual e o tamanho dos binarios? A estimativa de Flash foi 1764 bytes no AVR e 327276 bytes no ARM; RAM estatica de 44 e 18684 bytes. Mostre a secao 6 e a execucao no GitHub Actions. Os totais incluem os cores; nao confunda fonte, UF2, Intel HEX e ocupacao de Flash.
