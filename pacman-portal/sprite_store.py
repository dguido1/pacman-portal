"""
        Application:    Pac-Man Portal
          File Name:    sprite_store.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

from spritesheet import Spritesheet
import pygame as pg

# Class used for storing and retrieving sprites
class SpriteStore:

    def __init__(self):

        self.sprite_sheet = Spritesheet('images/spritesheet.png')

        self.pacman = self.get_pacman_sprites()
        self.blinky = self.get_blinky_sprites()
        self.pinky = self.get_pinky_sprites()
        self.clyde = self.get_clyde_sprites()
        self.inkey = self.get_inkey_sprites()
        self.portal = self.get_unscaled_portal_sprites()
        self.fruits = self.get_fruit_sprites()
        self.pac_life = self.sprite_sheet.get_image(x=(24 * 2), y=(24 * 3), w=24, h=24)

    # Returns list of (Pac-man) images
    def get_pacman_sprites(self):

        pacman_images = [self.sprite_sheet.get_image(x=(24 * 0), y=(24 * 7), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 2), y=(24 * 3), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 0), y=(24 * 3), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 6), y=(24 * 3), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 4), y=(24 * 3), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 3), y=(24 * 3), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 1), y=(24 * 3), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 7), y=(24 * 3), w=24, h=24),
                         self.sprite_sheet.get_image(x=(24 * 5), y=(24 * 3), w=24, h=24)]

        return pacman_images

    def get_pacman_dying_sprites(self):
        pacman_dying_images = [self.sprite_sheet.get_image(x=(24 * 0), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 3), y=(24 * 3), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 1), y=(24 * 3), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 4), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 5), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 6), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 7), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 8), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 9), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 10), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 11), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 12), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 13), y=(24 * 7), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 14), y=(24 * 7), w=24, h=24),
                               ]
        return pacman_dying_images

    # Returns list of (Inkey) images
    def get_blinky_sprites(self):

        blinky_images = [self.sprite_sheet.get_image(x=(24 * 0), y=(24 * 6), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 1), y=(24 * 6), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 2), y=(24 * 6), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 3), y=(24 * 6), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 4), y=(24 * 6), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 5), y=(24 * 6), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 6), y=(24 * 6), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 7), y=(24 * 6), w=24, h=24)]

        return blinky_images

    # Returns list of (Inkey) images
    def get_pinky_sprites(self):

        pinky_images = [self.sprite_sheet.get_image(x=(24 * 0), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 1), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 2), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 3), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 4), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 5), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 6), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 7), y=(24 * 8), w=24, h=24)]

        return pinky_images

    # Returns list of (Inkey) images
    def get_clyde_sprites(self):

        clyde_images = [self.sprite_sheet.get_image(x=(24 * 0), y=(24 * 9), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 1), y=(24 * 9), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 2), y=(24 * 9), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 3), y=(24 * 9), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 4), y=(24 * 9), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 5), y=(24 * 9), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 6), y=(24 * 9), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 7), y=(24 * 9), w=24, h=24)]

        return clyde_images

    # Returns list of (Inkey) images
    def get_inkey_sprites(self):

        inkey_images = [self.sprite_sheet.get_image(x=(24 * 8), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 9), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 10), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 11), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 12), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 13), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 14), y=(24 * 8), w=24, h=24),
                        self.sprite_sheet.get_image(x=(24 * 15), y=(24 * 8), w=24, h=24)]

        return inkey_images

    def get_ghost_running_away_sprites(self):
        running_away_images = [self.sprite_sheet.get_image(x=(24 * 6), y=(24 * 4), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 7), y=(24 * 4), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 8), y=(24 * 4), w=24, h=24),
                               self.sprite_sheet.get_image(x=(24 * 9), y=(24 * 4), w=24, h=24)]

        return running_away_images
    def get_ghost_eyes_sprites(self):

        eyes_images = [self.sprite_sheet.get_image(x=(24 * 8), y=(24 * 9), w=24, h=24),
                       self.sprite_sheet.get_image(x=(24 * 9), y=(24 * 9), w=24, h=24),
                       self.sprite_sheet.get_image(x=(24 * 10), y=(24 * 9), w=24, h=24),
                       self.sprite_sheet.get_image(x=(24 * 11), y=(24 * 9), w=24, h=24),
                       self.sprite_sheet.get_image(x=(24 * 12), y=(24 * 9), w=24, h=24),
                       self.sprite_sheet.get_image(x=(24 * 13), y=(24 * 9), w=24, h=24),
                       self.sprite_sheet.get_image(x=(24 * 14), y=(24 * 9), w=24, h=24),
                       self.sprite_sheet.get_image(x=(24 * 15), y=(24 * 9), w=24, h=24)
                       ]
        return eyes_images

    def get_numbers(self):
        numbers = [self.sprite_sheet.get_image(x=(24 * 8), y=(24 * 6), w=24, h=24),
                   self.sprite_sheet.get_image(x=(24 * 9), y=(24 * 6), w=24, h=24),
                   self.sprite_sheet.get_image(x=(24 * 10), y=(24 * 6), w=24, h=24),
                   self.sprite_sheet.get_image(x=(24 * 11), y=(24 * 6), w=24, h=24)
                   ]
        return numbers

    # Returns list of unscaled (Portal) images
    def get_unscaled_portal_sprites(self):
        portalsheet = Spritesheet('images/portals.png')
        portal_images_unscaled = [portalsheet.get_image(x=364, y=7, w=177, h=176),
                                  portalsheet.get_image(x=553, y=14, w=163, h=163),
                                  portalsheet.get_image(x=7, y=222, w=161, h=159),
                                  portalsheet.get_image(x=193, y=220, w=155, h=158),
                                  portalsheet.get_image(x=373, y=222, w=159, h=158),
                                  portalsheet.get_image(x=553, y=220, w=163, h=163)]

        return portal_images_unscaled

    def get_fruit_sprites(self):
        spritesheet = Spritesheet('images/spritesheet.png')

        fruit_images = [spritesheet.get_image(x=(24 * 0), y=(24 * 5), w=24, h=24),    # cherries
                        spritesheet.get_image(x=(24 * 1), y=(24 * 5), w=24, h=24),    # strawberry
                        spritesheet.get_image(x=(24 * 2), y=(24 * 5), w=24, h=24),    # orange
                        spritesheet.get_image(x=(24 * 3), y=(24 * 5), w=24, h=24),    # ?????
                        spritesheet.get_image(x=(24 * 4), y=(24 * 5), w=24, h=24),    # apple
                        spritesheet.get_image(x=(24 * 5), y=(24 * 5), w=24, h=24),      # grapes
                        ]

        return fruit_images

    @staticmethod
    def get_small_logo():
        image = pg.image.load('images/logo.png')
        scaled_image = pg.transform.scale(image, (150, 50))
        return scaled_image

    @staticmethod
    def get_bigger_logo():
        image = pg.image.load('images/logo.png')
        scaled_image = pg.transform.scale(image, (450, 200))
        return scaled_image