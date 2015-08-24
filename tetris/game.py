import tetris.gui
import time

class Game:
    def __init__(self):
        self.tick_rate = 1
        self.points = 0
        self.world_width = 13
        self.world_height = 15
        
        self.world = World(self.world_width, self.world_height)
        self.world.add_block(Block([['X', None, None], ['X', 'X', 'X']]))


    def __enter__(self):
        self.gui = tetris.gui.GUI()
        return self

    def run(self):
        self.start = time.time()
        self.last_tick = self.start

        # render once at start
        self.gui.draw_status(None, None)
        self.gui.draw_game(self.world)

        while True:
            action = self.gui.get_input((self.last_tick + self.tick_rate) - time.time())
            if action != None:
                self.gui.status_window.addch(action)
                self.gui.draw_game(self.world)

            if time.time() > (self.last_tick + self.tick_rate):
                self.tick()
            
    def tick(self):
        self.gui.status_window.addch('T')
        self.last_tick = time.time()

        self.points += 1
        self.tick_rate = 0.95 ** self.points

        self.gui.draw_game(self.world)
        self.gui.draw_status(None, None)

    def __exit__(self, exc_type, exc_value, traceback):
        self.gui.destroy()

class World:
    def __init__(self, width, height):
        self.world = [[None for x in range(width)] for x in range(height)]

    def add_block(self, block):
        for (ypos, yline) in enumerate(block.shape):
            for (xpos, xline) in enumerate(yline):
                self.world[block.ypos+ypos][block.xpos+xpos] = block.shape[ypos][xpos]

class Block:
    def __init__(self, shape, xpos=0, ypos=0):
        self.shape = shape
        self.xpos = xpos
        self.ypos = ypos

    def rotate(self):
        self.shape = [[e[len(self.shape[0])-1-i] for e in self.shape] for i in range(len(self.shape[0]))]
