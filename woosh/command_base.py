from woosh.builtin_env import BUILTIN_ENV
import woosh.woo_types as w
import woosh.woo_z as z
from woosh.errors import WrongArgumentTypeError


def arg_types(signature):
    return [parse_sub(t) for t in signature.split()]


def kwarg_types(signature):
    return dict(parse_kwsub(t) for t in signature.split())


def parse_sub(sub):
    '''
    @returns label, woo_type, default_value
    '''
    left, type = sub.split(':')
    if '=' in left:
        return left.split('=')[0], BUILTIN_ENV[type], parse_literal(left.split('=')[1])
    else:
        return left, BUILTIN_ENV[type], None


def parse_kwsub(sub):
    '''
    @returns label, woo_type, default_value
    label without '@'
    '''
    left, type = sub.split(':')
    if '=' in left:
        return left.split('=')[0][1:], (BUILTIN_ENV[type], parse_literal(left.split('=')[1]))
    else:
        return left, BUILTIN_ENV[type], None


def parse_literal(literal):
    if literal in ['True', 'False']:
        return z.WooBool(literal == 'True')
    elif literal[0] == '\'':
        return z.WooString(literal[1:-1])
    elif literal[0].isdigit():
        return z.WooInt(int(literal))
    else:
        return z.WooPath(literal)


class WFun:

    def __init__(self, args, kwargs):
        self.call_args, self.call_kwargs = args, kwargs

    def call(self, env):
        return woosh.woo_types.Nil()


class NativeFun(WFun):

    def __init__(self, args, kwargs):
        self.call_args, self.call_kwargs = args, kwargs
        self.run_args, self.run_kwargs = [], []
        for (label, arg_type, default_value), c_arg in zip(self.args, self.call_args):
            if arg_type != c_arg.woo_type:
                raise WrongArgumentTypeError('{0} type mismatch'.format(label))
            self.run_args.append((label, c_arg))
        self.run_args.extend((label, default_value) for label,
                             arg_type, default_value in self.args[len(self.call_args):])

        self.run_args = [a for l, a in self.run_args]
        # print(self.kwargs)
        for label, (kwarg_type, default_value) in self.kwargs.items():
            if label not in self.call_kwargs:
                self.run_kwargs.append((label, default_value))
            else:
                c_kwarg = self.call_kwargs[label]
                if kwarg_type != c_kwarg.woo_type:
                    raise WrongArgumentTypeError(
                        '@{0} type mismatch'.format(label))
                self.run_kwargs.append((label, c_kwarg))

        self.run_kwargs = dict(self.run_kwargs)

    @classmethod
    def woo_type(cls):
        return w.Fun(arg_types=cls.args, kwargs=cls.kwargs, return_type=cls.return_type)
