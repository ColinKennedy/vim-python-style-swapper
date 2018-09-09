#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A set of classes and functions needed to parse and print Python callable objects.'''

# IMPORT THIRD-PARTY LIBRARIES
# TODO : Make the functions used from the `parser` module into a common plug-in (so it can be re-used)
from python_function_expander.trimmer import parser
from astroid import as_string
import astroid


class MultiLineCallVisitor(as_string.AsStringVisitor):

    '''A visitor that re-prints <astroid.Call> nodes in a multi-line style.

    Attributes:
        _single_line_exceptions (tuple[str]):
            Any functions, by-name, which should not allowed to be made multi-line.

    '''

    _single_line_exceptions = ('super', )

    def _format_args(self, args):
        '''Change the given arguments into "multi-line" style arguments.

        Args:
            args (list[str]):
                The list of args/kwargs to change.

        Returns:
            list[str]: The multi-line representation of `args`.

        '''
        if not args:
            return ''

        # `args` has a chance of being a tuple. We need indexing so convert it to a list
        args = list(args)

        # Add proper indentation to every arg
        args[0] = '\n{indent}'.format(indent=self.indent) + args[0]
        args = [args[0]] + ['{indent}{name}'.format(indent=self.indent, name=name) for name in args[1:]]

        # Add commas to every arg, including the last arg
        args[-1] += ',\n'
        args = ',\n'.join(args)

        return args

    def _make_multi_line(self, node):
        '''list[str]: Add newline and extra space to each arg and kwarg.'''
        args = [arg.accept(self) for arg in node.args]
        keywords = []

        if node.keywords:
            keywords = [kwarg.accept(self) for kwarg in node.keywords]

        args.extend(keywords)
        return self._format_args(args)

    def visit_call(self, node):
        '''Expand an <astroid.Call> object into a valid Python string.

        Args:
            node (<astroid.Call>): The node to create a string representation for.

        Returns:
            str: The printable representation of the given `node`.

        '''
        expression = node.func.accept(self)

        try:
            if node.func.name in self._single_line_exceptions:
                return node.as_string()
        except AttributeError:
            # This only happens if node is a <astroid.Attribute>
            # An attribute will never be in the list of function exceptions so
            # just ignore it.
            #
            pass

        args = self._make_multi_line(node)

        return '{expression}({args})'.format(expression=expression, args=args)


def get_indent(text):
    return text[:len(text) - len(text.lstrip())]


def make_single_line(code, row):
    '''Convert the multi-line called object in some row into a single-line.

    Args:
        code (str): The full body of text to consider changing.
        row (int): A 1-based integer which represents the user's cursor position.

    Returns:
        str: The modified code.

    '''
    lines = code.split('\n')

    node = parser.get_nearest_call(code, row)

    if isinstance(node.parent, astroid.Assign):
        node = node.parent

    indent = get_indent(lines[node.fromlineno - 1])
    output_lines = node.as_string().split('\n')
    output_lines = ['{indent}{text}'.format(indent=indent, text=text) for text in output_lines]

    start = node.fromlineno - 1
    end = parser.get_tolineno(node, lines)
    lines[start:end] = output_lines

    code = '\n'.join(lines)

    return code


def make_multi_line(code, row):
    '''Convert the single-line callable object into a mult-line function.

    Args:
        code (str): The full body of text to consider changing.
        row (int): A 1-based integer which represents the user's cursor position.

    Returns:
        str: The modified code.

    '''
    lines = code.split('\n')

    node = parser.get_nearest_call(code, row)

    if isinstance(node.parent, astroid.Assign):
        node = node.parent

    # TODO : Indent must be retrieved from the user's config
    visitor = MultiLineCallVisitor(indent='    ')
    output = visitor(node)

    indent = get_indent(lines[node.fromlineno - 1])
    output_lines = output.split('\n')
    output_lines = ['{indent}{text}'.format(indent=indent, text=text) for text in output_lines]

    start = node.fromlineno - 1
    end = parser.get_tolineno(node, lines)
    lines[start:end] = output_lines

    code = '\n'.join(lines)

    return code


def toggle(code, row):
    '''Change a single-line call into a multiline call or vice-versa.

    Args:
        code (str): The code to change.
        row (int): A 0-based line number value to search for a call.

    Returns:
        tuple[str, <astroid.Call> or NoneType]:
            The changed code and the found astroid node, if any.
            If no astroid node is found, the original code is returned, untouched.

    '''
    lines = code.split('\n')

    call = parser.get_nearest_call(code, row)

    if not call:
        return (code, None)

    if call.fromlineno == parser.get_tolineno(call, lines):
        output = make_multi_line(code, row)
    else:
        output = make_single_line(code, row)

    lines = output.split('\n')
    code = '\n'.join(lines)

    return (code, call)
