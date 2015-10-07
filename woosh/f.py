from woosh.builtin_env import BUILTIN_ENV
import woosh.woo_types as w
import woosh.woo_instances as i
import woosh.woo_z as z
import pwd
import grp
import os
from woosh.command_base import arg_types, kwarg_types, NativeFun


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
