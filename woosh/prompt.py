import getpass
import platform
import datetime
import subprocess

LOADS = {
    'username': getpass.getuser,
    'host': lambda: '-'.join(platform.node().split('-')[1:]),
    'time': lambda: datetime.datetime.now().strftime('%H:%M'),
    'branch': lambda: subprocess.check_output(['git', 'branch'])
}
# {username}@{host}~{time}


def generate(prompt_config):
    loads = {a: b() for a, b in LOADS.items() if a in prompt_config}
    print(loads, prompt_config)
    return prompt_config.format(**loads)
