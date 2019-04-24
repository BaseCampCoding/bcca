from bcca.test import expect, passes_expectations


def test_opening_a_nonexistent_file_in_read_mode_errors():
    @expect(with_fake_files={"foo.txt": "hello world"}, to_raise=FileNotFoundError)
    def open_other_file_errors():
        open("bar.txt")

    assert passes_expectations(open_other_file_errors)
