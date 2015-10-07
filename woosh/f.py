from woosh.builtin_env import BUILTIN_ENV
import woosh.woo_types as w
import woosh.woo_instances as i
import woosh.woo_z as z
from woosh.errors import WrongArgumentTypeError
import os
import pwd
import grp


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


class Ls(NativeFun):
    args = arg_types('source=.:Path')
    kwargs = kwarg_types('@hide=False:Bool @hide_dir=False:Bool')
    return_type = w.List(BUILTIN_ENV['Resource'])

    def call(self, env):
        out = []
        out = [self.parse_file(file)
               for file in os.listdir(self.run_args[0].path)
               if (file[0] != '.' or not self.run_kwargs['hide'].value) and
                  (os.path.isfile(file) or not self.run_kwargs['hide_dir'].value)]
        return i.WooList(out, self.return_type)

    def parse_file(self, file):
        full_os_file_path = os.path.join(
            os.path.abspath(self.run_args[0].path), file)
        t = os.stat(full_os_file_path)
        resource = i.WooStruct({'path': z.WooPath(file), 'mode': self.parse_mode(
            oct(t[0])[2:]), 'size': z.WooInt(t.st_size)}, self.return_type.element_type)
        isfile = os.path.isfile(full_os_file_path)
        resource.slots['dir'] = z.WooBool(not isfile)
        resource.slots['count'] = z.WooInt(len(
            list(os.listdir(full_os_file_path))) if not isfile else 1)
        resource.slots['datetime'] = i.WooStruct(
            {'f': z.WooInt(t.st_mtime)}, BUILTIN_ENV['DateTime'])
        resource.slots['owner'] = z.WooString(pwd.getpwuid(t.st_uid).pw_name)
        resource.slots['group'] = z.WooString(grp.getgrgid(t.st_gid).gr_name)

        return resource

    def parse_mode(self, m):
        return i.WooStruct({'owner': self.parse_permission(m[2]),
                            'group': self.parse_permission(m[3]),
                            'other': self.parse_permission(m[4])}, BUILTIN_ENV['Mode'])

    def parse_permission(self, permission):
        return z.WooString(['none', 'execute', 'write', 'write and execute',
                            'read', 'read and execute', 'read and write', 'all'][int(permission)])

    # woo_types.Fun(arg_types=[('source', values['Path'])],
    #                       kwargs={'all': (False, woo_bool), 'dir': (
    #                           True, woo_bool)},
    #                       return_type=woo_types.List(values['Path'])))})

    #         woo_types.Fun(arg_types=[('dir', values['Path'])],
    #                       return_type=woo_types.Nil()))})


class Cd(NativeFun):
    args = arg_types('path=~:Path')
    kwargs = {}
    return_type = w.Nil

    def call(self, env):
        try:
            os.chdir(self.run_args[0].path)
        except FileNotFoundError:
            pass

        return w.WooNil
