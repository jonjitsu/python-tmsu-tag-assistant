import os
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.key_binding.defaults import load_key_bindings_for_prompt
from prompt_toolkit.keys import Keys

from .process import cmd, background

HISTORY_FILE = os.path.expanduser('~/.tmsu-ta-history')

def touch(filename):
    open(filename, 'a').close()

if not os.path.isfile(HISTORY_FILE):
    touch(HISTORY_FILE)

def is_tmsu_initialized():
    ex, out, err = cmd('tmsu info')
    return ex == 0


def parse_tags_list(o):
    """"""
    if '' == o.strip():
        return set()
    else:
        return set(o.strip().split(os.linesep))

def get_all_tags():
    ex, o, _ = cmd('tmsu tags')
    assert ex == 0
    return parse_tags_list(o)



def parse_tags_from_output(cmd_output):
    return set(cmd_output.split()[1:])

def get_file_tags(f):
    """ Return the current tags for a file f.

        Returns:
           Set(str)   a set representing all the tags
    """
    ex, o, _ = cmd(['tmsu', 'tags', f])
    assert ex == 0
    return parse_tags_from_output(o)

def get_suggested_tags(f, possible_tags):
    """ Given:
        - a file f
        - a set of tags
        return tag suggestions

        Possibilities:
        - from filename/path
        - from metadata
    """

class PromptTagger(object):
    def __init__(self, completer=None, history=None, auto_suggest=None):
        self.completer = completer if completer else WordCompleter(get_all_tags())
        self.history = history if history else FileHistory(HISTORY_FILE)
        self.auto_suggest = auto_suggest if auto_suggest else AutoSuggestFromHistory()
        self.registry = load_key_bindings_for_prompt()


    def __call__(self, file):
        registry = self.registry
        @registry.add_binding(Keys.F4, eager=True)
        def _(event):
            # event.cli.current_buffer.insert_text('hello world')
            background(['xdg-open', file])

        def tags_to_str(tags):
            return ' '.join(tags)

        current_tags = get_file_tags(file)
        p = "%s: %s\n> " % (file, tags_to_str(current_tags))
        tags = prompt(p, history=self.history,
                      auto_suggest=self.auto_suggest,
                      completer=self.completer,
                      key_bindings_registry=registry)
        tags = set(tags.strip().split(' '))
        self.add_tags_to_completer(tags)
        return tags

    def add_tags_to_completer(self, tags):
        current = set(self.completer.words)
        self.completer.words = list(current | tags)


def quote(s, char="'"):
    return char + s + char

def tags_to_str(tags, sep=' '):
    """Given a set of tags,
       return a string."""
    if isinstance(tags, set) or isinstance(tags, list):
        return sep.join(quote(tag) for tag in sorted(tags))
    else:
        raise 'Expected collection.'

class TmsuCmd(object):
    """ Represents a tmsu command.
        Works only with tag/untag commands.
    """
    TMSU_CMD = 'tmsu'
    def __init__(self, subcmd, *args):
        self.subcmd = subcmd
        self.args = args

    def __str__(self):
        """ Represent as a string invokable on command line.
            Works only with tag/untag commands.
        """
        args = list(self.args)
        cmd = [self.TMSU_CMD, self.subcmd]
        cmd.append("'%s'" % args.pop(0))
        cmd.append(tags_to_str(args.pop()))
        assert len(args) == 0
        return ' '.join(cmd)

    def as_cmd(self):
        """ Return this command in a format to be executed by subprocess.* functions. """
        args = list(self.args)
        cmd = [self.TMSU_CMD, self.subcmd]
        cmd.append(args.pop(0))
        cmd.extend(sorted(args.pop()))
        assert len(args) == 0
        return cmd

    @classmethod
    def tag(cls, file, tags):
        return cls('tag', file, tags)

    @classmethod
    def untag(cls, file, tags):
        return cls('untag', file, tags)

def tag_files_with(files, tagger=None):
    """ Given:
        - a collection of files
        - a tagging function
        return a collection of TmsuCmd
    """
    tagger = tagger or PromptTagger()
    return (TmsuCmd.tag(f, tagger(f)) for f in files)
