import cfpq_data as cfpq
import pytest
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable, Production, Terminal

from project import grammatics


def assert_cfgs(first: CFG, second: CFG):
    assert first.start_symbol == second.start_symbol
    assert first.productions == second.productions


def test_cfg_to_wcnf():
    initial = CFG.from_text("S -> a b")
    actual = grammatics.convert_to_weak_form(initial)
    excepted = CFG.from_text(
        'S -> "VAR:a#CNF#" "VAR:b#CNF#" \n "VAR:a#CNF#" -> a \n "VAR:b#CNF#" -> b'
    )

    assert_cfgs(actual, excepted)


def test_cfg_to_wcnf_complex():
    initial = CFG.from_text("S -> A S B | c\nB -> b\nA -> a")
    actual = grammatics.convert_to_weak_form(initial)
    excepted = CFG.from_text('S -> A "VAR:C#CNF#1" | c\nC#CNF#1 -> S B\nB -> b\nA -> a')

    assert_cfgs(actual, excepted)


