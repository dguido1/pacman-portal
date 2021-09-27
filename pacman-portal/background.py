"""
        Application:    Pac-Man Portal
          File Name:    background.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

import pygame as pg


# Class handling display of maze background
class Background(pg.sprite.Sprite):

    def __init__(self, image_file, location):

        pg.sprite.Sprite.__init__(self)             # Call sprite initializer
        self.image = pg.image.load(image_file)      # Set bg image property to an image file
        self.rect = self.image.get_rect()           # Set bg rect property to the rect of the imported image
        self.rect.left, self.rect.top = location    # Position this (Background) obj
