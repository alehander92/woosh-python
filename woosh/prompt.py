import getpass
import platform
import datetime


def generate():
    return '{0}@{1}~{2} '.format(
        getpass.getuser(),
        '-'.join(platform.node().split('-')[1:]),
        datetime.datetime.now().strftime('%H:%M'))
