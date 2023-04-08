from pyformlang.cfg import Variable, CFG
from pyformlang.finite_automaton import State
from pyformlang.regular_expression import Regex

from project.ecfg import ECFG
from project.recursive_automath import RecursiveAutomaton
from project import automath


def test_convert_cfg_to_ecfg():
    initial = CFG.from_text("S -> A S B | c\nB -> b\nA -> a")
    ecfg = ECFG.from_cfg(initial)
    expected_production = {
        Variable("S"): Regex("A S B | c"),
        Variable("B"): Regex("b"),
        Variable("A"): Regex("a"),
    }
    for key in expected_production.keys():
        actual = automath.build_minimal_dfa_from_regex(ecfg.productions[key])
        expected = automath.build_minimal_dfa_from_regex(expected_production[key])

        if actual.is_empty() and expected.is_empty():
            continue
        assert expected.is_equivalent_to(actual)


def test_convert_ecfg_to_recursive_automath():
    initial = CFG.from_text("S -> A S B | c\nB -> b\nA -> a")
    ecfg = ECFG.from_cfg(initial)
    expected_production = {
        Variable("S"): Regex("A S B | c"),
        Variable("B"): Regex("b"),
        Variable("A"): Regex("a"),
    }

    actual = RecursiveAutomaton.from_ecfg(ecfg)
    for key in expected_production.keys():
        expected = automath.build_minimal_dfa_from_regex(expected_production[key])

        if actual.boxes[key].is_empty() and expected.is_empty():
            continue
        assert actual.boxes[key].is_equivalent_to(expected)


def test_convert_to_adjacency_matrices():
    recursive = RecursiveAutomaton.from_ecfg(ECFG.from_text("S -> a S b | c"))
    states, matrix = recursive.to_matrices()
    assert len(states) == 10
    assert len(matrix) == 5
    assert len(matrix[State("S")]) == 1
    assert len(matrix[State("a")]) == 1
    assert len(matrix[State("b")]) == 1
    assert len(matrix[State("c")]) == 1
