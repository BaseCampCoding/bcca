from bcca.test import expect, passes_expectations


def test_opening_a_nonexistent_file_in_read_mode_errors():
    @expect(with_fake_files={"foo.txt": "hello world"}, to_raise=FileNotFoundError)
    def open_other_file_errors():
        open("bar.txt")

    assert passes_expectations(open_other_file_errors)


def test_opening_two_files():
    @expect(
        with_fake_files={"foo.txt": "hello world", "bar.txt": "game over"},
        to_return="hello worldgame over",
    )
    def two_files():
        return open("foo.txt").read() + open("bar.txt").read()


def test_file_readlines():
    @expect(with_fake_files={"foo.txt": "hello\nworld"}, to_return=["hello\n", "world"])
    def test_readline_works():
        return open("foo.txt").readlines()
