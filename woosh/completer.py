import os
import os.path


class CompletionError(Exception):
    pass

TOKEN_FUN, TOKEN_PATH, TOKEN_METHOD, TOKEN_INT, TOKEN_ARG = range(5)

LITERAL_TYPES = {'Path': 'path', 'Int': 'int'}


def complete(code, env):
    try:
        woo_type, expected, tokens = parse(code, env)
    except (CompletionError, ValueError):
        return []

    finished = not code or code[-1] == ' '
    return [globals()['complete_%s' % tab](woo_type, tokens[-1][1], env, finished) for tab in expected]


def complete_fun(woo_type, token, env, finished=True):
    # returns a list with the matching function names in env
    f = env
    completions = set()
    while f:
        completions.update(
            g for g, value
            in f.values.items()
            if hasattr(value, 'code') and (finished or g.startswith(token)))
        f = f.parent
    return list(completions)


def complete_path(woo_type, token, env, finished=True):
    # returns a list with the matching paths in current dir
    return [f for f in os.listdir('.') if finished or f.startswith(token)]


def complete_method(woo_type, token, env, finished=True):
    # returns a list with the matching methods of woo_type
    if not hasattr(woo_type.return_type, 'methods'):
        return []
    return ['{0}{1}'.format('#' if m[0].isalpha() else '', m)
            for m in woo_type.return_type.methods
            if finished or m.startswith(token[1:])]


def complete_arg(woo_type, token, env, finished=True):
    # returns a list with the matching kwargs of woo_type
    return ['@{0}'.format(label)
            for label in woo_type.kwargs
            if finished or label.startswith(token[1:])]  # @arg


def extract_type(tokens, env):
    for token in tokens[::-1]:
        if token[0] == TOKEN_FUN:
            fun = env[token[1]]
            if fun is None:
                raise CompletionError('unknown fun')
            return fun.woo_type
    return None


def classify_token(token, first=False, finished=True):
    if token == '' and first:
        return TOKEN_FUN, ''
    if token == '':
        return TOKEN_PATH, ''

    if token[0].isalpha() and token[0].islower() and first:
        for t in token[1:]:
            if not (t.isalnum() or t in '-_'):
                raise CompletionError('Unexpected symbol in fun')
        return TOKEN_FUN, token

    elif token[0].isdigit():
        for t in token[1:]:
            if not t.isdigit():
                raise CompletionError('Unexpected nan in int')
        return TOKEN_INT, token

    elif not first and (token[0].isalpha() or token[0] in '~.'):
        return TOKEN_PATH, token

    elif token[0] == '@':
        for t in token[1:]:
            if not (t.isalnum() or t in '-_~'):
                raise CompletionError()
        return TOKEN_ARG, token

    elif token[0] == '#':
        for t in token[1:]:
            if not (t.isalnum() or t in '-_~'):
                raise CompletionError()

        return TOKEN_METHOD, token

    else:
        raise CompletionError()


def tokenize(s):
    '''
    ls m
    => [(TOKEN_FUN, 'ls'), (TOKEN_PATH, 'm')]
    git #add
    => [(TOKEN_FUN, 'git'), (TOKEN_METHOD, '#add')]
    '''
    token_strings = s.split()
    tokens = [None] * len(token_strings)
    if not token_strings:
        return []
    elif len(token_strings) == 1:
        return [classify_token(
            token_strings[0], first=True, finished=s[-1] == ' ')]

    tokens[0] = classify_token(token_strings[0], first=True, finished=True)
    tokens[1:-1] = [classify_token(t) for t in token_strings[1:-1]]
    tokens[-1] = classify_token(token_strings[-1],
                                first=False, finished=s[-1] == ' ')
    return tokens


def parse(current, env):
    tokens = tokenize(current)
    if tokens == []:
        return None, [], []

    finished_token = current[-1] == ' '
    finished = tokens if finished_token else tokens[:-1]
    woo_type = extract_type(finished, env)

    expected = []
    if tokens[-1][0] in [TOKEN_FUN, TOKEN_METHOD]:
        if finished_token:
            # print(woo_type.arg_types[0].woo_type.__dict__)
            # input()
            if woo_type.arg_types and woo_type.arg_types[0].woo_type.label in LITERAL_TYPES:
                expected = [LITERAL_TYPES[
                    woo_type.arg_types[0].woo_type.label]]
            expected.extend(['arg', 'method'])
        else:
            expected = ['fun' if tokens[-1][0]
                        == TOKEN_FUN else 'method']
    elif tokens[-1][0] == TOKEN_PATH:
        if finished_token:
            expected = ['arg', 'method']
        else:
            expected = ['path']

    elif tokens[-1][0] == TOKEN_ARG:
        if finished_token:
            expected = ['arg', 'method']
        else:
            expected = ['arg']

    return woo_type, expected, tokens


def token_name(token):
    return ['token_fun', 'token_path', 'token_method', 'token_int', 'token_arg'][token]
