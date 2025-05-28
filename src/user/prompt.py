"""
This module provides the command line user interface for the shell.
"""

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.filters import Condition
from prompt_toolkit.application import get_app
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer
import os
import core.api


class CommandCompleter(Completer):
    """
    A custom completer for command line interface.
    This class provides command and file path completion for a given engine.
    """
    def __init__(self, engine):
        self.engine = engine
        self.commands = core.api.get_available_commands()

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor
        word_before_cursor = document.get_word_before_cursor(WORD=True)

        # Try to complete commands first
        # if no space, we are completing command
        if ' ' not in text_before_cursor:
            for cmd in self.commands:
                if cmd.startswith(word_before_cursor):
                    yield Completion(cmd,
                                     start_position=-len(word_before_cursor))
        else:
            # If there is a space, we are completing file paths
            current_dir = core.api.get_pwd(self.engine)
            path_prefix = word_before_cursor
            base_dir = current_dir

            if '/' in path_prefix or '\\' in path_prefix:
                # if path_prefix contains a separator, split it to get
                # the base directory and the prefix
                base_dir = os.path.dirname(os.path.join(current_dir,
                                                        path_prefix))
                path_prefix = os.path.basename(path_prefix)
            try:
                if os.path.isdir(base_dir):
                    for filename in os.listdir(base_dir):
                        full_path = os.path.join(base_dir, filename)
                        # check if the filename starts with the path prefix
                        if filename.startswith(path_prefix):
                            completion_text = filename
                            # if the full path is a directory, add a separator
                            if os.path.isdir(full_path):
                                completion_text += os.sep
                            yield Completion(completion_text,
                                             start_position=-len(path_prefix))
            except OSError:
                pass


def check_command_quote_complete(command: str) -> bool:
    """
    Check if the command has a complete quote.
    """
    quote = ''
    for c in command:
        if c == '"' or c == "'" or c == '`':
            if quote == '':
                quote = c
            elif quote == c:
                quote = ''
    return quote == ''


def is_multiline():
    """
    Check if the current input is multiline for unfinished quote.
    """
    current_text = get_app().current_buffer.text
    return not check_command_quote_complete(current_text)


def create_prompt(engine):
    """
    Create a prompt with custom completer and history.
    """
    input_str = prompt(
        f"{core.api.get_pwd(engine)}> ",
        # use custom completer
        completer=CommandCompleter(engine),
        # multiline input for unfinished quote
        multiline=Condition(is_multiline),
        # continuation prompt for multiline input
        prompt_continuation="quote> ",
        lexer=PygmentsLexer(BashLexer)
    )
    # replace newlines with empty string
    input_str = input_str.replace("\n", "")
    return input_str
