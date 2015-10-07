import sys
import yaml
import curses

PATH = ".woosh.yaml"

COLORS = {
    'white': curses.COLOR_WHITE,
    'yellow': curses.COLOR_YELLOW,
    'red':   curses.COLOR_RED,
    'green': curses.COLOR_GREEN,
    'blue': curses.COLOR_BLUE,
    'black': curses.COLOR_BLACK,
    'cyan': curses.COLOR_CYAN,
    'orange': 208,
    'pink': 201,
    'default': 0,
}

ATTRS = {
    'bold': curses.A_BOLD,
    'normal': curses.A_NORMAL
}


def load():
    with open(PATH, 'r') as f:
        source = f.read()
    init_colors()
    y = yaml.load(source)
    y['prompt'] = {a: (parse_style(b) if a != 'pattern' else b)
                   for i, (a, b) in enumerate(y['prompt'].items())}

    y['style'] = {k: parse_style(v) for k, v in y['style'].items()}
    return y


def init_colors():
    # a = 0  # evil but fix later, init_pair can only init limited number
    for a, (label, color) in enumerate(COLORS.items()):
        if a > 63:
            break
        if color > 7:
            continue
        print(color)
        curses.init_pair(a + 1, color, curses.COLOR_BLACK)
        COLORS[label] = curses.color_pair(a + 1)
    curses.init_pair(17, curses.COLOR_CYAN, curses.COLOR_BLACK)


def parse_style(style):
    if isinstance(style, str):
        return COLORS[style]
    else:
        return ATTRS[style[1]] | COLORS[style[0]]
