import tetris.gui
import time

class Game:
    def __init__(self):
        self.tick_rate = 1

    def __enter__(self):
        self.gui = tetris.gui.GUI()
        return self

    def run(self):
        self.start = time.time()
        self.last_tick = self.start

        while True:
            action = self.gui.get_input((self.last_tick + self.tick_rate) - time.time())
            if action != None:
                self.gui.status_window.addch(action)
                self.gui.draw_game(None)

            if time.time() > (self.last_tick + self.tick_rate):
                self.gui.status_window.addch('T')
                self.last_tick = time.time()

                self.gui.draw_game(None)
                self.gui.draw_status(None, None)
            


    def __exit__(self, exc_type, exc_value, traceback):
        self.gui.destroy()
