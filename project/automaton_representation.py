from typing import Dict, Set, Any

from pyformlang.finite_automaton import FiniteAutomaton, State, EpsilonNFA
from scipy.sparse import dok_matrix, kron


class AutomatonRepresentation:
    def __init__(self, start_states: Set = None,
                 final_states: Set = None,
                 states: Dict[State, int] = None,
                 transitions: Dict[Any, dok_matrix] = None):

        self.start_states: Set = start_states if start_states is not None else set()
        self.final_states: Set = final_states if final_states is not None else set()
        self.states: Dict[State, int] = states if states is not None else dict()
        self.transitions_matrix: Dict[Any, dok_matrix] = transitions if transitions is not None else dict()

    @classmethod
    def from_automaton(cls, automaton: FiniteAutomaton):
        result = cls(automaton.start_states, automaton.final_states)
        result.states = {value: i for i, value in enumerate(automaton.states)}

        states_count = len(automaton.states)
        transitions = automaton.to_dict()

        for from_state in transitions.keys():
            for label in transitions[from_state].keys():
                if not isinstance(transitions[from_state][label], set):
                    transitions[from_state][label] = {transitions[from_state][label]}

                for to_state in transitions[from_state][label]:
                    if label not in result.transitions_matrix:
                        result.transitions_matrix[label] = dok_matrix((states_count, states_count), dtype=bool)
                    result.transitions_matrix[label][(result.states[from_state]), (result.states[to_state])] = True

        return result

    def to_automaton(self) -> EpsilonNFA:
        automaton = EpsilonNFA()
        for symbol in self.transitions_matrix.keys():
            for state_from, state_to in zip(*self.transitions_matrix[symbol].nonzero()):
                automaton.add_transition(state_from, symbol, state_to)

        for state in self.start_states:
            automaton.add_start_state(State(state))

        for state in self.final_states:
            automaton.add_final_state(State(state))

        return automaton

    def intersect(self, automaton):
        labels = set(self.transitions_matrix.keys()).intersection(set(automaton.transitions_matrix.keys()))
        intersection_edges = {s: kron(self.transitions_matrix[s], automaton.transitions_matrix[s]) for s in labels}

        count = len(automaton.states)
        start_states = set()
        for first in self.start_states:
            for second in automaton.start_states:
                start_states.add(self.states[first] * count + automaton.states[second])

        final_states = set()
        for first in self.final_states:
            for second in automaton.final_states:
                final_states.add(self.states[first] * count + automaton.states[second])

        return AutomatonRepresentation(start_states, final_states, {v: i for i, v in enumerate(labels)}, intersection_edges)

    def transitive_closure(self) -> dok_matrix:
        if len(self.transitions_matrix) != 0:
            matrix = sum(self.transitions_matrix.values())
            previous = matrix.nnz
            current = 0
            while previous != current:
                matrix += matrix @ matrix
                previous = current
                current = matrix.nnz
        else:
            matrix = dok_matrix((0, 0), dtype=bool)
        return matrix
