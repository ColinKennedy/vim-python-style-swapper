#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
from python_function_expander.trimmer import parser
from astroid import as_string


class MultiLineCallVisitor(as_string.AsStringVisitor):

    '''A visitor that re-prints <astroid.Call> nodes in a multi-line style.'''

    def visit_call(self, node):
        expression = node.func.accept(self)
        args = [arg.accept(self) for arg in node.args]
        if node.keywords:
            keywords = [kwarg.accept(self) for kwarg in node.keywords]
        else:
            keywords = []

        args.extend(keywords)

        try:
            args[0] = '\n{indent}'.format(indent=self.indent) + args[0]
        except IndexError:
            pass

        try:
            args[-1] += ',\n'
        except IndexError:
            pass

        args = ['{indent}{name}'.format(indent=self.indent, name=name) for name in args]

        return '{expression}({args})'.format(expression=expression, args=',\n'.join(args))


def test_single_line():
    import textwrap

    code = textwrap.dedent(
        '''
        foo(
            thing,
            bar,
            fizz,
            another
        )
        '''
    )

    # print(make_multi_line(code, 2))
    print(make_single_line(code, 2))


def test_multi_line():
    import textwrap

    code = textwrap.dedent(
        '''
        foo(thing, bar, fizz, another)
        '''
    )

    print(make_multi_line(code, 2))
    # print(make_single_line(code, 2))


def make_single_line(code, row):
    # '''Convert the multi-line called object in some row into a single-line.

    # Args:
    #     code (str):

    # Returns:

    # '''
    lines = code.split('\n')

    call = parser.get_nearest_call(code, row)
    end = parser.get_tolineno(call, lines)

    lines[call.fromlineno - 1:end] = call.as_string().split('\n')
    code = '\n'.join(lines)

    return code


def make_multi_line(code, row):
    lines = code.split('\n')

    call = parser.get_nearest_call(code, row)

    # TODO : Indent must be retrieved from the user's config
    visitor = MultiLineCallVisitor(indent='    ')
    output = visitor(call)

    end = parser.get_tolineno(call, lines)
    lines[call.fromlineno - 1:end] = output.split('\n')
    code = '\n'.join(lines)

    return code


# test_single_line()
test_multi_line()
