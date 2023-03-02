import networkx as ntwx
import pyformlang.finite_automaton as auto
from pyformlang.regular_expression import Regex


def build_minimal_dfa_from_regex(raw_regex: str) -> auto.DeterministicFiniteAutomaton:
    regex = Regex(raw_regex)
    return regex.to_epsilon_nfa().minimize()


def build_nfa_from_graph(
    graph: ntwx.Graph, start_nodes=None, end_nodes=None
) -> auto.EpsilonNFA:
    result = auto.NondeterministicFiniteAutomaton.from_networkx(graph)
    to_start = start_nodes if start_nodes is not None else graph.nodes
    to_end = end_nodes if end_nodes is not None else graph.nodes

    for node in to_start:
        result.add_start_state(node)
    for node in to_end:
        result.add_final_state(node)
    return result
