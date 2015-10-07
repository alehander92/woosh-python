import curses
import woosh.prompt
import woosh.config
import woosh.runner
import woosh.builtin_env
import woosh.completer


def run_loop():
    # todo: add config handling
    # add option for reuse in an editor

    screen = init()

    config = woosh.config.load()
    prompt = woosh.prompt.generate(config['prompt'])
    Shell(screen, prompt, config, woosh.builtin_env.BUILTIN_ENV).run_loop()


class Shell:

    def __init__(self, screen, prompt, config, env):
        self.screen = screen
        self.prompt = prompt
        self.config = config
        self.env = env
        self.runner = woosh.runner.Runner()
        self.init_handlers()

    def init_handlers(self):
        self.handlers = {}

        for s in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'ENTER', 'BACKSPACE', 'HOME', 'END']:
            self.handlers['KEY_%s' % s] = getattr(self, 'read_%s' % s.lower())

        self.handlers[' '] = self.read_space
        self.handlers['\t'] = self.read_tab
        self.handlers['\n'] = self.read_enter
        self.handlers['%'] = self.read_bash
        self.handlers['\\'] = self.read_exit

        for s in range(0, 1024):
            if chr(s) not in self.handlers:
                self.handlers[chr(s)] = self.read_symbol

    def run_loop(self):
        self.real_history = []
        self.line, self.column = 0, 0
        self.z = len(self.prompt)

        self.parallel_history = []

        self.real_history.append('')
        self.screen.addstr(self.prompt)
        self.column = self.z
        self.last_completion_end_line = 0
        self.last_key = None

        self.doctor_who = 0  # doctor who travels thru history
        self.tardis = False  # flag if we are travelling thru paraller history with doctor who
        while True:
            key = self.screen.getkey()
            # self.display(self.handlers[key], 3, 4)
            self.handlers[key](key)
            self.last_key = key

    @property
    def history(self):
        if not self.tardis:
            return self.real_history
        else:
            return self.parallel_history

    @property
    def l(self):
        if not self.tardis:
            return self.real_history[-1]
        else:
            return self.parallel_history[self.doctor_who]

    @l.setter
    def l(self, l):
        if not self.tardis:
            self.real_history[-1] = l
        else:
            self.parallel_history[self.doctor_who] = l

    def display(self, obj, line, column=0):
        self.screen.move(line, column)
        self.screen.addstr(str(obj))
        self.a()

    def read_enter(self, _):
        self.line, self.column = self.line + 1, 0
        self.a()
        y = self.runner.run(self.l, self.env)
        if y:
            self.screen.addstr(str(y) + ' ' * 72)
            self.line, self.column = self.line + 1, 0
            self.a()
            self.screen.addstr(self.prompt)
            self.column = self.z
        else:
            self.screen.addstr(self.prompt)
            self.column = self.z

        self.real_history[-1] = self.l
        self.real_history.append('')
        self.doctor_who = len(self.real_history) - 1
        self.tardis = False

    def read_up(self, _):
        if self.doctor_who == 0:
            return
        if not self.tardis:
            self.tardis = True
            self.parallel_history = self.real_history[:]

        self.doctor_who -= 1
        self.screen.move(self.line, self.z)
        self.screen.addstr(self.history[self.doctor_who])
        self.screen.addstr('        ')
        self.column = len(self.history[self.doctor_who]) + self.z
        self.a()

    def read_down(self, _):
        if self.doctor_who == len(self.history) - 1:
            return
        if not self.tardis:
            self.tardis = True
            self.parallel_history = self.real_history[:]

        self.doctor_who += 1
        self.screen.move(self.line, self.z)
        self.screen.addstr(self.history[self.doctor_who])
        self.screen.addstr('        ')
        self.column = len(self.history[self.doctor_who]) + self.z
        self.a()

    def read_left(self, _):
        if self.column > self.z:
            self.column -= 1
        self.a()

    def read_right(self, _):
        self.column += 1
        self.a()

    def read_space(self, _):
        # match = self.last_history_match(self.history[-1])
        self.column += 1
        if self.column - 1 - self.z < len(self.l):
            self.screen.addstr(
                ' ' + self.l[self.column - 1 - self.z:])
            self.l = self.l[:self.column - 1 - self.z] + \
                ' ' + self.l[self.column - 1 - self.z:]
        else:
            self.screen.addstr(' ')
            self.l += ' '

        # self.screen.addstr(' %s' % match[self.column - self.z:])
        self.a()

    def a(self):
        self.screen.move(self.line, self.column)

    def read_tab(self, _):
        for l in range(self.line + 1, self.last_completion_end_line + 1):
            self.screen.move(l, 0)
            self.screen.clrtoeol()

        if self.last_key == '\t':
            # finds first completion
            if self.completions and self.completions[0]:
                h = self.l.rfind(' ')
                token = self.l[h + 1:]
                self.column = h + self.z + 1
                self.a()
                self.screen.addstr(self.completions[0][0])
                self.l = self.l[:h + 1] + self.completions[0][0]
                self.column = self.z + len(self.l)
                self.a()
                return

        self.completions = woosh.completer.complete(self.l, self.env)
        i = 0

        ex = True
        while ex:
            ex = False
            for j, tab in enumerate(self.completions):
                if len(tab) > i:
                    self.screen.move(self.line + i + 1, j * 48)
                    self.screen.addstr(tab[i])
                    ex = True
            i += 1

        self.last_completion_end_line = i - 1
        self.a()

    def read_exit(self, _):
        exit_woosh(self.screen)

    def read_bash(self, _):
        self.column += 1
        self.screen.addstr('2')

    def read_letter(self, letter):
        self.column += 1

        if self.column - 1 - self.z < len(self.l):
            self.screen.addstr(
                letter + self.l[self.column - 1 - self.z:])
            self.l = self.l[:self.column - 1 - self.z] + \
                letter + self.l[self.column - 1 - self.z:]
        else:
            self.screen.addstr(letter)
            self.l += letter

        # self.screen.addstr(str(self.line) + ' ' + str(self.column))
        self.a()

    def read_backspace(self, _):
        if self.column <= self.z:
            return

        self.column -= 1
        if self.column + 1 - self.z < len(self.l):
            self.a()
            self.screen.addstr(
                self.l[self.column + 1 - self.z:] + ' ')
            self.l = self.l[:self.column - self.z] + \
                self.l[self.column + 1 - self.z:]
            self.a()
        else:
            self.a()
            self.l = self.l[:-1]
            self.screen.addstr(' ')
            self.a()

    def read_end(self, _):
        self.column = self.z + len(self.l)
        self.a()

    def read_home(self, _):
        self.column = self.z
        self.a()

    read_symbol = read_letter


def init():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    return screen


def exit_woosh(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    exit()

# screen = init()
# screen.addstr('hello')
# e = screen.getkey()
# screen.addstr(e)
# screen.move(0, 6)

# f = screen.getkey()
# exit_woosh(screen)
