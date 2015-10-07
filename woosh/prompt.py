import getpass
import platform
import datetime
import subprocess
import re
import os
import os.path

FN = open(os.devnull, 'w')


def git_branch():
    try:
        return subprocess.check_output(['git', 'branch'], stderr=subprocess.STDOUT).split(b'\n')[0][2:]
    except subprocess.CalledProcessError:
        return ''


def git_repo():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT).strip().split(b'/')[-1]
    except subprocess.CalledProcessError:
        return ''


def display_pwd():
    pwd = os.getcwd()
    if pwd == os.path.expanduser('~'):
        return '~'
    else:
        return pwd.split('/')[-1]

LOADS = {
    'username': getpass.getuser,
    'host': lambda: '-'.join(platform.node().split('-')[1:]),
    'time': lambda: datetime.datetime.now().strftime('%H:%M'),
    'branch': git_branch,
    'repo': git_repo,
    'pwd': display_pwd
}

# {username}@{host}~{time}


class Prompt:

    def __init__(self, pattern, loads, load_styles):
        self.size, self.pattern, self.loads, self.load_styles = 0, pattern, loads, load_styles
        replaces = re.finditer(r'{[a-z]+}', self.pattern)
        self.replaces = []
        c = 0
        for r in replaces:
            if c < r.start():
                self.replaces.append(self.pattern[c:r.start()])
            self.replaces.append(self.pattern[r.start():r.end()])
            c = r.end()
        if c < len(self.pattern):
            self.replaces.append(self.pattern[c:])

    def deb(self, obj):
        with open('/home/penka-was-abducted/deb', 'a') as f:
            f.write(repr(obj) + '\n')

    def echo(self, shell):
        size = 0

        self.deb(self.load_styles)
        for a in self.replaces:
            if a[0] == '{':
                expanded = self.loads[a[1:-1]]()
                size += len(expanded)
                shell.screen.addstr(expanded, self.load_styles[a[1:-1]])
            else:
                size += len(a)
                shell.screen.addstr(a, 0)
        self.size = size


def generate(prompt_config):
    loads = {a: b for a, b in LOADS.items() if a in prompt_config['pattern']}
    load_styles = {a: b for a, b in prompt_config.items() if a != 'pattern'}

    return Prompt(prompt_config['pattern'], loads, load_styles)
