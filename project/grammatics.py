from typing import Union

import pydot
from networkx import MultiDiGraph, drawing
from pyformlang.cfg import CFG, Variable


def convert_to_weak_form(cfg: CFG) -> CFG:
    cleared_cfg = cfg.eliminate_unit_productions().remove_useless_symbols()

    weak_cfg = cleared_cfg._get_productions_with_only_single_terminals()
    weak_cfg = cleared_cfg._decompose_productions(weak_cfg)
    return CFG(start_symbol=cleared_cfg.start_symbol, productions=set(weak_cfg))


def query_graph_with_cfg(
    graph: MultiDiGraph,
    cfg: Union[CFG, str],
    start_nodes: set = None,
    final_nodes: set = None,
    start_symbol: Variable = Variable("S"),
):
    start_nodes = graph.nodes if start_nodes is None else start_nodes
    final_nodes = graph.nodes if final_nodes is None else final_nodes

    return {
        (u, v)
        for (variable, u, v) in hellings_algorithm(graph, cfg)
        if variable == start_symbol and u in start_nodes and v in final_nodes
    }


def hellings_algorithm(graph: Union[MultiDiGraph, str], cfg: Union[CFG, str]):
    if isinstance(graph, str):
        graph = drawing.nx_pydot.from_pydot(pydot.graph_from_dot_data(graph)[0])
    if isinstance(cfg, str):
        cfg = CFG.from_text(cfg)

    cfg = convert_to_weak_form(cfg)

    result = set()
    variables_prod = set()
    for prod in cfg.productions:
        if len(prod.body) == 1:
            for (v, u, label) in graph.edges(data="label"):
                if label == prod.body[0].value:
                    result.add((prod.head, v, u))
        elif len(prod.body) != 2:
            for n in graph.nodes:
                result.add((prod.head, n, n))
        else:
            variables_prod.add(prod)

    queue = list(result)

    while len(queue) > 0:
        (var1, v, u) = queue.pop()
        to_append = set()
        for var2, v1, u1 in result:
            if v == u1:
                for prod in variables_prod:
                    closure = (prod.head, v1, u)
                    if prod.body[0] == var2 and prod.body[1] == var1 and closure not in result:
                        to_append.add(closure)
                        queue.append(closure)
            if u == v1:
                for prod in variables_prod:
                    closure = (prod.head, v, u1)
                    if prod.body[0] == var1 and prod.body[1] == var2 and closure not in result:
                        to_append.add(closure)
                        queue.append(closure)
        result = result.union(to_append)
    return result
