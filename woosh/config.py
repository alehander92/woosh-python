import sys

PATH = ".woosh.yaml"


def load():
    with open(PATH, 'r') as f:
        source = f.read()
    return parse(source)


def parse(source):
    return dict([parse_pair(line) for line in source.split('\n')])


def parse_pair(code):
    key, value = code.split(':')[:2]
    value = value.strip()[1:-1]
    return key, value
