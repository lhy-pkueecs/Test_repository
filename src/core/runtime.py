"""
This module provides some utility functions and classes
to manage the shell engine's runtime.
"""

import core.app_factory as app_factory
from core.builtinapp_executor import BuiltinAppExecutor
import sys


class Context:
    """
    Context class to manage the state of the execution environment.
    """
    def __init__(self, root_context=None):
        self._context = dict()
        self._root_context = root_context if root_context is not None else self

    def set(self, key: str, value):
        """
        Set a value in the context.
        """
        self._context[key] = value

    def get(self, key: str):
        """
        Get a value from the context.
        """
        return self._context.get(key, None)

    def copy(self):
        """
        Create a copy of the context.
        """
        # create a new context with the same root context
        new_context = Context(self._root_context)
        new_context._context = self._context.copy()
        return new_context

    def get_root_context_copy(self):
        """
        Get a copy of the root context.
        """
        return self._root_context.copy()


class IOContextManager:
    """
    Context manager to manage the input and output streams.
    It will automatically recover the streams when exiting the context.
    """
    def __init__(self, input_stream=None, output_stream=None):
        if input_stream is not None:
            self.input_stream = input_stream
        else:
            self.input_stream = sys.stdin
        if output_stream is not None:
            self.output_stream = output_stream
        else:
            self.output_stream = sys.stdout
        self.original_input = sys.stdin
        self.original_output = sys.stdout

    def __enter__(self):
        sys.stdin = self.input_stream
        sys.stdout = self.output_stream
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdin = self.original_input
        sys.stdout = self.original_output


def execute_app(app: str, args: list, context: Context):
    """
    Execute the application with the given arguments and context.
    This function checks if the application is a builtin app or a regular app.
    If it's a builtin app, it uses the BuiltinAppExecutor to execute it.
    If it's a regular app, it uses the app factory to create and execute it.
    """
    if BuiltinAppExecutor.check_builtin_app(app):
        app_instance = BuiltinAppExecutor(context.get("self_engine"))
        with IOContextManager(context.get("input_stream"),
                              context.get("output_stream")):
            app_instance.execute_builtin_app(app, args)
    else:
        app_instance = app_factory.create_app(app)
        with IOContextManager(context.get("input_stream"),
                              context.get("output_stream")):
            app_instance.exec(args)
