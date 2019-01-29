from bcca.test import expect


class TestFunctionsCanHaveMultipleExpectations:
    @staticmethod
    def test_can_have_one_expectations():
        @expect(x=2, y=2, to_return=4)
        def add(x, y):
            return x + y

        assert len(add.expectations) == 1

    @staticmethod
    def test_can_have_two_expectations():
        @expect(x=2, y=2, to_return=4)
        @expect(x=3, y=4, to_return=7)
        def add(x, y):
            return x + y

        assert len(add.expectations) == 2

    # @staticmethod
    # def test_expectations_maintain_order():
    #     @expect(x=2, y=2, to_return=4)
    #     @expect(x=3, y=4, to_return=7)
    #     def add(x, y):
    #         return x + y

    #     assert add.expectations[0]['to_return'] == 4
    #     assert add.expectations[1]['to_return'] == 7
