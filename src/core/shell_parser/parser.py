"""
This module is used to parse the command line input using Lark
parser, and return the abstract syntax tree (AST) of the command.
"""

from lark import Lark, Transformer, LarkError
from core.error_handling import ParseError
import os


with open(os.path.join(os.path.dirname(__file__), "grammar.lark"), "r",
          encoding="utf-8") as f:
    grammar = f.read()


class CommandTransformer(Transformer):
    def seq(self, items):
        return {"type": "seq", "commands": items}

    def pipe(self, items):
        return {"type": "pipe", "commands": items}

    def call(self, items):
        return {"type": "call", "arguments_or_redirect": items}

    def redirection(self, items):
        return {"type": "redirection",
                "redirect_symbol": items[0].value, "file_argument": items[1]}

    def argument(self, items):
        return {"type": "argument", "values": items}

    def double_quoted(self, items):
        return {"type": "double_quoted", "values": items}

    def backquoted(self, items):
        return {"type": "backquoted", "value": items[0]}

    def non_keyword(self, items):
        return {"type": "non_keyword", "value": items[0].value}

    def single_quoted(self, items):
        return {"type": "single_quoted", "value": items[0].value[1:-1]}

    def doublequote_content(self, items):
        return {"type": "non_keyword", "value": items[0].value}

    def backquote_content(self, items):
        return {"type": "non_keyword", "value": items[0].value}

    def variable(self, items):
        return {"type": "variable", "value": items[0].value[1:]}


parser = Lark(grammar, parser="earley")
transformer = CommandTransformer()


def parse_command(command: str) -> dict:
    """
    Parse the command using Lark parser.
    Returns the abstract syntax tree (AST) of the command.
    Raises ParseError if the command is invalid.
    """
    try:
        return transformer.transform(parser.parse(command))
    except LarkError as e:
        raise ParseError(e)
