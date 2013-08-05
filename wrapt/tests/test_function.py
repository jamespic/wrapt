from __future__ import print_function

import unittest
import inspect

import wrapt

from .decorators import passthru_function_decorator

def function1(arg):
    '''documentation'''
    return arg

function1o = function1

@passthru_function_decorator
def function(arg):
    '''documentation'''
    return arg

function1d = function1

class TestNamingFunction(unittest.TestCase):

    def test_object_name(self):
        # Test preservation of function __name__ attribute.

        self.assertEqual(function1d.__name__, function1o.__name__)

    def test_object_qualname(self):
        # Test preservation of function __qualname__ attribute.

        try:
            __qualname__ = function1o.__qualname__
        except AttributeError:
            pass
        else:
            self.assertEqual(function1d.__qualname__, __qualname__)

    def test_module_name(self):
       # Test preservation of function __module__ attribute.

        self.assertEqual(function1d.__module__, __name__)

    def test_doc_string(self):
        # Test preservation of function __doc__ attribute.

        self.assertEqual(function1d.__doc__, function1o.__doc__)

    def test_argspec(self):
        # Test preservation of function argument specification.

        function1o_argspec = inspect.getargspec(function1o)
        function1d_argspec = inspect.getargspec(function1d)
        self.assertEqual(function1o_argspec, function1d_argspec)

    def test_isinstance(self):
        # Test preservation of isinstance() checks.

        self.assertTrue(isinstance(function1d, type(function1o)))

class TestCallingFunction(unittest.TestCase):

    def test_call_function(self):
        _args = (1, 2)
        _kwargs = { 'one': 1, 'two': 2 }

        @wrapt.function_decorator
        def _decorator(wrapped, args, kwargs):
            return wrapped(*args, **kwargs)

        @_decorator
        def _function(*args, **kwargs):
            return args, kwargs

        result = _function(*_args, **_kwargs)

        self.assertEqual(result, (_args, _kwargs))
