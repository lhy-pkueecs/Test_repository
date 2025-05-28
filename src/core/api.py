"""
This module provides the public API for interacting with the shell engine.

It includes functions for creating a shell engine instance,
evaluating commands, retrieving available commands,
and getting the current working directory.
"""

from core.engine import ShellEngine
from core.app_factory import get_available_apps as _get_available_apps
from core.builtinapp_executor import BuiltinAppExecutor as _BuiltinAppExecutor


def create_shell_engine(**kwargs) -> ShellEngine:
    """
    Create a shell engine instance.
    Args:
        **kwargs: Initial context to pass to the ShellEngine.
    """
    return ShellEngine(**kwargs)


def eval_command(engine: ShellEngine, command: str) -> None:
    """Evaluate a command using the shell engine.

    Args:
        engine: The ShellEngine instance to use for evaluating the command.
        command: The command string to evaluate.
    """
    engine._eval_command(command)


def get_available_commands() -> list:
    """Get a list of available commands.

    Returns:
        A list of available command names.
    """
    return _get_available_apps() + _BuiltinAppExecutor.get_builtin_apps()


def get_pwd(engine: ShellEngine) -> str:
    """Get the current working directory from the engine.

    Args:
        engine: The ShellEngine instance.

    Returns:
        A string representing the current working directory.
    """
    return engine._get_pwd()
