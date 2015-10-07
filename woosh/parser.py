import woosh.grammar
import woosh.converter

TOKEN_FUN, TOKEN_PATH, TOKEN_METHOD, TOKEN_INT, TOKEN_ARG, TOKEN_BLOCK = range(
    6)

LITERAL_TYPES = {'Path', 'Int'}


class WooError(Exception):
    pass


def parse(code):
    parsed = woosh.grammar.WooGrammar.parse(code)
    return woosh.converter.Converter().convert(parsed)


def extract_type(tokens, env):
    for token in tokens[::-1]:
        if token[0] == TOKEN_FUN:
            fun = env[token[1]]
            if fun is None:
                raise WooError('unknown fun')
            return fun.woo_type
    return None


def classify_token(token, first=False, finished=True, in_block=False):
    if token == '' and first:
        return TOKEN_FUN, ''
    if token == '':
        return TOKEN_PATH, ''

    if token[0].isalpha() and token[0].islower() and first:
        for t in token[1:]:
            if not (t.isalnum() or t in '-_'):
                raise WooError('Unexpected symbol in fun')
        return TOKEN_FUN, token

    elif token[0].isdigit():
        for t in token[1:]:
            if not t.isdigit():
                raise WooError('Unexpected nan in int')
        return TOKEN_INT, token

    elif not first and (token[0].isalpha() or token[0] in '~.'):
        return TOKEN_PATH, token

    elif token[0] == '@':
        for t in token[1:]:
            if not (t.isalnum() or t in '-_~'):
                raise WooError()
        return TOKEN_ARG, token

    elif token[0] in '#|?':
        for t in token[1:]:
            if not (t.isalnum() or t in '-_~'):
                raise WooError()

        return TOKEN_METHOD, token

    elif token[0] == '{':
        return TOKEN_BLOCK, token

    else:
        raise WooError()


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
        return [], False
    elif len(token_strings) == 1:
        return [classify_token(
            token_strings[0], first=True, finished=s[-1] == ' ')], False

    tokens[0] = classify_token(token_strings[0], first=True, finished=True)
    in_block = False
    for i, t in enumerate(token_strings[1:-1]):
        type, tokens[i + 1] = classify_token(t, in_block=in_block)
        if type == TOKEN_BLOCK:
            in_block = True
        elif type == TOKEN_BLOCKOUT:
            if in_block:
                in_block = False
            else:
                raise WooError()

    # tokens[1:-1] = [classify_token(t) for t in token_strings[1:-1]]
    tokens[-1] = classify_token(token_strings[-1],
                                first=False, finished=s[-1] == ' ', in_block=in_block)
    if tokens[-1][0] == TOKEN_BLOCK or tokens[-1][0] == TOKEN_BLOCKOUT and not in_block:
        raise WooError()
    elif tokens[-1][0] == TOKEN_BLOCKOUT:
        in_block = False
    return tokens, in_block


def parse_broken(current, env):
    tokens, in_block = tokenize(current)
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
                expected = [woo_type.arg_types[0].woo_type.label.lower()]
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

    elif tokens[-1][0] == TOKEN_BLOCK:
        expected = ['anon_var', 'path']

    return woo_type, expected, tokens


def token_name(token):
    return ['token_fun', 'token_path', 'token_method', 'token_int', 'token_arg'][token]
