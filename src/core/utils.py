"""
This module provides some utility classes and functions.
"""


class IOFileManager:
    """
    A sugar class for managing input and output file streams together.
    It will automatically close the streams when exiting the context.
    """
    def __init__(self, in_file: str = None, out_file: str = None,
                 outfile_mode: str = 'w'):
        self.in_file = in_file
        self.out_file = out_file
        self.outfile_mode = outfile_mode
        self.input_stream = None
        self.output_stream = None

    def __enter__(self):
        if self.in_file:
            try:
                self.input_stream = open(self.in_file, 'r')
            except FileNotFoundError:
                raise ValueError(f"Input file {self.in_file} not found.")

        if self.out_file:
            try:
                self.output_stream = open(self.out_file, self.outfile_mode)
            except FileNotFoundError:
                raise ValueError(f"Output file {self.out_file} not found.")

        return self.input_stream, self.output_stream

    def __exit__(self, exc_type, exc_value, traceback):
        if self.input_stream:
            self.input_stream.close()

        if self.output_stream:
            self.output_stream.close()


class char_with_info:
    """
    A class to store a character and its quote information.
    """
    def __init__(self, char: str, is_quoted: bool):
        self.char = char
        self.is_quoted = is_quoted


class char_with_info_list:
    """
    A class to store a list of characters with their quote information.
    """
    def __init__(self, string: str, is_quoted: bool):
        self.char_list = []
        for char in string:
            self.char_list.append(char_with_info(char, is_quoted))

    def get_glob_mask(self):
        result = ""
        for char in self.char_list:
            if char.is_quoted and char.char == "*":
                result += "[*]"
            else:
                result += char.char
        return result

    def __str__(self):
        return "".join([char.char for char in self.char_list])

    def __len__(self):
        return len(self.char_list)

    def __getitem__(self, index: int):
        return self.char_list[index]

    def __setitem__(self, index: int, value):
        self.char_list[index] = value

    def __iadd__(self, other):
        self.char_list += other.char_list
        return self
