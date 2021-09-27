"""
        Application:    Pac-Man Portal
          File Name:    sprites.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

from abc import ABC, abstractmethod


# Parent (Entity) class for players and enemies
class Entity(ABC):

    def __init__(self, game, images):

        self.game = game
        self.screen = game.screen
        self.images = images
        self.rect = self.images[0].get_rect()

        self.rect.centerx = game.WIDTH / 2      # temporary start location
        self.rect.centery = game.HEIGHT / 2

        self.speed = 2.5
        self.direction = None
        self.graph = None                       # Entity graph

        self.current_node = None                # Entity nodes
        self.next_node = None
        self.adj_node = None

        self.is_alive = True

    @abstractmethod
    def move(self, direction):      # abstract method
        pass

    def draw(self, indices):        # overwrite for ghost because more animations (e.g. blue/white or just eyes)
        self.screen.blit(self.images[indices[self.game.img_index.frame_index()]], self.rect)
