import woosh.woo_ast as woo_ast


class Converter(object):

    def convert(self, sexp):
        return self.convert_a(sexp.children)

    def convert_a(self, expressions):
        return woo_ast.Node('Cell', expressions=[self.convert_child(expr.children[0]) for expr in expressions])

    def convert_child(self, child):
        # print(child, child.expr_name, len(child.children))
        # print(child.children[0].expr_name)
        return getattr(self, 'convert_' + child.expr_name)(child)

    def convert_expr(self, expr):
        return self.convert_child(expr.children[0])

    def convert_fun_label(self, m):
        return woo_ast.Node('FunLabel', label=m.text)

    def convert_fun_call(self, sexp):
        return woo_ast.Node('FunCall',
                            label=self.convert_child(
                                sexp.children[0]).fields['label'],
                            args=[self.convert_child(c.children[0].children[
                                                     0]) for c in sexp.children[2]],
                            kwargs=[self.convert_child(c.children[0].children[0]) for c in sexp.children[3]])

    def convert_int(self, sexp):
        return woo_ast.Node('Int', value=int(sexp.text))

    def convert_bool(self, sexp):
        return woo_ast.Node('Bool', value=sexp.text == 'True')

    def convert_path(self, sexp):
        return woo_ast.Node('Path', path=sexp.text)

    def convert_string(self, sexp):
        return woo_ast.Node('String', value=sexp.text[1:-1])

    def convert_kwarg_colon(self, sexp):
        return woo_ast.Node('Kwarg', label=self.convert_child(sexp.children[0]), value=self.convert_child(sexp.children[2]))

    def convert_tf(self, sexp):
        return woo_ast.Node('Kwarg', label=sexp.text[1:], value=woo_ast.Node('Bool', value=True))
