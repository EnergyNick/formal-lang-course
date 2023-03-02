import cfpq_data as cfpq
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton, State, Symbol

from project import automath
from project import utilities


def generate_graph():
    return cfpq.labeled_two_cycles_graph(4, 8, labels=("first", "second"))


def generate_small_graph():
    return cfpq.labeled_two_cycles_graph(1, 3, labels=("first", "second"))


def test_equivalence_min_dfa_by_regex():
    dfa = automath.build_minimal_dfa_from_regex("xy(z)")

    expected_dfa = DeterministicFiniteAutomaton()
    st0 = State(0)
    st23 = State("2;3")
    st1 = State(1)
    expected_dfa.add_start_state(st0)
    expected_dfa.add_final_state(st1)
    expected_dfa.add_transitions([(st0, "xy", st23), (st23, "z", st1)])

    assert dfa.is_equivalent_to(expected_dfa)
    assert dfa == dfa.minimize()


def test_create_nfa_with_correct_unsetted_start_and_end_states():
    graph = generate_graph()
    nfa = automath.build_nfa_from_graph(graph)

    info = utilities.get_graph_info(graph)
    nodes = set(graph.nodes.keys())
    assert nfa.get_number_transitions() == info.nodes_count + 1
    assert nfa.start_states == nodes
    assert nfa.final_states == nodes


def test_create_nfa_with_correct_start_and_end_states():
    graph = generate_graph()
    start_states = [0, 3]
    end_states = [2, 7, 8]
    nfa = automath.build_nfa_from_graph(graph, start_states, end_states)

    info = utilities.get_graph_info(graph)
    assert nfa.get_number_transitions() == info.nodes_count + 1
    assert nfa.start_states == set(start_states)
    assert nfa.final_states == set(end_states)


def test_equivalence_nfa_by_graph():
    graph = generate_small_graph()
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

    expected_nfa.add_transitions([(st0, first, st1),
                                 (st1, first, st0),
                                 (st0, second, st2),
                                 (st4, second, st0),
                                 (st3, second, st4),
                                 (st2, second, st3)])

    assert nfa.is_equivalent_to(expected_nfa)
