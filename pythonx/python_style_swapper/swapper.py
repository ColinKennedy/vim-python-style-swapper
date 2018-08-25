#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''A set of classes and functions needed to parse and print Python callable objects.'''

# IMPORT THIRD-PARTY LIBRARIES
# TODO : Make the functions used from this module a common plug-in (so it can be re-used)
from python_function_expander.trimmer import parser
from astroid import as_string


class MultiLineCallVisitor(as_string.AsStringVisitor):

    '''A visitor that re-prints <astroid.Call> nodes in a multi-line style.'''

    def _format_args(self, args):
        '''Change the given arguments into "multi-line" style arguments.

        Args:
            args (list[str]):
                The list of args/kwargs to change.

        Returns:
            list[str]: The multi-line representation of `args`.

        '''
        args = list(args)

        try:
            args[0] = '\n{indent}'.format(indent=self.indent) + args[0]
        except IndexError:
            return args


        args = [args[0]] + ['{indent}{name}'.format(indent=self.indent, name=name) for name in args[1:]]

        args[-1] += ',\n'

        return args

    def visit_call(self, node):
        '''Expand an <astroid.Call> object into a valid Python string.

        Args:
            node (<astroid.Call>): The node to create a string representation for.

        Returns:
            str: The printable representation of the given `node`.

        '''
        expression = node.func.accept(self)
        args = [arg.accept(self) for arg in node.args]
        if node.keywords:
            keywords = [kwarg.accept(self) for kwarg in node.keywords]
        else:
            keywords = []

        args.extend(keywords)

        args = self._format_args(args)

        return '{expression}({args})'.format(expression=expression, args=',\n'.join(args))


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

    call = parser.get_nearest_call(code, row)

    indent = get_indent(lines[call.fromlineno - 1])
    output_lines = call.as_string().split('\n')
    output_lines = ['{indent}{text}'.format(indent=indent, text=text) for text in output_lines]

    start = call.fromlineno - 1
    end = parser.get_tolineno(call, lines)
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

    call = parser.get_nearest_call(code, row)

    # TODO : Indent must be retrieved from the user's config
    visitor = MultiLineCallVisitor(indent='    ')
    output = visitor(call)

    indent = get_indent(lines[call.fromlineno - 1])
    output_lines = output.split('\n')
    output_lines = ['{indent}{text}'.format(indent=indent, text=text) for text in output_lines]

    start = call.fromlineno - 1
    end = parser.get_tolineno(call, lines)
    lines[start:end] = output_lines

    code = '\n'.join(lines)

    return code


def toggle(code, row):
    lines = code.split('\n')

    call = parser.get_nearest_call(code, row)

    if call.fromlineno == parser.get_tolineno(call, lines):
        output = make_multi_line(code, row)
    else:
        output = make_single_line(code, row)

    lines = output.split('\n')
    code = '\n'.join(lines)

    return (code, call)