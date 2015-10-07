import woosh.woo_types as woo_types
import woosh.builtin_env as b


class WooString(WooObject):

    def __init__(self, value):
        self.value = value
        self.woo_type = b.woo_string


class WooInt(WooObject):

    def __init__(self, value):
        self.value = value
        self.woo_type = b.woo_int


class WooBool(WooObject):

    def __init__(self, value):
        self.value = value
        self.woo_type = b.woo_bool


class WooPath(WooObject):

    def __init__(self, path):
        self.path = path
        self.woo_type = b.BUILTIN_ENV['Path']
