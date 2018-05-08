from bcca.test import should_print, with_inputs

@should_print
def test_printing_once(output):
    print('hello')
    assert output == 'hello'


@should_print
def test_printing_multiline(output):
    print('hello')
    print('world')
    assert output == '''
hello
world
'''


@with_inputs('nate', 'clark')
def test_inputs():
    assert input() == 'nate'
    assert input() == 'clark'

@should_print
@with_inputs('Nate')
def test_both(output):
    name = input('What is your name? ')
    print('Hello,', name)
    assert output == '''
What is your name? Nate
Hello, Nate
'''
