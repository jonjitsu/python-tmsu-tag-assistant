import os
from subprocess import Popen, PIPE

def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode('utf-8')
    else:
        return bytes_or_str

def cmd(c):
    """ Run an external process and return the results. """
    if type(c) is str:
        c = c.split()

    process = Popen(c, stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    return process.returncode, to_str(out), to_str(err)

def background(c):
    if type(c) is str:
        c = c.split()

    with open(os.devnull, 'w') as devnull:
        Popen(c, stdout=devnull, stderr=devnull)
