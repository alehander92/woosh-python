import os
import os.path
import woosh.parser


class WooError(Exception):
    pass


def complete(code, env):
    try:
        woo_type, expected, tokens = woosh.parser.parse_broken(code, env)
    except (CompletionError, woosh.parser.WooError, ValueError):
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
