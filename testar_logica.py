"""Testes de estados e integracao com stubs; nao substituem o Wokwi."""
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest

ROOT = Path(__file__).resolve().parent
PERIOD = 1 << 30
clock = types.SimpleNamespace(now=0)
import time
time.ticks_ms = lambda: clock.now % PERIOD
time.ticks_diff = lambda a, b: (a - b + PERIOD // 2) % PERIOD - PERIOD // 2
CODE_ROOT = ROOT / 'wokwi' if (ROOT / 'wokwi/main.py').exists() else ROOT
spec = importlib.util.spec_from_file_location('semaforo', CODE_ROOT / 'main.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Logica(unittest.TestCase):
    def test_ciclo_limites(self):
        s = m.Semaforo(0)
        for instante, estado in [(0, 0), (4999, 0), (5000, 1), (9999, 1),
                                 (10000, 2), (11999, 2), (12000, 0), (17000, 1)]:
            s.atualizar(instante)
            self.assertEqual(s.estado, estado)

    def test_botao_verde(self):
        s = m.Semaforo(0)
        s.atualizar(5000)
        s.atualizar(5100, True)
        self.assertEqual(s.estado, m.AMARELO)
        s.atualizar(7099)
        self.assertEqual(s.estado, m.AMARELO)
        s.atualizar(7100)
        self.assertEqual(s.estado, m.VERMELHO)

    def test_botao_amarelo_nao_prolonga(self):
        s = m.Semaforo(0)
        s.atualizar(5000)
        s.atualizar(10000)
        for instante in [10001, 10100, 11000, 11999]:
            s.atualizar(instante, True)
        s.atualizar(12000)
        self.assertEqual(s.estado, m.VERMELHO)

    def test_botao_vermelho_renova_janela(self):
        s = m.Semaforo(0)
        s.atualizar(4999, True)
        s.atualizar(9998)
        self.assertEqual(s.estado, m.VERMELHO)
        s.atualizar(9999)
        self.assertEqual(s.estado, m.VERDE)

    def test_wrap_contador(self):
        inicio = PERIOD - 2000
        s = m.Semaforo(inicio)
        s.atualizar((inicio + 4999) % PERIOD)
        self.assertEqual(s.estado, m.VERMELHO)
        s.atualizar((inicio + 5000) % PERIOD)
        self.assertEqual(s.estado, m.VERDE)

    def test_x_configuravel_limita_bonus(self):
        antigo = m.T_AMARELO_MS
        try:
            m.T_AMARELO_MS = 8000
            s = m.Semaforo(0)
            s.atualizar(5000)
            s.atualizar(10000)
            s.atualizar(10100, True)
            s.atualizar(12100)
            self.assertEqual(s.estado, m.VERMELHO)
        finally:
            m.T_AMARELO_MS = antigo

    def test_diagrama(self):
        d = json.loads((CODE_ROOT / 'diagram.json').read_text(encoding='utf-8'))
        ids = {p['id'] for p in d['parts']}
        self.assertEqual(len(ids), len(d['parts']))
        self.assertEqual(sum(p['type'] == 'wokwi-led' for p in d['parts']), 3)
        for a, b, *_ in d['connections']:
            self.assertIn(a.split(':')[0], ids)
            self.assertIn(b.split(':')[0], ids)

    def test_integracao_irq_registradores_debounce(self):
        class Fim(Exception):
            pass

        history = []
        class Mem:
            value = 0
            def __setitem__(self, addr, value):
                if addr == 0xD0000018:
                    self.value &= ~value
                elif addr == 0xD0000014:
                    self.value |= value
                else:
                    raise AssertionError(hex(addr))
                self_value = self.value
                assert self_value == 0 or self_value & (self_value - 1) == 0
                if addr == 0xD0000014:
                    history.append((clock.now, self.value))

        class Pin:
            OUT, IN, PULL_UP, IRQ_FALLING = 1, 0, 2, 4
            instances = {}
            def __init__(self, number, mode, pull=None, **kwargs):
                self.number, self.level, self.handler = number, 1, None
                self.instances[number] = self
            def value(self):
                return self.level
            def irq(self, trigger, handler, hard):
                self.handler = handler

        # Primeiro pedido com bounce; segundo pedido durante vermelho;
        # botao mantido baixo por 6 s nao deve renovar repetidamente.
        events = {5100: 0, 5102: 1, 5103: 0, 5200: 1,
                  8000: 0, 14000: 1}
        def tick():
            clock.now += 1
            if clock.now > 14500:
                raise Fim()
            if clock.now in events:
                button = Pin.instances[16]
                previous = button.level
                button.level = events[clock.now]
                if previous == 1 and button.level == 0:
                    button.handler(button)
            return clock.now

        machine = types.ModuleType('machine')
        machine.Pin, machine.mem32 = Pin, Mem()
        machine.disable_irq = lambda: 0
        machine.enable_irq = lambda state: None
        micro = types.ModuleType('micropython')
        micro.alloc_emergency_exception_buf = lambda n: None
        sys.modules['machine'], sys.modules['micropython'] = machine, micro
        old = m.ticks_ms
        clock.now, m._evento_irq = 0, 0
        m.ticks_ms = tick
        try:
            with self.assertRaises(Fim):
                m.executar()
        finally:
            m.ticks_ms = old
        self.assertEqual([v for _, v in history], [1 << 13, 1 << 15, 1 << 14,
                                                   1 << 13, 1 << 15])
        self.assertLessEqual(history[2][0] - 5100, 2)
        self.assertLessEqual(history[3][0] - history[2][0], 2001)
        self.assertTrue(13000 <= history[4][0] <= 13002)


if __name__ == '__main__':
    unittest.main(verbosity=2)
