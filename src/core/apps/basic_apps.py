"""
This module defines applications below:
echo, ls, cat, head, tail, grep
which are concrete implementations of the App class.
"""

import os
import re
from core.app import App
from core.app_factory import register
import sys


@register("echo")
class Echo(App):
    def _run(self, args):
        out = (" ".join(args))
        print(out)


@register("ls")
class Ls(App):
    def _run(self, args):
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ValueError("wrong number of arguments")
        else:
            ls_dir = args[0]
        for f in os.listdir(ls_dir):
            if not f.startswith("."):
                print(f)


@register("cat")
class Cat(App):
    def _run(self, args):
        if len(args) == 0:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            else:
                for line in sys.stdin:
                    print(line, end="")
        else:
            for a in args:
                with open(a, "r") as f:
                    print(f.read(), end="")


@register("head")
class Head(App):
    def _run(self, args):
        if len(args) > 3:
            raise ValueError("wrong number of arguments")
        is_stdin = False
        if len(args) == 0:
            num_lines = 10
            is_stdin = True
        elif len(args) == 1:
            # must be head [FILE]
            num_lines = 10
            file = args[0]
        elif len(args) == 2:
            # must be head [OPTIONS]
            if args[0] != "-n":
                raise ValueError("Unknown option: " + args[0])
            num_lines = int(args[1])
            is_stdin = True
        else:
            # must be head [OPTIONS] [FILE]
            if args[0] != "-n":
                raise ValueError("Unknown option: " + args[0])
            num_lines = int(args[1])
            file = args[2]
        if is_stdin:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            lines = sys.stdin.readlines()
            for i in range(0, min(len(lines), num_lines)):
                print(lines[i], end="")
        else:
            with open(file, "r") as f:
                lines = f.readlines()
                for i in range(0, min(len(lines), num_lines)):
                    print(lines[i], end="")


@register("tail")
class Tail(App):
    def _run(self, args):
        if len(args) > 3:
            raise ValueError("wrong number of arguments")
        is_stdin = False
        if len(args) == 0:
            num_lines = 10
            is_stdin = True
        elif len(args) == 1:
            # must be tail [FILE]
            num_lines = 10
            file = args[0]
        elif len(args) == 2:
            # must be tail [OPTIONS]
            if args[0] != "-n":
                raise ValueError("Unknown option: " + args[0])
            num_lines = int(args[1])
            is_stdin = True
        else:
            # must be tail [OPTIONS] [FILE]
            if args[0] != "-n":
                raise ValueError("Unknown option: " + args[0])
            num_lines = int(args[1])
            file = args[2]
        if is_stdin:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            lines = sys.stdin.readlines()
            display_length = min(len(lines), num_lines)
            for i in range(0, display_length):
                print(lines[len(lines) - display_length + i], end="")
        else:
            with open(file, "r") as f:
                lines = f.readlines()
                display_length = min(len(lines), num_lines)
                for i in range(0, display_length):
                    print(lines[len(lines) - display_length + i], end="")


@register("grep")
class Grep(App):
    def _run(self, args):
        if len(args) < 1:
            raise ValueError("wrong number of arguments")
        if len(args) == 1:
            if sys.stdin.isatty():
                raise ValueError("empty input")
            pattern = args[0]
            for line in sys.stdin:
                if re.match(pattern, line):
                    print(line, end="")
        else:
            pattern = args[0]
            files = args[1:]
            for file in files:
                with open(file, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        if re.match(pattern, line):
                            if len(files) > 1:
                                print(f"{file}:{line}", end="")
                            else:
                                print(line, end="")
