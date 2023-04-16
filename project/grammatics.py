from typing import Union

import pydot
from networkx import MultiDiGraph, drawing
from pyformlang.cfg import CFG, Variable


def convert_to_weak_form(cfg: CFG) -> CFG:
    cleared_cfg = cfg.eliminate_unit_productions().remove_useless_symbols()

    weak_cfg = cleared_cfg._get_productions_with_only_single_terminals()
    weak_cfg = cleared_cfg._decompose_productions(weak_cfg)
    return CFG(start_symbol=cleared_cfg.start_symbol, productions=set(weak_cfg))



