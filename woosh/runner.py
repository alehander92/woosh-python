import woosh.parser
import woosh.woo_types as w
import woosh.woo_z as z
import woosh.woo_instances as i
from woosh.errors import FunNotFoundException, WError


class Runner:

    def run(self, code, env):
        '''
        return the result of the last expression
        for now work only for one expression, because
        it's only used for terminal one-liners
        '''
        try:
            ast = woosh.parser.parse(code)
        except woosh.parser.WooError as e:
            return i.WooException('Parser error: {0}'.format(str(e)), env['WException'])
        if not ast.fields['expressions']:
            return w.WooNil
        e = ast.fields['expressions'][0]
        try:
            return self.run_node(e, env)
        except WError as e:
            return i.WooException('Code error: {0}'.format(str(e)), env['WException'])

    def run_node(self, node, env):
        fields = node.fields.copy()
        fields['env'] = env
        return getattr(self, 'run_{0}'.format(node.node_type.lower()))(**fields)

    def run_funcall(self, label, args, kwargs, env):
        '''
        fun calls can be 2 kinds
        native fun calls
            ls, cd, help
            they are implemented as python classes and they are just initialized and called
        system fun calls
                git, ps, hg
                they are being called using the system native call for now
        '''
        fun_object = env[label]
        if fun_object is None:
            raise FunNotFoundException("%s not found" % label)

        f = fun_object.code(self.run_list(args, env),
                            self.run_kwargs(kwargs, env))
        return f.call(env)
        # return fun_object.code(self.run_list(args, env),
        # self.run_kwargs(kwargs, env)).call(env)

    def run_int(self, value, env):
        return z.WooInt(value)

    def run_bool(self, value, env):
        return z.WooBool(value)

    def run_path(self, path, env):
        return z.WooPath(path)

    def run_string(self, value, env):
        return z.WooString(value)

    def run_list(self, nodes, env):
        return [self.run_node(node, env) for node in nodes]

    def run_kwargs(self, kwargs, env):
        return {kwarg.fields['label']: self.run_node(kwarg.fields['value'], env) for kwarg in kwargs}
