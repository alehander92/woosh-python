from woosh.woo_instances import WooObject
import woosh.builtin_env as b
import os.path


class WooString(WooObject):

    def __init__(self, value):
        self.value = value
        self.woo_type = b.woo_string

    def as_string(self):
        return '\'{0}\''.format(self.value)


class WooInt(WooObject):

    def __init__(self, value):
        self.value = value
        self.woo_type = b.woo_int

    def as_string(self):
        return str(self.value)


class WooBool(WooObject):

    def __init__(self, value):
        self.value = value
        self.woo_type = b.woo_bool

    def as_string(self):
        return 'True' if self.value else 'False'


class WooPath(WooObject):

    def __init__(self, path):
        self._path = path
        self.woo_type = b.BUILTIN_ENV['Path']

    @property
    def path(self):
        if not self._path or self._path[0] != '~':
            return self._path
        else:
            return os.path.expanduser(self._path)

    def as_string(self):
        return self.path
