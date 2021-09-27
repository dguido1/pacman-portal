"""
        Application:    Pac-Man Portal
          File Name:    node.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

import pygame as pg
from pygame.sprite import Sprite

YELLOW = (255, 255, 0)


# Node class, defines each unit of graph
class Node(Sprite):

    # Initialize node
    def __init__(self, game, x, y, adj=None, adjw=[]):

        super().__init__()
        self.screen = game.screen
        self.x, self.y = x, y + 60       # center coordinates!
        self.adj = adj
        self.adjw = adjw
        self.rect = pg.Rect(self.x, self.y, 1, 1)
        self.game = game

        self.exists = True

    # Update node
    def update(self, kind):

        self.draw(kind=kind)
        self.rect = pg.Rect(self.x, self.y, 3, 3)

    # Draw node to the screen
    def draw(self, kind):                                                               # kind
        if kind == 'pe':                                                                # draw pellet
            pg.draw.circle(self.screen, YELLOW, (self.x, self.y), 3)
        elif kind == 'pp':                                                              # draw power pellet
            pg.draw.circle(self.screen, YELLOW, (self.x, self.y), 6)
        elif kind == 'no':                                                              # draw node
            pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(self.x, self.y, 3, 3))

