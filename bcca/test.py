from unittest import mock
from bcca.pytest_plugin import FakeStringIO, FakeStdIn

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
    print(inputs)
    def _inner(test_function):
        def test_ignoring_input(input, *args, **kwargs):
            return test_function(*args, **kwargs)
        return mock.patch('sys.stdin', new_callable=lambda: FakeStdIn(inputs))(test_ignoring_input)
    return _inner
