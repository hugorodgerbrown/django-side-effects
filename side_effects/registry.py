# -*- coding: utf-8 -*-
"""side_effects.registry"""
from collections import defaultdict


class Registry(object):

    """Registry of side effect functions."""

    def __init__(self):
        self._registry = defaultdict(list)

    def register(self, label, func):
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
        self._registry[label].append(func)

    def execute(self, label, *args, **kwargs):
        """Execute all the side-effects functions registered to a label."""
        for func in self._registry[label]:
            func(*args, **kwargs)

    def docs(self):
        """Print out the docstrings for all registered side-effects."""
        for key in sorted(self._registry.keys()):
            print self._registry[key].__doc__
