import networkx as ntwx
import pyformlang.finite_automaton as auto
from pyformlang.regular_expression import PythonRegex

from project.automaton_representation import AutomatonRepresentation


def build_minimal_dfa_from_regex(raw_regex: str) -> auto.DeterministicFiniteAutomaton:
    """
    Build deterministic finite automaton from string with regular expression
    :param raw_regex: string with regular expression
    :return: Minimized automation from regex
    """
    regex = PythonRegex(raw_regex)
    return regex.to_epsilon_nfa().minimize()


def build_nfa_from_graph(
        graph: ntwx.Graph, start_nodes=None, end_nodes=None
) -> auto.EpsilonNFA:
    """
    Build nondeterministic finite automaton
    :param graph: Graph to build nfa
    :param start_nodes: Start state nodes for automaton (if None will be set all the graph nodes)
    :param end_nodes: Final state nodes for automaton (if None will be set all the graph nodes)
    :return: Default nfa from graph
    """
    result = auto.NondeterministicFiniteAutomaton.from_networkx(graph)
    to_start = start_nodes if start_nodes is not None else graph.nodes
    to_end = end_nodes if end_nodes is not None else graph.nodes

    for node in to_start:
        result.add_start_state(node)
    for node in to_end:
        result.add_final_state(node)
    return result


def intersect(first: auto.FiniteAutomaton, second: auto.FiniteAutomaton) -> auto.FiniteAutomaton:
    """
    Create automatons representing intersection of two finite automatons.
    :return:
    Intersection of two finite automatons
    """
    first_repr = AutomatonRepresentation.from_automaton(first)
    second_repr = AutomatonRepresentation.from_automaton(second)
    return first_repr.intersect(second_repr).to_automaton()


def query_regex_graph(regex: str, graph: ntwx.Graph, start_states=None, final_states=None):
    """
    Query finite automaton by regular expression.
    :param regex: string with regular expression
    :param graph: graph to search
    :param start_states: start states of graph
    :param final_states: final states of graph
    :return: set of initial and final state pairs
    """
    graph_repr = AutomatonRepresentation.from_automaton(build_nfa_from_graph(graph, start_states, final_states))
    regex_repr = AutomatonRepresentation.from_automaton(build_minimal_dfa_from_regex(regex))
    intersected = graph_repr.intersect(regex_repr)
    rows, columns = intersected.transitive_closure().nonzero()

    result = set()
    count = len(regex_repr.states)
    for row, column in zip(rows, columns):
        if row in intersected.start_states and column in intersected.final_states:
            result.add((row // count, column // count))
    return result
