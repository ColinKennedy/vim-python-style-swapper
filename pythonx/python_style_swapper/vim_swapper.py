#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORT THIRD-PARTY LIBRARIES
import vim

# IMPORT LOCAL LIBRARIES
from . import swapper


def _to_vim(cursor):
    '''tuple[int, int]: Change the given cursor to a Vim cursor, which is base-1.'''
    # Reference: https://github.com/reconquest/vim-pythonx
    #            I copied the code from this repository, to avoid the extra dependency
    #
    return (cursor[0] + 1, cursor[1])


def _set_cursor(cursor):
    '''Set the current cursor as the user's cursor in the current buffer.'''
    # Reference: https://github.com/reconquest/vim-pythonx
    #            I copied the code from this repository, to avoid the extra dependency
    #
    vim.current.window.cursor = _to_vim(cursor)


def toggle():
    code = '\n'.join(vim.current.window.buffer)

    (row, _) = vim.current.window.cursor

    output, call = swapper.toggle(code, row)

    if not call:
        return

    lines = output.splitlines()

    # TODO : Consider making this better by NOT replacing the entire buffer and
    # instead just replacing the part of the buffer where the function text was
    # changed. Or not! https://ubiquity.acm.org/article.cfm?id=1513451
    #
    vim.current.window.buffer[:] = lines

    # TODO : Figure out a way to convert the cursor
    # first_non_whitespace_character_column = \
    #     len(trimmed_lines[call.fromlineno - 1]) - \
    #     len(trimmed_lines[call.fromlineno - 1].lstrip())

    # _set_cursor((call.fromlineno - 1, first_non_whitespace_character_column))
