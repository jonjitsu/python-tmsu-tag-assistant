"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mtmsu_tag_assistant` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``tmsu_tag_assistant.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``tmsu_tag_assistant.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import os
from pprint import pprint
import sys

import click
from click import echo

from .tmsu import tag_files_with, is_tmsu_initialized

def line_iter(stream):
    return iter(lambda: stream.readline().rstrip(), '')

def execute(c):
    ex, out, err = cmd(c)
    if ex != 0:
        echo(err, err=True)
    echo(out)

def execute_cmds(cmds):
    for cmd in cmds:
        execute(cmd.as_cmd())

def export_cmds(cmds, stream):
    stream.writelines(str(cmd) for cmd in cmds)

@click.command()
@click.option('-o', '--output', metavar='FILE', type=click.File('w'),
               help='Don\'t actually execute the tagging but save the commands to a file')
@click.argument('file', default='-', type=click.File('r'))
def main(file, output):
    if not is_tmsu_initialized():
        echo('TMSU not initialized. Please run:\ntmsu init', err=True)
        sys.exit(1)

    if not sys.__stdin__.isatty():
        echo('atty')
    # return
    # @TODO save to file to free up stdin so this works with piping

    files = line_iter(file)
    cmds = tag_files_with(files)
    if output is None:
        execute_cmds(cmds)
    else:
        export_cmds(cmds, output)
    echo("Cheers!")

