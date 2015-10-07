import woosh.env
import woosh.woo_types as woo_types
import woosh.woo_instances as woo_instances
import types

woo_string = woo_types.Base('String')
woo_int = woo_types.Base('Int')
woo_bool = woo_types.Base('Bool')
values = {
    'String': woo_string,
    'Int':    woo_int,
    'Bool':   woo_bool,
    'Path': woo_types.Base('Path')
}

woo_mode = woo_types.Struct(
    'Mode', other=woo_string, group=woo_string, owner=woo_string, other_id=woo_int, group_id=woo_int, owner_id=woo_int)

woo_datetime = woo_types.Struct('Datetime', year=woo_int, month=woo_int,
                                day=woo_int, hour=woo_int, minute=woo_int, second=woo_int)
values.update({
    'Mode': woo_mode,
    'Datetime': woo_datetime
})


values.update({
    'Git': woo_types.Struct('Git sucks', root=values['Path'], ignore=[woo_string])
})

values.update({'Resource': woo_types.Struct('Resource', dir=woo_bool,
                                            mode=woo_mode, count=woo_int,
                                            group=woo_string, owner=woo_string,
                                            size=woo_int, datetime=woo_datetime, path=woo_string)})

values.update({'List': woo_types.List, 'Map': woo_types.Map})

values.update({'DateTime': woo_types.Struct('DateTime', f=woo_int)})
values['List'].methods = {
    '|':    woo_instances.WooFun('|', [],
                                 woo_types.Fun(arg_types=[('self', values['List']), ('transformator', woo_string)],
                                               return_type=woo_types.List(woo_string))),
    '?':    woo_instances.WooFun('?', [],
                                 woo_types.Fun(arg_types=[('self', values['List']), ('check', woo_string)],
                                               return_type=woo_types.List(woo_string))),
    'sort_by': woo_instances.WooFun('?', [],
                                    woo_types.Fun(arg_types=[('self', values['List']), ('cmp', woo_string)],
                                                  return_type=woo_types.List(woo_string))),

    'count': woo_instances.WooFun('?', [],
                                  woo_types.Fun(arg_types=[('self', values['List'])],
                                                return_type=woo_int))
}

values.update({'WException': woo_types.WException()})


def resourse_as_string(s, self):
    return '{0} {1} {2}'.format(self.slots['mode'].as_string(),
                                self.slots['size'].as_string(), self.slots['path'].as_string())


def mode_as_string(s, self):
    return '{0}{1}{2}'.format(self.slots['owner_id'].as_string(),
                              self.slots['group_id'].as_string(),  self.slots['other_id'].as_string())

values['Resource'].slots['as_string'] = types.MethodType(
    resourse_as_string, values['Resource'])

values['Mode'].slots['as_string'] = types.MethodType(
    mode_as_string, values['Resource'])

BUILTIN_ENV = woosh.env.Env(None, values)
