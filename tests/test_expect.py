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
    @expect(name='nate', to_print='hello nate')
    def greet(name):
        print('hello', name)

    assert passes_expectations(greet)


def test_expect_greet_can_fail():
    @expect(name='evil nate', to_print='hello nate')
    def greet(name):
        print('hello', name)

    assert not passes_expectations(greet)


def test_printing_multiline():
    @expect(to_print='''hello
world''')
    def hello_world():
        print('hello')
        print('world')

    assert passes_expectations(hello_world)


# TODO: Convert these tests into @expect tests

# @with_inputs('nate', 'clark')
# def test_inputs():
#     assert input() == 'nate'
#     assert input() == 'clark'

# @should_print
# @with_inputs('Nate')
# def test_both(output):
#     name = input('What is your name? ')
#     print('Hello,', name)
#     assert output == '''
# What is your name? Nate
# Hello, Nate
# '''

# @fake_file({'foo.txt': 'hello world'})
# def test_simple_read():
#     assert open('foo.txt').read() == 'hello world'

# @fake_file({'foo.txt': 'hello world'})
# def test_open_other_file_errors():
#     with pytest.raises(ValueError):
#         assert open('bar.txt')

# @fake_file({'foo.txt': 'hello world', 'bar.txt': 'game over'})
# def test_two_files():
#     assert open('foo.txt').read() == 'hello world'

#     assert open('bar.txt').read() == 'game over'

# @fake_file({'foo.txt': 'hello\nworld'})
# def test_readline_works():
#     assert open("foo.txt").readlines() == ['hello\n', 'world']

# @fake_file({'foo.txt': 'hello world'})
# def test_write_mode_works():
#     open('foo.txt', 'w').write('game over')

#     assert open('foo.txt').read() == 'game over'

# @fake_file({'foo.txt': 'hello world'})
# def test_append_mode_works():
#     open('foo.txt', 'a').write('game over')

#     assert open('foo.txt').read() == 'hello worldgame over'

# @fake_file({'foo.txt': 'hello world'})
# def test_with_statement_read_works():
#     with open('foo.txt') as f:
#         assert f.read() == 'hello world'

# @fake_file({'foo.txt': 'hello world'})
# def test_with_statement_write_works():
#     with open('foo.txt', 'w') as f:
#         f.write('game over')

#     assert open('foo.txt').read() == 'game over'