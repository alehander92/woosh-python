from woosh.builtin_env import BUILTIN_ENV
import woosh.woo_instances
import woosh.f as f

BUILTIN_ENV.values.update({
    'ls': woosh.woo_instances.WooFun('ls', f.Ls, f.Ls.woo_type()),
    'cd': woosh.woo_instances.WooFun('cd', f.Cd, f.Cd.woo_type())
})
