from project.language.lang_parser import (
    is_text_correct_in_language,
    generate_dot_to_str,
)
from textwrap import dedent


def test_empty():
    assert is_text_correct_in_language("")
    assert is_text_correct_in_language("           ")
    assert is_text_correct_in_language(
        """
    // BABABABBA

    """
    )


def test_not_parsing():
    assert not is_text_correct_in_language("notInSet")
    assert not is_text_correct_in_language("print")
    assert not is_text_correct_in_language("var =a ")
    assert not is_text_correct_in_language('x = load "test"')
    assert not is_text_correct_in_language('var x = load "test"')
    assert not is_text_correct_in_language("{{}10 {..}}")


def test_print_fucn():
    assert is_text_correct_in_language("show 10;")
    assert is_text_correct_in_language("show {1..100};")
    assert is_text_correct_in_language("show {1, 20, 300, 4000};")
    assert is_text_correct_in_language('show import "test";')


def test_bind_statement():
    assert is_text_correct_in_language("var xv = 5;")
    assert is_text_correct_in_language("var xa = {1..100};")
    assert is_text_correct_in_language("var xd = {1, 2, 3, 5};")
    assert is_text_correct_in_language('var xxx = import "test";')


def test_lambda_statement():
    assert is_text_correct_in_language("var res = x -> x => edges >> graph ;")
    assert is_text_correct_in_language('var res = x -> (x ?> "a") ?=> edges >> graph ;')
    assert not is_text_correct_in_language("var res = x -> x;")
    assert not is_text_correct_in_language("var res = x -> show i;")


def test_example_belongs():
    assert is_text_correct_in_language(exampleShorted)
    assert is_text_correct_in_language(exampleFromLang)


def test_to_dot():
    res = generate_dot_to_str(exampleShorted)
    with open("exampleShorted.dot", "r") as file:
        expected = file.read()
    print(dedent(res))
    assert dedent(res) == dedent(expected)


exampleFromLang = """
var initial = import "TestGraph";
var extended = import "ExtendedTestGraph";

var upd1 = initial starts =+ {1..15};
var upd2 = upd1 finals =+ 0;

// Test
var upd3 = upd2 starts =# extended;

var cnct = (upd3) ++ upd2;
var inter = upd2 /\ initial;

show cnct ?> 0;

show edges >> inter;

var res = (x -> (vertices >> x) ?> 2) ?=> {cnct, upd1, upd2};
"""

exampleShorted = """
var initial = import "TestGraph";

var upd1 = initial starts =+ {1..15};
var inter = upd1 /\ initial;

show edges >> inter;
var res = (x -> (vertices >> x) ?> 2) ?=> {initial, upd1, inter};
"""
