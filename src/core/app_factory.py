"""
This module handles the registration, creation, and discovery of applications.

It provides mechanisms to register new application types,
instantiate applications by name,
and retrieve a list of all available applications.
"""

from core.app import App
from typing import Dict, Type
from .error_handling import print_error_handler


_app_registry: Dict[str, Type[App]] = {}


def register(name: str):
    def decorator(cls: Type[App]):
        _app_registry[name] = cls
        return cls
    return decorator


def create_app(name: str) -> App:
    """
    Create an application instance by name.
    """
    try:
        if name.startswith('_'):
            name = name[1:]
            app = _app_registry[name](name, print_error_handler)
        else:
            app = _app_registry[name](name)
        return app
    except KeyError:
        raise ValueError(f"unsupported application {name}")


def get_available_apps() -> list:
    """
    Get a list of available applications.
    """
    original_apps = list(_app_registry.keys())
    unsafe_apps = ["_" + name for name in original_apps]
    return original_apps + unsafe_apps
