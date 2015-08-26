#!/usr/bin/python
# -*- coding: utf-8 -*-

import tetris.gui
import tetris.block
import tetris.world

import time
import random
import copy

class Game:
    def __init__(self):
        self.tick_interval = 1
        self.points = 0

        self.world_width = 14
        self.world_height = 15
        
        self.world = tetris.world.World(self.world_width, self.world_height)

        random.seed(time.time())
        self.block_bag = []

        self.next_block = self.create_random_block()
        self.current_block = None

    def __enter__(self):
        self.gui = tetris.gui.GUI(self.world_width, self.world_height)
        return self

    def create_random_block(self):
        if len(self.block_bag) == 0:
            self.block_bag = copy.copy(tetris.block.blocks)
            random.shuffle(self.block_bag)

        new_block = random.choice(self.block_bag)
        self.block_bag.remove(new_block)
        return tetris.block.Block(new_block, self.world_width / 2 - 2, 0)

    def run(self):
        self.start = time.time()
        self.last_tick = self.start

        # render once at start
        self.gui.draw_status(self.next_block, self.points)
        self.gui.draw_game(self.world, self.current_block)

        while True:
            if self.current_block == None:
                self.current_block = self.next_block
                self.next_block = self.create_random_block()
                self.gui.draw_game(self.world, self.current_block)
                self.gui.draw_status(self.next_block, self.points)

            action = self.gui.get_input((self.last_tick + self.tick_interval) - time.time())

            if action != None:
                if action == Action.rotate:
                    # fix this crap
                    self.current_block.rotate()
                    # if we end up colliding, reverse operation
                    if self.world.collides(self.current_block):
                        self.current_block.rotate()
                        self.current_block.rotate() # :D
                        self.current_block.rotate()

                if action == Action.down:
                    self.tick()

                if action == Action.move_left:
                    self.current_block.xpos -= 1
                    if self.world.collides(self.current_block):
                        self.current_block.xpos += 1

                if action == Action.move_right:
                    self.current_block.xpos += 1
                    if self.world.collides(self.current_block):
                        self.current_block.xpos -= 1

#                self.gui.status_window.addch(action)
                self.gui.draw_game(self.world, self.current_block)

            if time.time() > (self.last_tick + self.tick_interval):
                self.tick()

            while self.world.line_check() is not None:
                self.points += 1
                self.world.remove_line(self.world.line_check())

            if self.world.game_over():
                pass


            
    def tick(self):
#        self.gui.status_window.addch('T')
        self.last_tick = time.time()

        if self.tick_interval <= 0.2:
            self.tick_interval = 0.95 ** self.points

        self.current_block.ypos += 1
        if self.world.collides(self.current_block):
            self.current_block.ypos -= 1
            self.world.add_block(self.current_block)
            self.current_block = None

        self.gui.draw_game(self.world, self.current_block)
        self.gui.draw_status(self.next_block, self.points)

    def __exit__(self, exc_type, exc_value, traceback):
        self.gui.destroy()

class Action:
    rotate = 1
    down = 2
    move_left = 3
    move_right = 4

