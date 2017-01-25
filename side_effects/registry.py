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

    def docs(self, verbose=False):
        """Return dict containing labels and function docstrings for all registered side-effects."""
        _docs = defaultdict(list)
        for label in self.labels():
            for func in self.functions(label):
                _docs[label].append(_docstring(func, verbose=verbose))
        return dict(_docs)


def _docstring(func, verbose=False):
    """Strip the first line from a docstring."""
    if verbose:
        return func.__doc__
    try:
        return func.__doc__.strip().split('\n')[0]
    except AttributeError:
        return None


def register_side_effect(label, func):
    """Helper function to add a side-effect function to the registry."""
    _registry.add(label, func)


def run_side_effects(label, *args, **kwargs):
    """Run all of the side-effect functions registered for a label."""
    for func in _registry.functions(label):
        try:
            func(*args, **kwargs)
            # queue.enqueue(func, *args, **kwargs)
        except:
            logger.exception("Error running side_effect for %s: %s", label, func.__name__)
            # logger.exception("Error queueing side_effect for %s: %s", label, func.__name__)


def display_side_effects(verbose=False):
    """Print out the docs for all side-effects (in YAML block style)."""
    return yaml.dump(_registry.docs(verbose=verbose), default_flow_style=False)

# global registry - NB race condition warning.
_registry = Registry()
