from bcca.test import should_print, with_inputs, fake_file
import pytest


@should_print
def test_printing_once(output):
    print("hello")
    assert output == "hello"


@should_print
def test_printing_multiline(output):
    print("hello")
    print("world")
    assert (
        output
        == """
hello
world
"""
    )


@with_inputs("nate", "clark")
def test_inputs():
    assert input() == "nate"
    assert input() == "clark"


@should_print
@with_inputs("Nate")
def test_both(output):
    name = input("What is your name? ")
    print("Hello,", name)
    assert (
        output
        == """
What is your name? Nate
Hello, Nate
"""
    )


@fake_file({"foo.txt": "hello world"})
def test_simple_read():
    assert open("foo.txt").read() == "hello world"


@fake_file({"foo.txt": "hello world"})
def test_open_other_file_errors():
    with pytest.raises(FileNotFoundError):
        assert open("bar.txt")


@fake_file({"foo.txt": "hello world", "bar.txt": "game over"})
def test_two_files():
    assert open("foo.txt").read() == "hello world"

    assert open("bar.txt").read() == "game over"


@fake_file({"foo.txt": "hello\nworld"})
def test_readline_works():
    assert open("foo.txt").readlines() == ["hello\n", "world"]


@fake_file({"foo.txt": "hello world"})
def test_write_mode_works():
    open("foo.txt", "w").write("game over")

    assert open("foo.txt").read() == "game over"


@fake_file({"foo.txt": "hello world"})
def test_append_mode_works():
    open("foo.txt", "a").write("game over")

    assert open("foo.txt").read() == "hello worldgame over"


@fake_file({"foo.txt": "hello world"})
def test_with_statement_read_works():
    with open("foo.txt") as f:
        assert f.read() == "hello world"


@fake_file({"foo.txt": "hello world"})
def test_with_statement_write_works():
    with open("foo.txt", "w") as f:
        f.write("game over")

    assert open("foo.txt").read() == "game over"

