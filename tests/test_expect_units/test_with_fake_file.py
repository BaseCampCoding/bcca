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

    assert passes_expectations(two_files)


def test_file_readlines():
    @expect(with_fake_files={"foo.txt": "hello\nworld"}, to_return=["hello\n", "world"])
    def test_readline_works():
        return open("foo.txt").readlines()

    assert passes_expectations(test_readline_works)


def test_can_write_to_existing_fake_file():
    @expect(with_fake_files={"foo.txt": "hello world"}, to_return="game over")
    def test_write_mode_works():
        open("foo.txt", "w").write("game over")
        return open("foo.txt").read()

    assert passes_expectations(test_write_mode_works)


def test_can_append_to_fake_file():
    @expect(
        with_fake_files={"foo.txt": "hello world"}, to_return="hello worldgame over"
    )
    def test_append_mode_works():
        open("foo.txt", "a").write("game over")
        return open("foo.txt").read()

    assert passes_expectations(test_append_mode_works)


def test_context_manager_works_on_fake_file():
    @expect(with_fake_files={"foo.txt": "hello world"}, to_return="hello world")
    def test_with_statement_read_works():
        with open("foo.txt") as f:
            return f.read()

    assert passes_expectations(test_with_statement_read_works)


def test_context_manager_works_for_writing_fake_file():
    @expect(with_fake_files={"foo.txt": "hello world"}, to_return="game over")
    def test_with_statement_write_works():
        with open("foo.txt", "w") as f:
            f.write("game over")
        return open("foo.txt").read()

    assert passes_expectations(test_with_statement_write_works)
