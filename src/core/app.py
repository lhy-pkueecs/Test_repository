from abc import ABC, abstractmethod
from core.error_handling import (ErrorHandler, raise_error_handler,
                                 AppRuntimeError, AppValueError)


class App(ABC):
    """
    Abstract base class for all applications.
    The run method should be implemented by subclasses.
    """
    def __init__(self, name,
                 error_handler: ErrorHandler = raise_error_handler):
        """
        Initialize the application with a name and an error handler.
        """
        self._name = name
        self._error_handler = error_handler

    @abstractmethod
    def _run(self, args):
        pass

    def exec(self, args):
        """
        Executes the application's main logic with the given arguments.

        This method wraps the _run method with app providing error handling.
        ValueErrors are caught and wrapped in AppValueError.
        Other exceptions are caught and wrapped in AppRuntimeError.
        The configured error_handler is then used to
        handle these application-specific errors.
        """
        try:
            self._run(args)
        except ValueError as e:
            app_value_error = AppValueError(e, self._name)
            self._error_handler.handle_error(app_value_error)
        except Exception as e:
            app_runtime_error = AppRuntimeError(e, self._name)
            self._error_handler.handle_error(app_runtime_error)
