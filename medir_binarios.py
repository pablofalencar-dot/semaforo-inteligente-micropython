"""Executado no GitHub Actions depois das duas compilacoes Arduino CLI."""
from pathlib import Path
import json
import os
import subprocess

resultados = []
for alvo, prefixo, fqbn in [('avr', 'avr', 'arduino:avr:uno'),
                            ('arm', 'arm-none-eabi', 'rp2040:rp2040:rpipico')]:
    elf = next(Path('build', alvo).glob('*.elf'))
    size = next(p for p in (Path.home()/'.arduino15/packages').rglob(prefixo+'-size') if p.is_file())
    saida = subprocess.check_output([str(size), '-B', str(elf)], text=True)
    print(alvo, saida)
    campos = saida.splitlines()[-1].split()
    texto, dados, bss = map(int, campos[:3])
    resultados.append(dict(alvo=alvo, fqbn=fqbn, text=texto, data=dados, bss=bss,
                           flash_bytes=texto+dados, ram_estatica_bytes=dados+bss,
                           elf_bytes=elf.stat().st_size))
Path('build/resultados.json').write_text(json.dumps(resultados, indent=2))
linhas = ['## Comparacao medida dos firmwares nativos',
          '| Alvo | text | data | bss | Flash text+data | RAM data+bss |',
          '| --- | ---: | ---: | ---: | ---: | ---: |']
for r in resultados:
    linhas.append('| {alvo} | {text} | {data} | {bss} | {flash_bytes} | {ram_estatica_bytes} |'.format(**r))
linhas += ['', 'Todos os valores em bytes. RAM estatica exclui pilha e heap.',
           'Esta medicao inclui os respectivos cores Arduino. A pratica Python e separada.',
           'AVR usa digitalWrite; RP2040 usa SIO direto. Nao isola apenas a ISA.']
resumo = '\n'.join(linhas)+'\n'
print(resumo)
Path('build/medicao.md').write_text(resumo)
with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as f:
    f.write(resumo)
