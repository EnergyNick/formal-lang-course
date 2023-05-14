from project.language.lang_parser import (
    is_text_correct_in_language,
    generate_dot_to_str,
)
from textwrap import dedent

from tests.test_lang_parser_constants import (
    exampleFromLang,
    exampleShorted,
    exampleDotFileContent,
)


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
    assert dedent(res) == dedent(exampleDotFileContent)
