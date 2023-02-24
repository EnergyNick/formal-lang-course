import cfpq_data as cfpq
import networkx as ntwx
from collections import namedtuple

GraphInfo = namedtuple("GraphInfo", ["nodes_count", "edges_count", "labels"])


def get_graph_info_from_dataset(name: str) -> GraphInfo:
    csv_path = cfpq.download(name)
    graph = cfpq.graph_from_csv(csv_path)
    return get_graph_info(graph)


def get_graph_info(graph: ntwx.Graph) -> GraphInfo:
    labels = list(set(attributes["label"] for (_, _, attributes) in graph.edges.data()))
    return GraphInfo(graph.number_of_nodes(), graph.number_of_edges(), labels)


def save_graph_to_file(graph: ntwx.Graph, file_path: str):
    pydot_graph = ntwx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write_raw(file_path)


def create_two_cycles_graph_to_file(file_path: str,
                                    first_nodes: int, first_label: str,
                                    second_nodes: int, second_label: str):
    graph = cfpq.labeled_two_cycles_graph(n=first_nodes, m=second_nodes, labels=(first_label, second_label))
    save_graph_to_file(graph, file_path)
