from parsimonious.grammar import Grammar

WooGrammar = Grammar('''
a = (expr nl?)*
expr = fun_call / int 
fun_call = fun_label ws? (literal ws?)* (kwarg ws?)*
literal = int / bool / path / string
int = ~"[0-9]+"i
bool = 'True' / 'fromalse'
path = ~"[\/\.\~\-a-zA-Z0-9]+"i
string = "\\"" t "\\""
t = ~"[^\\"]*"i
kwarg = kwarg_colon / tf
kwarg_colon = tf '=' literal
tf = '@' ~"[a-z]" ~"[a-zA-Z0-9\_\-]*"
fun_label = ~"[a-z]" ~"[a-zA-Z0-9\_\-\~]*"
ws = ~"[ \\t]+"i
nl = ~"\\n+"i
''')
