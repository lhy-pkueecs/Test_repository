"""
This module defines the eval tree for evaluating abstract syntax trees (ASTs).
And it contains the necessary classes and functions for the eval tree.
It provides an abstract base class for eval nodes
and a factory function to create eval nodes based on their type name.
"""

from abc import ABC, abstractmethod
from typing import Dict, Type
from core.runtime import Context


class EvalNode(ABC):
    """
    Abstract base class for all eval nodes.
    The run method should be implemented by subclasses.
    """
    @abstractmethod
    def __init__(self, ast: dict):
        pass

    @abstractmethod
    def eval(self, context: Context):
        pass


_eval_node_registry: Dict[str, Type[EvalNode]] = {}


def register(name: str):
    def decorator(cls: Type[EvalNode]):
        _eval_node_registry[name] = cls
        return cls
    return decorator


def create_eval_node(name: str, ast: dict) -> EvalNode:
    """
    Create an eval node instance by name.
    """
    try:
        eval_node = _eval_node_registry[name](ast)
        return eval_node
    except KeyError:
        raise ValueError(f"unsupported eval node {name}")


class EvalTree:
    """
    Represents a tree of eval nodes. Which is used to evaluate the command.
    """
    def __init__(self, ast: dict):
        """
        Initialize the eval tree with an AST (abstract syntax tree).
        The AST is a dictionary representation of the tree.
        """
        self.root = create_eval_node(ast["type"], ast)

    def eval(self, context: Context = None):
        """
        Evaluate the tree.
        Directly raise exception during the evaluation.
        """
        self.root.eval(context)
