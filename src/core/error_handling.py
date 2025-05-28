"""
This module define custom exceptions and error handling strategies.
And provide a method to handle errors from the execution of the engine.
"""

from abc import ABC, abstractmethod


"""
Custom Exceptions
"""


class AppRuntimeError(Exception):
    """
    Custom exception for application runtime errors.
    """
    def __init__(self, e: Exception, app_name: str = "App"):
        self.app_name = app_name
        super().__init__(e)

    def __str__(self):
        return f"{self.app_name}: unexpected error: {super().__str__()}"


class AppValueError(ValueError):
    """
    Custom exception for application value errors.
    """
    def __init__(self, e: ValueError, app_name: str = "App"):
        self.app_name = app_name
        super().__init__(e)

    def __str__(self):
        return f"{self.app_name}: {super().__str__()}"


class ParseError(Exception):
    """
    Custom exception for parsing errors.
    """
    def __init__(self, e: Exception):
        super().__init__(e)

    def __str__(self):
        return f"ParseError: {super().__str__()}"


# exceptions that are recoverable
# which actually occur because of user input errors


recoverable_exceptions = (
    AppRuntimeError,
    AppValueError,
    ParseError,
    ValueError,
)

"""
Error Handlers
"""


class ErrorHandler(ABC):
    """Abstract base class for error handling strategies."""
    @abstractmethod
    def handle_error(exception: Exception):
        """Handles the exception encountered during App execution."""
        pass


class RaiseErrorHandler(ErrorHandler):
    """Error handler strategy that raises an error."""
    def handle_error(self, exception: Exception):
        raise exception


class PrintErrorHandler(ErrorHandler):
    """Error handler strategy that prints the error message."""
    def handle_error(self, exception: Exception):
        print(exception)


# singleton instances of error handlers
print_error_handler = PrintErrorHandler()
raise_error_handler = RaiseErrorHandler()


def engine_error_handler(exception: Exception, exit_flag: bool = True):
    """
    Handles errors encountered during the execution of the engine.
    When exit_flag is True, it raises the exception.
    When exit_flag is False, it prints the error message.
    Unrecoverable exceptions are always raised.
    """
    if exit_flag:
        expected_error_handler = raise_error_handler
    else:
        expected_error_handler = print_error_handler
    if isinstance(exception, recoverable_exceptions):
        # Handle recoverable exceptions
        expected_error_handler.handle_error(exception)
    else:
        # Handle unrecoverable exceptions, always raise
        raise exception
