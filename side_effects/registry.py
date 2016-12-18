# -*- coding: utf-8 -*-
"""
side_effects.registry

This module contains the Registry class that is responsible for managing
all of the registered side-effects.

"""
from collections import defaultdict
import logging
import yaml

logger = logging.getLogger(__name__)


class Registry(object):

    """
    Registry of side effect functions.

    This class is used to manage the side-effects linking. Functions
    that are decorated with @is_side_effect_of are added to the internal
    list of (label, func) tuples, and when the side-effecting function is
    called, all of the relevant matching functions are fired.

    """

    def __init__(self):
        self._funcs = []

    def add(self, label, func):
        """
        Add a function to the registry.

        Args:
            label: string, the name of the side-effect - this is used
                to bind two function - the function that @has_side_effects
                and the function that @is_side_effect.
            func: a function that will be called when the side-effects are
                executed - this will be passed all of the args and kwargs
                of the original function.

        """
        self._funcs.append((label, func))

    def labels(self):
        """Return sorted unique list of labels."""
        return list(set(f[0] for f in self._funcs))

    def functions(self, label):
        """Return list of functions in the registry matching a label."""
        return [f[1] for f in self._funcs if f[0] == label]

    def execute(self, label, *args, **kwargs):
        """
        Execute all the side-effects functions registered to a label.

        The execute function catches and logs all exceptions, but does
        not stop for them.

        # TODO: add in async function calling.

        """
        for func in self.functions(label):
            try:
                func(*args, **kwargs)
            except:
                logger.exception("Error executing side_effect for %s: %s", label, func.__name__)

    def docs(self):
        """Return dict containing labels and function docstrings for all registered side-effects."""
        _docs = defaultdict(list)
        for label in self.labels():
            for func in self.functions(label):
                _docs[label].append(parse_docstring(func))
        return dict(_docs)


def parse_docstring(func):
    """Strip the first line from a docstring."""
    try:
        return func.__doc__.strip().split('\n')[0]
    except AttributeError:
        return None


def register_side_effect(label, func):
    """Helper function to add a side-effect function to the registry."""
    _registry.add(label, func)


def run_side_effects(label, *args, **kwargs):
    """Run all of the side-effect functions registered for a label."""
    _registry.execute(label, *args, **kwargs)


def display_side_effects():
    """Print out the docs for all side-effects (in YAML block style)."""
    print yaml.dump(_registry.docs(), default_flow_style=False)

# global registry
_registry = Registry()
