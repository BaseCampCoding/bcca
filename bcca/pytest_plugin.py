from _pytest.assertion.util import assertrepr_compare
from io import StringIO, FileIO
import sys
from unittest import mock


def fake_open(file_contents):
    def _f(file, mode='r'):
        if file in file_contents:
            return StringIO(file_contents[file])
        else:
            raise ValueError(f'You tried to open {file}, but you didn\'t fake it out!')

    return _f


class FakeStringIO(StringIO):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.getvalue().strip() == other.strip()
        else:
            return super().__eq__(other)

    def __repr__(self):
        return repr(self.getvalue().strip())


class FakeStdIn:
    def __init__(self, responses):
        self.responses = responses
        self.idx = 0

    def readline(self):
        if self.idx >= len(self.responses):
            raise AssertionError('No more input provided!')
        else:
            self.idx += 1
            sys.stdout.write(self.responses[self.idx - 1] + '\n')
            return self.responses[self.idx - 1]


def pytest_assertrepr_compare(config, op, left, right):
    if isinstance(left, FakeStringIO) and isinstance(right, str) and op == '==':
        return assertrepr_compare(
            config,
            op,
            left.getvalue().strip(),
            right.strip(),
        )
