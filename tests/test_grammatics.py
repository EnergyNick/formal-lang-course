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


def get_graph_with_cfg() -> tuple[MultiDiGraph, str]:
    graph_edges = [
        (0, 1, {"label": "a"}),
        (2, 0, {"label": "a"}),
        (1, 2, {"label": "a"}),
        (2, 3, {"label": "b"}),
        (3, 2, {"label": "b"}),
    ]
    graph = MultiDiGraph()
    graph.add_edges_from(graph_edges)

    cfg = """
            S -> A B
            S -> A C
            A -> a
            B -> b
            C -> S B
           """

    return graph, cfg


def test_helings_algorithm():
    graph, cfg = get_graph_with_cfg()

    expected = {
        (Variable("A"), 0, 1),
        (Variable("A"), 1, 2),
        (Variable("A"), 2, 0),
        (Variable("B"), 2, 3),
        (Variable("B"), 3, 2)
    }
    expected = expected.union([(Variable("C"), i, j) for j in range(2, 4) for i in range(0, 3)])
    expected = expected.union([(Variable("S"), i, j) for j in range(2, 4) for i in range(0, 3)])

    hellings_result = grammatics.hellings_algorithm(graph, cfg)
    assert len(hellings_result.difference(expected)) == 0


def test_query_cfg_graph():
    graph, cfg = get_graph_with_cfg()

    start_nodes = {0, 2}
    final_nodes = {3}

    query_result = grammatics.query_graph_with_cfg(graph, cfg, start_nodes, final_nodes)
    assert query_result == {(0, 3), (2, 3)}
