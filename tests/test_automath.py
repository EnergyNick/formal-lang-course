import itertools
import cfpq_data as cfpq
import networkx as nx
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)

from project import automath, utilities


def generate_graph(n, m, labels=("first", "second")):
    return cfpq.labeled_two_cycles_graph(n, m, labels=labels)


def test_equivalence_min_dfa_by_regex():
    dfa = automath.build_minimal_dfa_from_text("xy(z)")

    expected_dfa = DeterministicFiniteAutomaton()
    st0 = State(0)
    st23 = State("2;3")
    st45 = State("4;5")
    st1 = State(1)
    expected_dfa.add_start_state(st0)
    expected_dfa.add_final_state(st1)
    expected_dfa.add_transitions(
        [(st45, "z", st1), (st23, "y", st45), (st0, "x", st23)]
    )

    assert dfa.is_equivalent_to(expected_dfa)
    assert dfa == dfa.minimize()


def test_create_nfa_with_correct_unsetted_start_and_end_states():
    graph = generate_graph(4, 8)
    nfa = automath.build_nfa_from_graph(graph)

    info = utilities.get_graph_info(graph)
    nodes = set(graph.nodes.keys())
    assert nfa.get_number_transitions() == info.nodes_count + 1
    assert nfa.start_states == nodes
    assert nfa.final_states == nodes


def test_create_nfa_with_correct_start_and_end_states():
    graph = generate_graph(4, 8)
    start_states = [0, 3]
    end_states = [2, 7, 8]
    nfa = automath.build_nfa_from_graph(graph, start_states, end_states)

    info = utilities.get_graph_info(graph)
    assert nfa.get_number_transitions() == info.nodes_count + 1
    assert nfa.start_states == set(start_states)
    assert nfa.final_states == set(end_states)


def test_equivalence_nfa_by_graph():
    graph = generate_graph(1, 3)
    nfa = automath.build_nfa_from_graph(graph, [0], [2, 3])

    expected_nfa = NondeterministicFiniteAutomaton()

    st0 = State(0)
    st1 = State(1)
    st2 = State(2)
    st3 = State(3)
    st4 = State(4)

    first = Symbol("first")
    second = Symbol("second")

    expected_nfa.add_start_state(st0)
    expected_nfa.add_final_state(st2)
    expected_nfa.add_final_state(st3)

    expected_nfa.add_transitions(
        [
            (st0, first, st1),
            (st1, first, st0),
            (st0, second, st2),
            (st4, second, st0),
            (st3, second, st4),
            (st2, second, st3),
        ]
    )

    assert nfa.is_equivalent_to(expected_nfa)


def test_intersect():
    regexes = ["abc def", "abc def*", "abc def | def abc", "xy z | a b*"]
    automates = [automath.build_minimal_dfa_from_text(expr) for expr in regexes]
    for first, second in itertools.product(automates, automates):
        expected = first.get_intersection(second)
        got = automath.intersect(first, second)
        assert expected.is_equivalent_to(got)


def test_query():
    regex = "d*a*n*i*e*l*"
    graph = generate_graph(3, 3, labels=("a", "b"))
    start_states = {0}
    final_states = {1, 2, 3}

    actual = automath.query_regex_graph(regex, graph, start_states, final_states)
    assert actual == {(0, 1), (0, 2), (0, 3)}


def test_bfs_query():
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])
    edges = [(0, "a", 1), (1, "a", 2)]
    graph.add_edges_from(list(map(lambda x: (x[0], x[2], {"label": x[1]}), edges)))

    start_nodes = {0, 1}
    query_with_end = automath.rpq_by_bfs(graph, "a*", start_nodes, {2}, True)
    query_complex = automath.rpq_by_bfs(graph, "a*", start_nodes, None, False)

    assert query_with_end == {(1, 2), (0, 2)}
    assert query_complex == {1, 2}
