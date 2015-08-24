import tetris.gui
import tetris.block
import tetris.world

import time

class Game:
    def __init__(self):
        self.tick_interval = 1
        self.points = 0

        self.world_width = 13
        self.world_height = 15
        
        self.world = tetris.world.World(self.world_width, self.world_height)

        self.world.add_block(tetris.block.Block(tetris.block.blocks[0], 0, self.world_height - 5))
        self.world.add_block(tetris.block.Block(tetris.block.blocks[1], 2, self.world_height - 4))

        self.next_block = self.create_random_block()
        self.current_block = None

    def __enter__(self):
        self.gui = tetris.gui.GUI()
        return self

    def create_random_block(self):
        return tetris.block.Block(tetris.block.blocks[1], 3, 3)

    def run(self):
        self.start = time.time()
        self.last_tick = self.start

        # render once at start
        self.gui.draw_status(None, None)
        self.gui.draw_game(self.world, self.current_block)

        while True:
            if self.current_block == None:
                self.current_block = self.next_block
                self.next_block = self.create_random_block()

            action = self.gui.get_input((self.last_tick + self.tick_interval) - time.time())

            if action != None:
                if action == Action.rotate:
                    self.current_block.rotate()

                if action == Action.down:
                    pass

                if action == Action.move_left:
                    self.current_block.xpos -= 1

                if action == Action.move_right:
                    self.current_block.xpos += 1

                self.gui.status_window.addch(action)
                self.gui.draw_game(self.world, self.current_block)

            if time.time() > (self.last_tick + self.tick_interval):
                self.tick()
            
    def tick(self):
        self.gui.status_window.addch('T')
        self.last_tick = time.time()

        #self.points += 1 flyttas till där man ska få poäng

        if self.tick_interval <= 0.2:
            self.tick_interval = 0.95 ** self.points

        if self.current_block.ypos

        self.current_block.ypos+=1

        self.gui.draw_game(self.world, self.current_block)
        self.gui.draw_status(None, None)

    def __exit__(self, exc_type, exc_value, traceback):
        self.gui.destroy()

class Action:
    rotate = 1
    down = 2
    move_left = 3
    move_right = 4
