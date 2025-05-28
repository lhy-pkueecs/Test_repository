"""
This module defines the BuiltinAppExecutor class, which is responsible
for executing builtin applications in a shell engine context.
"""

from core.error_handling import (AppRuntimeError, AppValueError,
                                 raise_error_handler, print_error_handler)


class BuiltinAppExecutor:
    """
    This class is responsible for executing builtin applications.
    Implicitly requires the shell engine to have methods for changing
    directories, getting the current working directory, and setting
    and unsetting variables.
    """
    builtin_commands = {
            "cd": None,
            "pwd": None,
            "set": None,
            "unset": None
        }

    def __init__(self, engine):
        """
        Initialize the BuiltinAppExecutor with the given shell engine.
        """
        self.shell_engine = engine
        # Map app names to their corresponding methods
        self.builtin_commands = {
            "cd": self._cd,
            "pwd": self._pwd,
            "set": self._set,
            "unset": self._unset
        }

    def execute_builtin_app(self, app_name: str, args: list):
        """
        Execute the builtin application with the given name and arguments.
        """
        error_handler = raise_error_handler
        if app_name.startswith("_"):
            error_handler = print_error_handler
            app_name = app_name[1:]
        if app_name in self.builtin_commands:
            command_method = self.builtin_commands[app_name]
            try:
                # Execute the command method with the provided arguments
                command_method(args)
            except ValueError as e:
                error_handler.handle_error(AppValueError(e, app_name))
            except Exception as e:
                # Catch other potential exceptions during command execution
                error_handler.handle_error(AppRuntimeError(e, app_name))
        else:
            # If the command name is not found in our map
            raise ValueError(f"unsupported application {app_name}")

    @classmethod
    def check_builtin_app(cls, app_name: str) -> bool:
        """
        Check if the given app name is a builtin application.
        """
        if app_name.startswith("_"):
            app_name = app_name[1:]
        return app_name in cls.builtin_commands

    @classmethod
    def get_builtin_apps(cls):
        """
        Get a list of available builtin applications.
        """
        original_apps = list(cls.builtin_commands.keys())
        unsafe_apps = ["_" + name for name in original_apps]
        return original_apps + unsafe_apps
    """
    Builtin application methods.
    """
    def _cd(self, args: list):
        """
        Change the current working directory.
        """
        if len(args) != 1:
            raise ValueError("cd command requires exactly one argument")
        path = args[0]
        self.shell_engine._change_directory(path)

    def _pwd(self, args: list):
        """
        Get the current working directory.
        """
        print(self.shell_engine._get_pwd())

    def _set(self, args: list):
        """
        Set a variable in the context.
        """
        if len(args) != 2:
            raise ValueError("set command requires exactly two arguments")
        var_name = args[0]
        value = args[1]
        self.shell_engine._set_var(var_name, value)

    def _unset(self, args: list):
        """
        Unset a variable in the context.
        """
        if len(args) != 1:
            raise ValueError("unset command requires exactly one argument")
        var_name = args[0]
        self.shell_engine._unset_var(var_name)
