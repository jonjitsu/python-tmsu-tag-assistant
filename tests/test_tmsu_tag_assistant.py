import pytest
# from click.testing import CliRunner

# from tmsu_tag_assistant.cli import main


# def test_main():
#     runner = CliRunner()
#     result = runner.invoke(main, ['--help'])

#     assert result.output == '()\n'
#     assert result.exit_code == 0

from tmsu_tag_assistant.cli import line_iter
from io import StringIO
import os
from collections import Iterable

def test_line_iter():
    lines = ['line1', 'line2']
    stream = StringIO(os.linesep.join(lines))
    it = line_iter(stream)
    # assert is an iterator
    assert iter(it) == iter(it)
    for actual, expected in zip(it, lines):
        assert actual == expected

    stream = StringIO(os.linesep.join(lines) + os.linesep)
    it = line_iter(stream)
    # assert is an iterator
    assert iter(it) == iter(it)
    for actual, expected in zip(it, lines):
        assert actual == expected

from tmsu_tag_assistant.process import cmd

def test_cmd():
    ex, out, err = cmd('true')
    assert ex == 0
    assert out == ''
    assert err == ''

    ex, out, err = cmd('false')
    assert ex == 1
    assert out == ''
    assert err == ''

    ex, out, err = cmd('ls /aasdflas12390812309asdfasdf')
    assert ex == 2
    assert out == ''
    assert err == 'ls: cannot access /aasdflas12390812309asdfasdf: No such file or directory\n'

    ex, out, err = cmd(['bash', '-c', 'echo testing 123'])
    assert ex == 0
    assert out == 'testing 123\n'
    assert err == ''


from tmsu_tag_assistant.tmsu import parse_tags_from_output, parse_tags_list

def test_parse_tags_from_output():
    o = "Generators.pdf: ebook python compsci"
    expected = {'ebook', 'python', 'compsci'}
    assert expected == parse_tags_from_output(o)

    o = "Generators.pdf:"
    assert set() == parse_tags_from_output(o)

def test_parse_tags_list():
    o = ""
    assert parse_tags_list(o) == set()

    o = 'tag1\n'
    assert parse_tags_list(o) == {'tag1'}

    tags = {'tag1', 'tag2'}
    o = '\n'.join(tags)
    assert parse_tags_list(o) == tags
    o = '\n'.join(tags) + '\n'
    assert parse_tags_list(o) == tags

from tmsu_tag_assistant.tmsu import TmsuCmd

def test_TmsuCmd_tag():
    file = 'Generators.pdf'
    tags = {'pdf', 'ebook', 'python'}
    cmd = TmsuCmd.tag(file, tags)
    assert isinstance(cmd, TmsuCmd)

def test_TmsuCmd_untag():
    file = 'Generators.pdf'
    tags = {'pdf', 'ebook', 'python'}
    cmd = TmsuCmd.untag(file, tags)
    assert isinstance(cmd, TmsuCmd)

def test_TmsuCmd_str():
    file = 'Generators Tutorial 2011.pdf'
    tags = {'pdf', 'ebook', 'python'}
    cmd = TmsuCmd.tag(file, tags)
    expected = "tmsu tag '%s' 'ebook' 'pdf' 'python'" % (file)
    assert str(cmd) == expected

def test_TmsuCmd_as_cmd():
    file = 'Generators Tutorial 2011.pdf'
    tags = {'pdf', 'ebook', 'python'}
    cmd = TmsuCmd.tag(file, tags)
    expected = ['tmsu', 'tag', file, 'ebook', 'pdf', 'python']
    assert cmd.as_cmd() == expected

from tmsu_tag_assistant.tmsu import tag_files_with

def test_tag_files_with():
    tags = {'pdf', 'ebook', 'year=1923'}
    tagger = lambda f: tags
    files = ['Generators.pdf']
    actual = list(tag_files_with(files, tagger))
    assert isinstance(actual[0], TmsuCmd)
    assert "tmsu tag 'Generators.pdf' 'ebook' 'pdf' 'year=1923'" == str(actual[0])


from tmsu_tag_assistant.tmsu import simple_suggested_tags

def test_simple_suggested_tags():
    tags = ['python', 'ebook', 'compsci']
    f = './papers/Python Generators and object oriented programming.epub'
    suggested = simple_suggested_tags(f, tags)
    assert suggested == {'python'}
