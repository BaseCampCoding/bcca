from bcca.test import expect, passes_expectations
import pytest


def test_expect_add_2_plus_2_to_return_4_passes():
    @expect(x=2, y=2, to_return=4)
    def add(x, y):
        return x + y

    assert passes_expectations(add)


def test_expect_add_can_fail():
    @expect(x=2, y=2, to_return=5)
    def add(x, y):
        return x + y

    assert not passes_expectations(add)


def test_expect_greet_to_print_greeting():
    @expect(name="nate", to_print="hello nate")
    def greet(name):
        print("hello", name)

    assert passes_expectations(greet)


def test_expect_greet_can_fail():
    @expect(name="evil nate", to_print="hello nate")
    def greet(name):
        print("hello", name)

    assert not passes_expectations(greet)


def test_printing_multiline():
    @expect(
        to_print="""hello
world"""
    )
    def hello_world():
        print("hello")
        print("world")

    assert passes_expectations(hello_world)


def test_expectation_can_assume_inputs():
    @expect(with_inputs=["nate", "clark"], to_return="nate clark")
    def test_inputs():
        return input() + " " + input()

    assert passes_expectations(test_inputs)


def test_expectations_can_assume_inputs_and_expect_output():
    @expect(
        with_inputs=["Nate"],
        to_print="""
What is your name? Nate
Hello, Nate
""",
    )
    def test_both():
        name = input("What is your name? ")
        print("Hello,", name)

    assert passes_expectations(test_both)


def test_expectations_can_stub_out_a_file():
    @expect(with_fake_files={"foo.txt": "hello world"}, to_return="hello world")
    def test_simple_read():
        return open("foo.txt").read()

    assert passes_expectations(test_simple_read)


def test_can_have_multiple_expectations():
    @expect(x=7, y=3, to_return=10)
    @expect(x=-1, y=3, to_return=2)
    def add(x, y):
        return x + y

    assert passes_expectations(add)
