import io
import sys

from project.language.interpreter import interpreter

dataset_name = "travel"
dataset_nodes = 131
dataset_edges = 277
dataset_starts = 131
dataset_finals = 1


def _parse_as_set(set_str: str):
    return set(set_str.strip()[1:-1].split(", "))


def test_simple_show():
    stream = io.StringIO()
    with stream as sys.stdout:
        interpreter('show "Hello world!";')
        assert stream.getvalue().strip() == "Hello world!"


def test_vars_and_show():
    stream = io.StringIO()
    with stream as sys.stdout:
        interpreter(
            """
        var v1 = "Hello world!";
        var v2 = 54;
        var v3 = {1..3};
        show v1;
        show v2;
        show v3;
        """
        )
        result = stream.getvalue().splitlines()
        assert result[0].strip() == "Hello world!"
        assert result[1].strip() == "54"
        assert _parse_as_set(result[2]) == {str(i) for i in range(1, 4)}


def test_arithmetic():
    stream = io.StringIO()
    with stream as sys.stdout:
        interpreter(
            """
            var first = 5;
            var second = 100;
            show first + first;
            show first * second;
            show second / first;
            show second - first;
            show (first + first) == (first * 2);
            """
        )

        result = stream.getvalue().splitlines()
        assert result[0].strip() == "10"
        assert result[1].strip() == "500"
        assert result[2].strip() == "20"
        assert result[3].strip() == "95"
        assert result[4].strip() == "True"


def test_set_operations():
    stream = io.StringIO()
    with stream as sys.stdout:
        interpreter(
            """
            var first = {1, 3 - 1, 3, (3 + 1), 5};
            var second = {1..5};
            var third = {3..20};
            show first == second;
            show first ++ third;
            show third - first;
            """
        )

        result = stream.getvalue().splitlines()
        assert result[0].strip() == "True"
        assert _parse_as_set(result[1]) == {str(i) for i in range(1, 21)}
        assert _parse_as_set(result[2]) == {str(i) for i in range(6, 21)}


def test_load_and_getters():
    stream = io.StringIO()
    with stream as sys.stdout:
        interpreter(
            f"""
            var graph = import "{dataset_name}";
            show vertices >> graph;
            show edges >> graph;
            """
        )

        result = stream.getvalue().splitlines()
        assert len(result[0].strip().split(", ")) == dataset_nodes
        assert len(result[1].strip().split("), (")) == dataset_edges


def test_lambda_modify():
    stream = io.StringIO()
    with stream as sys.stdout:
        limit = 10
        interpreter(
            f"""
            var temp = {{1..{limit}}};
            show (x -> x * x) => temp;
            show (x -> x % 3 == 0) ?=> temp;
            """
        )
        result = stream.getvalue().splitlines()
        assert _parse_as_set(result[0]) == {str(i * i) for i in range(1, limit + 1)}
        assert _parse_as_set(result[1]) == {
            str(i) for i in range(1, limit + 1) if i % 3 == 0
        }


def test_graph_modify():
    stream = io.StringIO()
    with stream as sys.stdout:
        interpreter(
            f"""
            var v1 = import "{dataset_name}";
            show starts >> v1;
            show finals >> v1;

            var v2 = v1 starts =# {{1..4}};
            var v3 = v2 finals =# {{1}};
            var v4 = v3 finals =+ {{2..3}};

            show starts >> v4;

            show finals >> v3;
            show finals >> v4;
        """
        )

        result = stream.getvalue().splitlines()
        assert len(result[0].strip().split(", ")) == dataset_starts
        assert len(result[1].strip().split("), (")) == dataset_finals
        assert _parse_as_set(result[2]) == {str(i) for i in range(1, 5)}
        assert _parse_as_set(result[3]) == {"1"}
        assert _parse_as_set(result[4]) == {str(i) for i in range(1, 4)}
