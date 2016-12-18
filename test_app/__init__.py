# -*- coding: utf-8 -*-
"""test_app."""
from side_effects.decorators import (
    has_side_effects,
    is_side_effect_of
)


@has_side_effects('foo')
def foo():
    print 'this is foo'


@is_side_effect_of('foo')
def bar():
    """This is function with a one-line docstring."""
    print 'this is bar, a side-effect of foo'


@is_side_effect_of('foo')
def baz():
    """
    This is function with a two-line docstring.

    More details go here.
    """
    print 'this is baz, a side-effect of foo'
