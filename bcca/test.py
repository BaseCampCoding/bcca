from unittest import mock
from bcca.pytest_plugin import FakeStringIO, FakeStdIn, fake_open
from inspect import signature


def should_print(test_function):
    '''should_print is a helper for testing code that uses print

    For example, if you had a function like this:

    ```python
    def hello(name):
        print('Hello,', name)
    ```

    You might want to test that it prints "Hello, Nate" if you give it the
    name "Nate". To do that, you could write the following test.

    ```python
    @should_print
    def test_hello_nate(output):
        hello("Nate")

        assert output == "Hello, Nate"
    ```

    There are a couple pieces of this:
        - Put `@should_print` directly above the test function.
        - Add an `output` parameter to the test function.
        - Assert against `output`
    '''
    return mock.patch('sys.stdout', new_callable=FakeStringIO)(test_function)


def with_inputs(*inputs):
    '''with_inputs accepts strings to be used as user input

    For example, if you had a function like this:

    ```python
    def get_age():
        age_string = input('What is your age? ')
        return int(age_string)
    ```

    You might want to test that it returns 27 if you give it
    "27" as user input. To do that, you could write the following test.

    ```python
    @with_inputs('27')
    def test_get_age():
        assert get_age() == 27
    ```

    There are a couple pieces to this:
        - Put `@with_inputs` directly above your test function.
        - Provide `@with_inputs(...)` with the strings you want
          to substitute for the user input.
    '''

    def _inner(test_function):
        def test_ignoring_input(input, *args, **kwargs):
            return test_function(*args, **kwargs)

        return mock.patch(
            'sys.stdin',
            new_callable=lambda: FakeStdIn(inputs))(test_ignoring_input)

    return _inner


def fake_file(file_contents):
    '''fake_file can be used to test simple interactions with the file system.

    It will intercept calls to `open`, and substitute file system behavior
    based on `file_contents`.

    For example, if you wanted to test some code that reads from a file:

    ```python
    def simple_read():
        with open('my_file.txt') as f:
           return f.read()
    ```

    You could write a test like this:

    ```python
    @fake_file({'my_file.txt': 'hello world'})
    def test_simple_read():
        assert simple_read() == 'hello world'
    ```

    If you wanted to write to a file, the code looks just like you would expect:

    ```python
    @fake_file({'my_file.txt': 'hello world'})
    def test_writing():
        with open('my_file.txt', 'w') as f:
            f.write('good bye')

        assert open('my_file.txt').read() == 'good bye'
    '''

    def _inner(test_function):
        @mock.patch(
            'builtins.open', new_callable=lambda: fake_open(file_contents))
        def test_it(fake_open, *args, **kwargs):
            return test_function(*args, **kwargs)

        return test_it

    return _inner


def expect(**expectation_args):
    def test_wrapper(function_under_test):
        if hasattr(function_under_test, 'expectations'):
            function_under_test.expectations.insert(0, expectation_args)
        else:
            function_under_test.expectations = [expectation_args]

        return function_under_test

    return test_wrapper


def check_expectations(function):
    return [
        check_expectation(function, expectation)
        for expectation in getattr(function, 'expectations', [])
    ]


def check_expectation(function, expectation_args):
    if 'with_inputs' in expectation_args:
        patched_stdin = mock.patch(
            'sys.stdin',
            new_callable=lambda: FakeStdIn(expectation_args['with_inputs']))
        patched_stdin.start()

    if 'to_return' in expectation_args:
        return check_function_returns_correctly(function, expectation_args)
    elif 'to_print' in expectation_args:
        return check_function_prints_correctly(function, expectation_args)
    else:
        raise ValueError(
            f'Expectation didn\'t assert expect anything:\n{expectation_args}')

    if 'with_inputs' in expectation_args:
        patched_stdin.stop()


def check_function_returns_correctly(function, expectation_args):
    actual = function(**args_for(function, expectation_args))
    if actual == expectation_args['to_return']:
        return {'result': 'pass'}
    else:
        return {
            'result': 'fail',
            'expected': expectation_args['to_return'],
            'actual': actual
        }


def check_function_prints_correctly(function, expectation_args):
    with mock.patch('sys.stdout', new_callable=FakeStringIO) as fake_stdout:
        function(**args_for(function, expectation_args))

    if fake_stdout == expectation_args['to_print']:
        return {'result': 'pass'}
    else:
        return {
            'result': 'fail',
            'expected': expectation_args['to_print'],
            'actual': fake_stdout
        }


def args_for(function, expectation_args):
    return {
        param: expectation_args[param]
        for param in signature(function).parameters
    }


def passes_expectations(function):
    return all(expectation['result'] == 'pass'
               for expectation in check_expectations(function))
