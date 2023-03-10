import networkx as ntwx
import pyformlang.finite_automaton as auto
from pyformlang.regular_expression import PythonRegex


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
