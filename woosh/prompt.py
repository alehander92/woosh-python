import getpass
import platform
import datetime


def generate():
    return '{0}@{1}~{2} '.format(
        getpass.getuser(),
        platform.node(),
        datetime.datetime.now().strftime('%H:%M'))
