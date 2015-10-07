import curses
import woosh.prompt
import woosh.runner
import woosh.builtin_env


def run_loop():
    # todo: add config handling
    # add option for reuse in an editor
    screen = init()

    prompt = woosh.prompt.generate()
    Shell(screen, prompt, woosh.builtin_env.BUILTIN_ENV).run_loop()


class Shell:

    def __init__(self, screen, prompt, env):
        self.screen = screen
        self.prompt = prompt
        self.env = env
        self.runner = woosh.runner.Runner()
        self.init_handlers()

    def init_handlers(self):
        self.handlers = {}

        for s in ['UP', 'DOWN', 'LEFT', 'RIGHT', 'ENTER']:
            self.handlers['KEY_%s' % s] = getattr(self, 'read_%s' % s)

        self.handlers[' '] = self.read_space
        self.handlers['\t'] = self.read_tab
        self.handlers['%'] = self.read_bash
        self.handlers['\\'] = self.read_exit

        for s in range(0, 1024):
            if chr(s) not in self.handlers:
                self.handlers[chr(s)] = self.read_symbol

    def run_loop(self):
        self.history = []
        self.line, self.column = 0, 0
        self.z = len(prompt)

        self.history.append('')
        self.screen.addstr(prompt)
        self.y = self.z

        while True:
            key = screen.getkey()

    def read_enter(self):
        self.line, self.column = line + 1, 0
        self.screen.move(self.line, self.column)
        y = self.runner.run(self.history[-1], self.env)
        if y:
            self.screen.addstr(y)
            self.line, self.column = line + 1, 0
            self.screen.move(self.line, self.column)
            self.screen.addstr(prompt)
            self.column = self.z
        else:
            self.screen.addstr(prompt)
            self.column = self.z

        self.history.append('')

    def read_letter(self):
        pass


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
