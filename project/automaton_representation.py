from typing import Dict, Set, Any

from pyformlang.finite_automaton import FiniteAutomaton, State, EpsilonNFA
from scipy.sparse import dok_matrix, kron, vstack, block_diag


class AutomatonRepresentation:
    """
    Provide useful representation of automation for different operations
    """
    def __init__(
        self,
        start_states: Set = None,
        final_states: Set = None,
        states: Dict[State, int] = None,
        transitions: Dict[Any, dok_matrix] = None,
    ):

        self.start_states: Set = start_states if start_states is not None else set()
        self.final_states: Set = final_states if final_states is not None else set()
        self.states: Dict[State, int] = states if states is not None else dict()
        self.idx_to_states = {v: k for k, v in self.states.items()}
        self.transitions_matrix: Dict[Any, dok_matrix] = (
            transitions if transitions is not None else dict()
        )

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
                        result.transitions_matrix[label] = dok_matrix(
                            (states_count, states_count), dtype=bool
                        )
                    result.transitions_matrix[label][
                        (result.states[from_state]), (result.states[to_state])
                    ] = True

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

    def get_intersection_of_labels(self, other):
        return set(self.transitions_matrix.keys()).intersection(
            set(other.transitions_matrix.keys())
        )

    def intersect(self, automaton):
        labels = self.get_intersection_of_labels(automaton)
        intersection_edges = {
            s: kron(self.transitions_matrix[s], automaton.transitions_matrix[s])
            for s in labels
        }

        count = len(automaton.states)
        start_states = set()
        for first in self.start_states:
            for second in automaton.start_states:
                start_states.add(self.states[first] * count + automaton.states[second])

        final_states = set()
        for first in self.final_states:
            for second in automaton.final_states:
                final_states.add(self.states[first] * count + automaton.states[second])

        return AutomatonRepresentation(
            start_states,
            final_states,
            {v: i for i, v in enumerate(labels)},
            intersection_edges,
        )

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

    def sync_bfs(self, target_automaton, for_each_start=False):
        start_states_indices, visited = self._bfs_cycle(
            target_automaton, for_each_start
        )

        results = set()
        target_states_names = list(target_automaton.states.keys())
        self_states_names = list(self.states.keys())
        target_count = len(target_automaton.states)
        for i, j in zip(*visited.nonzero()):
            if (
                j >= target_count
                and target_states_names[i % target_count]
                in target_automaton.final_states
            ):
                current = j - target_count
                if self_states_names[current] in self.final_states:
                    element = (
                        (start_states_indices[i // target_count], current)
                        if for_each_start
                        else current
                    )
                    results.add(element)
        return results

    def build_initial(self, target_automaton, start_states_indices):
        count = len(self.states)
        target_count = len(target_automaton.states)
        initial = dok_matrix(
            (
                target_count,
                count + target_count,
            ),
            dtype=bool,
        )
        start = dok_matrix((1, count), dtype=bool)
        for i in start_states_indices:
            start[0, i] = True
        for name in target_automaton.start_states:
            i = target_automaton.states[name]
            initial[i, i] = True
            initial[i, target_count:] = start
        return initial

    def _bfs_cycle(self, target, for_each_start):
        start_states_indices = [self.states[state] for state in self.start_states]
        current = (
            vstack([self.build_initial(target, {i}) for i in start_states_indices])
            if for_each_start
            else self.build_initial(target, start_states_indices)
        )
        labels = self.get_intersection_of_labels(target)
        direct_sum = dict()
        for label in labels:
            direct_sum[label] = dok_matrix(
                block_diag(
                    (target.transitions_matrix[label], self.transitions_matrix[label])
                )
            )

        visited = dok_matrix(current.shape, dtype=bool)
        old_visited = None
        while old_visited is None or visited.nnz != old_visited.nnz:
            old_visited = visited.copy()
            for dir_sum_matrix in direct_sum.values():
                new_current = (
                    visited @ dir_sum_matrix
                    if current is None
                    else current @ dir_sum_matrix
                )
                visited += self.transform_current(target, new_current)
            current = None
        return start_states_indices, visited

    @classmethod
    def transform_current(cls, target_automaton, current):
        target_count = len(target_automaton.states)
        transformed_current = dok_matrix(current.shape, dtype=bool)
        for i, j in zip(*current.nonzero()):
            if j < target_count:
                row = current[i, target_count:]
                if row.nnz > 0:
                    each_start = i // target_count * target_count
                    transformed_current[each_start + j, j] = True
                    transformed_current[each_start + j, target_count:] += row
        return transformed_current
