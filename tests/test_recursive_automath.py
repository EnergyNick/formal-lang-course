from pyformlang.cfg import Variable, CFG
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
