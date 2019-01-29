from bcca.test import expect, check_expectations


class TestCanCheckReturnValueExpectations:
    @staticmethod
    def test_can_check_zero_expectations():
        def add(x, y):
            return x + y

        assert check_expectations(add) == []

    @staticmethod
    def test_can_pass_one_expectations():
        @expect(x=3, y=4, to_return=7)
        def add(x, y):
            return x + y

        assert check_expectations(add) == [{'result': 'pass'}]

    @staticmethod
    def test_can_fail_one_expectations():
        @expect(x=3, y=4, to_return=8)
        def add(x, y):
            return x + y

        assert check_expectations(add) == [{
            'result': 'fail',
            'actual': 7,
            'expected': 8
        }]

    @staticmethod
    def test_can_check_two_expectations():
        @expect(x=2, y=2, to_return=4)
        @expect(x=3, y=4, to_return=7)
        def add(x, y):
            return x + y

        assert check_expectations(add) == [{
            'result': 'pass'
        }, {
            'result': 'pass'
        }]

    @staticmethod
    def test_expectations_maintain_order():
        @expect(x=2, y=2, to_return=5)
        @expect(x=3, y=4, to_return=7)
        def add(x, y):
            return x + y

        results = check_expectations(add)
        assert results[0]['result'] == 'fail'
        assert results[1]['result'] == 'pass'