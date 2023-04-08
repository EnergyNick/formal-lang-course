from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA

from project.ecfg import ECFG


class RecursiveAutomaton:
    """
    Class of recursive finite automaton
    """

    def __init__(self, start_symbol: Variable, boxes: dict[Variable, EpsilonNFA]):
        self.start_symbol: Variable = start_symbol
        self.boxes: dict[Variable, EpsilonNFA] = boxes

    def minimize(self):
        """
        Minimize automaton
        :return:
        """
        for variable, automate in self.boxes.items():
            self.boxes[variable] = automate.minimize()
        return self

    @classmethod
    def from_ecfg(cls, ecfg: ECFG):
        """
        Create recursive automation from extended context-free grammar
        :param ecfg: original grammar
        :return: recursive automation of grammar
        """
        elements = {
            head: body.to_epsilon_nfa() for head, body in ecfg.productions.items()
        }
        return cls(ecfg.start_symbol, elements)
