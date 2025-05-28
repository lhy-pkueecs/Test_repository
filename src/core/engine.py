from core.eval_tree import EvalTree
from core.runtime import Context
from core.shell_parser.parser import parse_command
from core.error_handling import engine_error_handler
import os


class ShellEngine:
    """
    Shell engine to evaluate commands, which have a runtime context.
    """
    def __init__(self, **kwargs):
        """
        Initialize the shell engine with the given context.
        The context includes variables, IO streams,
        exit flag, and the shell engine itself.
        the exit flag is used to determine if the engine should exit
        when an recoverable error occurs.
        """
        self.__context = Context()
        for key, value in kwargs.items():
            self.__context.set(key, value)
        self.__context.set("self_engine", self)
        self.__exit_flag = kwargs.get("exit_flag", True)

    def _eval_command(self, command: str):
        """
        Evaluate the command.
        """
        try:
            parsed_tree = parse_command(command)
            eval_tree = EvalTree(parsed_tree)
            eval_tree.eval(self.__context)
        except Exception as e:
            engine_error_handler(e, self.__exit_flag)
    """
    Some methods to manage the state of the engine.
    """
    def _change_directory(self, path: str):
        """
        Change the current working directory.
        """
        os.chdir(path)

    def _get_pwd(self):
        """
        Get the current working directory.
        """
        return os.getcwd()

    def _set_var(self, var_name: str, value: str):
        """
        Set a variable in the context.
        """
        self.__context.set(var_name, value)

    def _unset_var(self, var_name: str):
        """
        Unset a variable in the context.
        """
        self.__context.set(var_name, None)

    def _get_var(self, var_name: str):
        """
        Get a variable from the context.
        """
        return self.__context.get(var_name)
