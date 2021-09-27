"""
        Application:    Pac-Man Portal
          File Name:    sprites.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:

        Note: Basic idea retrieved from Eric Matthes via github
        https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/#loading-the-first-piece
"""

import pygame as pg


# Sprite sheet Class
class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename)
        pass

    def get_image(self, x, y, w, h):
        image_rect = pg.Rect(x, y, w, h)
        image = pg.Surface(image_rect.size).convert()
        image.blit(self.spritesheet, (0, 0), image_rect)
        image.set_colorkey((0, 0, 0), pg.RLEACCEL)              # colorkey makes black background from sheet invisible
        return image
