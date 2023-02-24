import filecmp
import os.path
import cfpq_data as cfpq
import pytest

from project import utilities


def test_get_info():
    initial = cfpq.labeled_two_cycles_graph(4, 8, labels=("first", "second"))

    info = utilities.get_graph_info(initial)
    assert info.nodes_count == initial.number_of_nodes()
    assert info.edges_count == initial.number_of_edges()
    assert info.labels == ["first", "second"]


def test_incorrect_get_info_from_dataset():
    with pytest.raises(Exception):
        utilities.get_graph_info_from_dataset("PYTHON IS OOP FUNCTIONAL LANGUAGE")


def test_get_info_from_dataset():
    dataset_name = "travel"
    dataset_nodes = 131
    dataset_edges = 277

    info = utilities.get_graph_info_from_dataset(dataset_name)
    assert info.nodes_count == dataset_nodes
    assert info.edges_count == dataset_edges


def test_build_graph_to_file(tmp_path: str):
    first_nodes = 5
    first_label = "first"
    second_nodes = 5
    second_label = "second"

    expected = "expected.dot"
    expected_path = os.path.join(tmp_path, expected)
    expected_graph = cfpq.labeled_two_cycles_graph(
        first_nodes, second_nodes, labels=(first_label, second_label)
    )
    utilities.save_graph_to_file(expected_graph, expected_path)

    actual = "actual.dot"
    actual_path = os.path.join(tmp_path, actual)
    utilities.create_two_cycles_graph_to_file(
        actual_path, first_nodes, first_label, second_nodes, first_label
    )

    assert filecmp.cmp(actual_path, expected_path)
