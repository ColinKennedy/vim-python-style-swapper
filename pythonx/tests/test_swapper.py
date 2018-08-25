#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        return swapper.make_single_line(code, row)

    def _compare(self, expected, code):
        code, (row, _) = self._acquire_cursor(code)
        output = self._compare_function(code, row)

        # raise ValueError(output)
        # raise ValueError(expected)

        for index, (char1, char2) in enumerate(zip(expected, output)):
            if char1 != char2:
                raise ValueError((char1, expected[:index + 1], output[:index + 1]))

        # raise ValueError(output)
        # raise ValueError(expected)

        self.assertEqual(expected, output)


class SingleLineSwap(_Common):

    @staticmethod
    def _compare_function(code, row):
        return swapper.make_multi_line(code, row)

    def test_best_case(self):
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

    def test_best_case(self):
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


class ToggleStyle(_Common):

    @staticmethod
    def _compare_function(code, row):
        toggled_code = swapper.toggle(code, row)[0]
        return toggled_code

    def test_weird_whitespace(self):
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
