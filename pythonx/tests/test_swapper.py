#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A series of tests for the style swapper.'''

# IMPORT STANDARD LIBRARIES
import textwrap
import unittest

# IMPORT THIRD-PARTY LIBRARIES
from python_style_swapper import swapper


class _Common(unittest.TestCase):

    '''A test case that defines some useful functions for refactoring functions.'''

    @staticmethod
    def _acquire_cursor(text):
        '''Get the cursor in some text and remove the cursor marker.

        Args:
            text (str): The code to find a cursor for.

        Returns:
            tuple[str, tuple[int, int]]:
                The modified code, followed by the row and column that the cursor
                was found in.

        '''
        lines = text.split('\n')

        for row, line in enumerate(lines):
            try:
                index = line.index('|')
            except ValueError:
                continue

            if line[index + 2] == '|':
                lines[row] = line.replace('|', '')
                return ('\n'.join(lines), (row + 1, index))

        raise ValueError('No cursor was found.')

    @staticmethod
    def _compare_function(code, row):
        '''str: Convert the code to a single line, at the given row number.'''
        return swapper.make_single_line(code, row)

    def _compare(self, expected, code):
        '''Assert that `code` matches `expected` when it is processed by our `_compare_function`.'''
        code, (row, _) = self._acquire_cursor(code)
        output = self._compare_function(code, row)

        self.assertEqual(expected, output)


class SingleLineSwap(_Common):

    '''A series of tests that force a single line into a multi-line Python function.'''

    @staticmethod
    def _compare_function(code, row):
        '''str: Convert the code to a multi-line, at the given row number.'''
        return swapper.make_multi_line(code, row)

    def test_best_case(self):
        '''Convert a basic single-line function into a multi-line function.'''
        code = textwrap.dedent(
            '''
            foo(bar, thing=None, an|o|ther={'asdfd': [('asdfasfd', 'tt'), 8]})
            '''
        )

        expected = textwrap.dedent(
            '''
            foo(
                bar,
                thing=None,
                another={'asdfd': [('asdfasfd', 'tt'), 8]},
            )
            '''
        )

        self._compare(expected, code)

    def test_weird_whitespace(self):
        '''Convert a basic single-line function into a multi-line function.'''
        code = textwrap.dedent(
            '''
            foo(   bar,     thing|=|None,     another={'asdfd': [('asdfasfd', 'tt'), 8]})
            '''
        )

        expected = textwrap.dedent(
            '''
            foo(
                bar,
                thing=None,
                another={'asdfd': [('asdfasfd', 'tt'), 8]},
            )
            '''
        )

        self._compare(expected, code)


class MultiLineSwap(_Common):

    '''A series of tests to convert various multi-line calls into a single line.'''

    def test_best_case(self):
        '''Convert a basic multi-line function into a single-line function.'''
        code = textwrap.dedent(
            '''
            foo(
                thin|g|,
                bar,
                fizz,
                another,
            )
            '''
        )

        expected = textwrap.dedent(
            '''
            foo(thing, bar, fizz, another)
            '''
        )

        self._compare(expected, code)

    def test_another_case(self):
        '''Convert a basic multi-line function into a single-line function.'''
        code = textwrap.dedent(
            '''
            foo(
                thing,
                bar,
                f|i|zz,
                another
            )
            '''
        )

        expected = textwrap.dedent(
            '''
            foo(thing, bar, fizz, another)
            '''
        )

        self._compare(expected, code)

    def test_mixed_indentation(self):
        '''Convert a non-standard multi-line function into a single-line function.'''
        code = textwrap.dedent(
            '''
            foo(
                thing,
                    bar,
            f|i|zz,
                        another
            )
            '''
        )

        expected = textwrap.dedent(
            '''
            foo(thing, bar, fizz, another)
            '''
        )

        self._compare(expected, code)


class SingleLineAssignmentSwap(_Common):

    '''A series of tests to convert various single-line calls into a multi-line call.'''

    @staticmethod
    def _compare_function(code, row):
        return swapper.make_multi_line(code, row)

    def test_best_case(self):
        '''Convert a basic single-line function into a multi-line function.'''
        code = textwrap.dedent(
            '''
            obj = foo(bar, thing=None, an|o|ther={'asdfd': [('asdfasfd', 'tt'), 8]})
            '''
        )

        expected = textwrap.dedent(
            '''
            obj = foo(
                bar,
                thing=None,
                another={'asdfd': [('asdfasfd', 'tt'), 8]},
            )
            '''
        )

        self._compare(expected, code)

    def test_weird_whitespace(self):
        '''Convert a non-standard single-line function into a multi-line function.'''
        code = textwrap.dedent(
            '''
            obj = foo(   bar,     thing|=|None,     another={'asdfd': [('asdfasfd', 'tt'), 8]})
            '''
        )

        expected = textwrap.dedent(
            '''
            obj = foo(
                bar,
                thing=None,
                another={'asdfd': [('asdfasfd', 'tt'), 8]},
            )
            '''
        )

        self._compare(expected, code)


class MultiLineAssignmentSwap(_Common):

    '''A series of tests to convert various multi-line calls into a single line.'''

    def test_best_case(self):
        '''Convert a basic multi-line function into a single-line function.'''
        code = textwrap.dedent(
            '''
            obj = foo(
                thin|g|,
                bar,
                fizz,
                another,
            )
            '''
        )

        expected = textwrap.dedent(
            '''
            obj = foo(thing, bar, fizz, another)
            '''
        )

        self._compare(expected, code)

    def test_another_case(self):
        '''Convert a basic multi-line function into a single-line function.'''
        code = textwrap.dedent(
            '''
            obj = foo(
                thing,
                bar,
                f|i|zz,
                another
            )
            '''
        )

        expected = textwrap.dedent(
            '''
            obj = foo(thing, bar, fizz, another)
            '''
        )

        self._compare(expected, code)

    def test_mixed_indentation(self):
        '''Convert a non-standard multi-line function into a single-line function.'''
        code = textwrap.dedent(
            '''
            obj = foo(
                thing,
                    bar,
            f|i|zz,
                        another
            )
            '''
        )

        expected = textwrap.dedent(
            '''
            obj = foo(thing, bar, fizz, another)
            '''
        )

        self._compare(expected, code)


class ToggleStyle(_Common):

    '''A series of tests that converts call functions automatically.'''

    @staticmethod
    def _compare_function(code, row):
        '''str: Convert the code to a single line, at the given row number.'''
        toggled_code = swapper.toggle(code, row)[0]
        return toggled_code

    def test_weird_whitespace(self):
        '''Convert a basic single-line function into a multi-line function.'''
        code = textwrap.dedent(
            '''
            foo(   bar,     thing|=|None,     another={'asdfd': [('asdfasfd', 'tt'), 8]})
            '''
        )

        expected = textwrap.dedent(
            '''
            foo(
                bar,
                thing=None,
                another={'asdfd': [('asdfasfd', 'tt'), 8]},
            )
            '''
        )

        self._compare(expected, code)

    def test_mixed_indentation(self):
        '''Convert a non-standard multi-line function into a single-line function.'''
        code = textwrap.dedent(
            '''
            foo(
                thing,
                    bar,
            f|i|zz,
                        another
            )
            '''
        )

        expected = textwrap.dedent(
            '''
            foo(thing, bar, fizz, another)
            '''
        )

        self._compare(expected, code)
