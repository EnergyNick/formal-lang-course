import filecmp
import os.path

import cfpq_data as cfpq
import pytest
from pyformlang.cfg import CFG, Variable, Production, Terminal

from project import utilities


def test_get_info():
    initial = cfpq.labeled_two_cycles_graph(4, 8, labels=("first", "second"))

    info = utilities.get_graph_info(initial)
    assert info.nodes_count == initial.number_of_nodes()
    assert info.edges_count == initial.number_of_edges()
    assert set(info.labels) == {"first", "second"}


def test_incorrect_get_info_from_dataset():
    with pytest.raises(Exception):
        utilities.get_graph_info_from_dataset("PYTHON IS OOP FUNCTIONAL LANGUAGE")


def test_get_info_from_dataset():
    dataset_name = "travel"
    dataset_nodes = 131
    dataset_edges = 277

    info = utilities.get_graph_info_from_dataset(dataset_name)
    assert info.nodes_count == dataset_nodes
    assert info.edges_count == dataset_edges


def test_build_graph_to_file(tmp_path: str):
    first_nodes = 5
    first_label = "first"
    second_nodes = 5
    second_label = "second"

    expected = "expected.dot"
    expected_path = os.path.join(tmp_path, expected)
    expected_graph = cfpq.labeled_two_cycles_graph(
        first_nodes, second_nodes, labels=(first_label, second_label)
    )
    utilities.save_graph_to_file(expected_graph, expected_path)

    actual = "actual.dot"
    actual_path = os.path.join(tmp_path, actual)
    utilities.create_two_cycles_graph_to_file(
        actual_path, first_nodes, first_label, second_nodes, second_label
    )

    assert filecmp.cmp(actual_path, expected_path)


def assert_cfgs(first: CFG, second: CFG):
    assert first.start_symbol == second.start_symbol
    assert first.productions == second.productions


def test_cfg_from_file(tmpdir):
    path = tmpdir + 'test.txt'
    with open(path, 'w') as f:
        f.write("S -> A\nA -> B\nB -> b")

    actual = utilities.parse_cfg_from_file(path)
    varS = Variable("S")
    varA = Variable("A")
    varB = Variable("B")
    productions = {
        Production(varA, [varB]),
        Production(varS, [varA]),
        Production(varB, [Terminal("b")]),
    }
    expected = CFG(productions=productions, start_symbol=varS)

    assert_cfgs(actual, expected)


def test_cfg_to_wcnf():
    initial = CFG.from_text("S -> a b")
    actual = utilities.convert_to_weak_form(initial)
    excepted = CFG.from_text(
        'S -> "VAR:a#CNF#" "VAR:b#CNF#" \n "VAR:a#CNF#" -> a \n "VAR:b#CNF#" -> b'
    )

    assert_cfgs(actual, excepted)


def test_cfg_to_wcnf_complex():
    initial = CFG.from_text("S -> A S B | c\nB -> b\nA -> a")
    actual = utilities.convert_to_weak_form(initial)
    excepted = CFG.from_text('S -> A "VAR:C#CNF#1" | c\nC#CNF#1 -> S B\nB -> b\nA -> a')

    assert_cfgs(actual, excepted)
