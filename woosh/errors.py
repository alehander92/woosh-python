class WError(Exception):
    pass


class WrongArgumentTypeError(WError):
    pass


class FunNotFoundException(WError):
    pass
