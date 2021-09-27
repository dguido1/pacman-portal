"""
        Application:    Pac-Man Portal
          File Name:    pacman.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

from sprites import Entity
import pygame as pg
from sprite_store import SpriteStore
import copy

# Pac-man Class
class Pacman(Entity):

    # Initialize pac-man
    def __init__(self, game, images, graph):

        super().__init__(game=game, images=images)
        self.lives = 3
        self.moving = False

        # Player graph
        self.graph = graph

        # Player nodes
        self.current_node = self.graph.nodes[65]
        self.next_node = self.graph.nodes[65]
        self.adj_node = self.graph.nodes[45]

        sprite_store = SpriteStore()
        self.numbers_images = sprite_store.get_numbers()
        self.numbers_rect = self.numbers_images[0].get_rect()
        self.numbers_duration = 3000        # 3 seconds
        self.numbers_start = pg.time.get_ticks()
        self._200 = False
        self.rect_200 = copy.deepcopy(self.numbers_rect)
        self._400 = False
        self.rect_400 = copy.deepcopy(self.numbers_rect)
        self._800 = False
        self.rect_800 = copy.deepcopy(self.numbers_rect)
        self._1600 = False
        self.rect_1600 = copy.deepcopy(self.numbers_rect)

        # Cooldown for teleporting through portals
        self.cd = 1000      # 1000 ms = 1 second
        self.last_tp = pg.time.get_ticks()

        # Switch on when power pellet is eaten
        self.op = False
        self.op_start = pg.time.get_ticks()
        self.op_duration = 8500       # (8.5 seconds based on Google's Pac-Man)
        self.enemies_eaten = 0

        self.speed = 3.5
        self.portal_reset = False

        self.sound = None

        self.direction = 'stop'

        self.elapsed_00 = pg.time.get_ticks()
        self.elapsed_01 = pg.time.get_ticks()

        dying_images = self.game.sprite_store.get_pacman_dying_sprites()
        self.dying_start = pg.time.get_ticks()
        self.dying_index = 0
        self.finished = False       # if animation is finished

        self.dying_U = []
        for img in dying_images:
            temp = pg.transform.rotate(img, 0)
            self.dying_U.append(temp)        # no change -- sprite is initially upwards
        self.dying_L = []
        for img in dying_images:
            temp = pg.transform.rotate(img, 90)
            self.dying_L.append(temp)
        self.dying_D = []
        for img in dying_images:
            temp = pg.transform.rotate(img, 180)
            self.dying_D.append(temp)
        self.dying_R = []
        for img in dying_images:
            temp = pg.transform.rotate(img, 270)
            self.dying_R.append(temp)

    # Update pac-man
    def update(self):

        self.elapsed_00 = pg.time.get_ticks() - self.elapsed_00
        if self.elapsed_00 > 200:  # animate every half second
            self.handle_animation()

        self.elapsed_01 = pg.time.get_ticks() - self.elapsed_01

        if not self.get_enemy_collision():
            self.handle_animation()
            self.calculate_player_movement()
            self.eat()
            self.manage_op()
        else:
            self.die()
            self.game.has_game_started = False
        self.print_scores()

    def die(self):
        self.game.has_game_started = False
        self.game.voice.play(self.game.death_sound)  # play the RIP sound
        last_change = pg.time.get_ticks()
        time_elapsed = abs(last_change - pg.time.get_ticks())
        self.finished = False

        # change frame every 145 ms
        while not self.finished:     # stall for duration of RIP sound, keep updating screen
            if time_elapsed > 75:
                self.dying_index += 1
                last_change = pg.time.get_ticks()

            self.game.process_events()  # Get user input
            self.game.update()  # Update this (Game) instance

            self.graph.update()  # Update (Graph) instance

            self.draw_death()
            self.game.ui_update()
            for enemy in self.game.enemies:  # Update (Enemy) instances
                enemy.update()

            pg.display.update()  # Tell game engine to update this games display

            time_elapsed = abs(last_change - pg.time.get_ticks())

        start = pg.time.get_ticks()
        time_elapsed = abs(start - pg.time.get_ticks())

        while time_elapsed < 2000:      # stall for 2 seconds
            self.game.process_events()  # Get user input
            self.game.update()  # Update this (Game) instance

            self.graph.update()  # Update (Graph) instance

            self.game.ui_update()
            for enemy in self.game.enemies:  # Update (Enemy) instances
                enemy.update()

            pg.display.update()  # Tell game engine to update this games display

            time_elapsed = abs(start - pg.time.get_ticks())

        self.game.new_life = True
        print('new life, lives left: ' + str(self.lives))

        if self.lives <= 0:
            self.game.game_over = True
            print ('game 0ver')

    # Calculate pac-man movement, used only as BRAIN
    def calculate_player_movement(self):

        if self.game.has_game_started:

            # If the player hasn't pressed a key or of pac-man is stopped
            if (self.direction is None or self.direction == 'stop') \
                    and self.graph.is_valid_move(self.current_node, self.game.last_key):

                adj_list = self.graph.get_adj_path(self.current_node, self.game.last_key)
                self.adj_node = adj_list[0]
                self.next_node = adj_list[len(adj_list) - 1]

                if self.graph.is_valid_move(self.current_node, self.game.last_key):
                    self.direction = self.game.last_key
                    self.move(self.direction)

            # Normal input of [L, R, U, D] was made
            elif self.direction == 'left' or self.direction == 'right' \
                    or self.direction == 'up' or self.direction == 'down':

                # Collided with portal
                if self.get_portal_collision() and not self.portal_reset:

                    # if not self.graph.is_valid_move(self.current_node, self.direction):
                    self.teleport(self.get_portal_collision())
                    self.move(self.direction)

                # Not colliding with portal
                else:

                    # Normal node stopping buffer initialized correctly
                    if len(self.graph.get_map_buffer(self, self.direction)) > 0:
                        collide_point_x = self.graph.get_map_buffer(self, self.direction)[0]
                        collide_point_y = self.graph.get_map_buffer(self, self.direction)[1]

                    # Collided with normal node
                    if self.rect.collidepoint(collide_point_x, collide_point_y):

                        self.game.debug_game_state()  # Print debug info

                        # Set portal reset to False
                        if self.portal_reset:
                            self.portal_reset = not self.portal_reset

                        # Set current node to the node pac-man collided with
                        self.current_node = self.adj_node

                        # Valid move in the requested direction
                        if self.graph.is_valid_move(self.current_node, self.game.last_key):
                            #print('\n[CALCULATE MOVEMENT]: ' + self.game.last_key + ' is a VALID request, Move: '
                                  #+ self.game.last_key + '\n')

                            self.direction = self.game.last_key
                            adj_list = self.graph.get_adj_path(self.current_node, self.game.last_key)
                            self.adj_node = adj_list[0]
                            self.next_node = adj_list[len(adj_list) - 1]

                        # Requested movement was invalid
                        # --> Same direction movement is valid
                        elif self.graph.is_valid_move(self.current_node, self.direction):
                            #print('\n[CALCULATE MOVEMENT]: ' + self.game.last_key + ' is an INVALID request, Continue moving: '
                                #+ self.direction + '\n')

                            adj_list = self.graph.get_adj_path(self.current_node, self.direction)
                            self.adj_node = adj_list[0]
                            self.next_node = adj_list[len(adj_list) - 1]
                            self.move(self.direction)

                        # Both requested and same direction movement return invalid
                        else:
                            #print('\n[CALCULATE MOVEMENT]: ' + self.game.last_key + ' is an INVALID request and ' + self.direction
                                  #+ ' is an invalid direction, STOP' + '\n')

                            self.direction = 'stop'
                            self.move(self.direction)

                    # Not colliding with normal node or portals, keep moving
                    else:
                        self.move(self.direction)

    # Move pac-man, used only as ENGINE
    def move(self, direction):

        if direction == 'stop':
            self.moving = False
            self.direction = 'stop'
        else:
            self.moving = True

            if direction == 'left':
                self.rect.centerx -= self.speed
            elif direction == 'right':
                self.rect.centerx += self.speed
            elif direction == 'up':
                self.rect.centery -= self.speed
            elif direction == 'down':
                self.rect.centery += self.speed

    def print_scores(self):
        if self.op:
            if self._200:
                self.screen.blit(self.numbers_images[0], self.rect_200)
            if self._400:
                self.screen.blit(self.numbers_images[1], self.rect_400)
            if self._800:
                self.screen.blit(self.numbers_images[2], self.rect_800)
            if self._1600:
                self.screen.blit(self.numbers_images[3], self.rect_1600)

    def eat(self):
        for pellet in self.graph.pellets:
            if pellet.rect.colliderect(self.rect):
                self.game.score += 10
                self.graph.pellets.remove(pellet)

                # om nom sound
                self.game.eating_sound.set_volume(.4)
                self.game.voice.play(self.game.eating_sound)

        for power_pellet in self.graph.power_pellets:
            if power_pellet.rect.colliderect(self.rect):
                self.game.score += 50
                self.graph.power_pellets.remove(power_pellet)
                self.pp()

                # om nom sound
                self.game.eating_sound.set_volume(.4)
                self.game.voice.play(self.game.eating_sound)
        if self.op:
            for enemy in self.game.enemies:
                if self.rect.colliderect(enemy.rect) and not enemy.go_home:
                    enemy.go_home = True
                    self.enemies_eaten += 1
                    self.game.score += 200 * self.enemies_eaten
                    self.game.eat_ghost_sound.set_volume(.99)
                    self.game.voice.play(self.game.eat_ghost_sound)
                    if self.enemies_eaten == 1:
                        self._200 = True
                        self.rect_200 = copy.deepcopy(enemy.rect)
                    if self.enemies_eaten == 2:
                        self._400 = True
                        self.rect_400 = copy.deepcopy(enemy.rect)
                    if self.enemies_eaten == 3:
                        self._800 = True
                        self.rect_800 = copy.deepcopy(enemy.rect)
                    if self.enemies_eaten == 4:
                        self._1600 = True
                        self.rect_1600 = copy.deepcopy(enemy.rect)
        if not self.graph.pellets and not self.graph.power_pellets:
            self.game.win = True
            print('===\n===\n===\n\nYOU WIN\n\n===\n===\n===')
        if self.graph.fruit_exists and self.graph.fruits_rect.colliderect(self.rect):
            self.graph.fruit_exists = False
            self.game.score += 100 * (self.graph.fruit_index + 1)

            # om nom sound
            self.game.eating_sound.set_volume(.4)
            self.game.voice.play(self.game.eating_sound)

    # In eat() -- Handles when eating power pellets (pp)
    def pp(self):
        self.op_start = pg.time.get_ticks()
        self.op = True

    # In update() -- Manages op timer (8.5 seconds)
    def manage_op(self):
        now = pg.time.get_ticks()
        if abs(self.op_start - now) >= self.op_duration:
            self.op = False
            self.enemies_eaten = 0
            self._200 = False
            self._400 = False
            self._800 = False
            self._1600 = False

        #if self.op:
            #print('Pac-Man is POWERFUL')
        #else:
            #print('Pac-Man is WEAK')

    # Handles collision between pac-man and portals
    def get_portal_collision(self):

        #   If no collision is made between pac-man and portal --> Returns False
        #   If  a collision is made between pac-man and portal --> Return the destination node

        # Has collided with a portal
        if self.game.portal1.open and self.game.portal2.open:

            # Get '(x, y)' value of portal1's current node
            p1_x = self.game.portal1.current_node.x
            p1_y = self.game.portal1.current_node.y

            # Get '(x, y)' value of portal2's current node
            p2_x = self.game.portal2.current_node.x
            p2_y = self.game.portal2.current_node.y

            # Check for collision between pac-man and portal1
            if self.rect.collidepoint(p1_x, p1_y):
                # print('Collided with portal 01')
                return self.game.portal2.current_node

            # Check for collision between pac-man and portal2
            elif self.rect.collidepoint(p2_x, p2_y):
                # print('Collided with portal 02')
                return self.game.portal1.current_node

        # Return False if no collision is made
        return False

    # Handles collision between pac-man and portals
    def get_enemy_collision(self):
        if self.op:
            pass
        else:
            #   If no collision is made between pac-man and portal --> Returns False
            #   If  a collision is made between pac-man and portal --> Return the destination node

            for enemy in self.game.enemies:

                # Get '(x, y)' value of portal1's current node
                p1_x = enemy.current_node.x
                p1_y = enemy.current_node.y

                # Check for collision between pac-man and portal1
                if self.rect.colliderect(enemy.rect) and not enemy.go_home:

                    self.lives -= 1

                    if not self.game.new_life:
                        return True
    # Teleport to a different location
    def teleport(self, destination_node):
        now = pg.time.get_ticks()

        if abs(self.last_tp - now) >= self.cd:      # if cd time is over

            # Set current node to the node pac-man collided with
            self.current_node = destination_node
            self.rect.centerx = destination_node.x
            self.rect.centery = destination_node.y

            # Valid move in the requested direction
            if self.graph.is_valid_move(self.current_node, self.game.last_key):
                self.direction = self.game.last_key
                adj_list = self.graph.get_adj_path(self.current_node, self.game.last_key)
                self.adj_node = adj_list[0]
                self.next_node = adj_list[len(adj_list) - 1]
                print('\n[TELEPORT]: ' + self.game.last_key + ' is a VALID request, Move: ' + self.game.last_key + '\n')
                self.game.tp_sound.set_volume(.99)
                self.game.portal.play(self.game.tp_sound)

            # Requested movement was invalid
            # --> Same direction movement is valid
            elif self.graph.is_valid_move(self.current_node, self.direction):
                adj_list = self.graph.get_adj_path(self.current_node, self.direction)
                self.adj_node = adj_list[0]
                self.next_node = adj_list[len(adj_list) - 1]
                print('\n[TELEPORT]: ' + self.game.last_key + ' is an INVALID request, Continue moving: '
                      + self.direction + '\n')

            # Both requested and same direction movement return invalid
            else:
                print('\n[TELEPORT]: ' + self.game.last_key + ' is an INVALID request and ' + self.direction
                      + ' is an invalid direction, STOP' + '\n')
                self.direction = 'stop'

                # Set portal reset to True
                self.portal_reset = True

        self.last_tp = now

    # Handle pac-man animation
    def handle_animation(self):
        if self.direction == 'left' and self.moving:
            indices = (0, 1, 2)
            self.draw(indices=indices)
            self.game.last_img_index = indices[self.game.img_index.frame_index()]
        elif self.direction == 'right' and self.moving:
            indices = (0, 3, 4)
            self.draw(indices=indices)
            self.game.last_img_index = indices[self.game.img_index.frame_index()]
        elif self.direction == 'up' and self.moving:
            indices = (0, 5, 6)
            self.draw(indices=indices)
            self.game.last_img_index = indices[self.game.img_index.frame_index()]
        elif self.direction == 'down' and self.moving:
            indices = (0, 7, 8)
            self.draw(indices=indices)
            self.game.last_img_index = indices[self.game.img_index.frame_index()]
        else:  # will stop animation when pacman stops moving
            self.screen.blit(self.images[self.game.last_img_index], self.rect)

    def draw_death(self):
        if self.game.last_key == 'left':
            self.screen.blit(self.dying_L[self.dying_index], self.rect)
        elif self.game.last_key == 'right' or self.game.last_key == 'stop':
            self.screen.blit(self.dying_R[self.dying_index], self.rect)
        elif self.game.last_key == 'up':
            self.screen.blit(self.dying_U[self.dying_index], self.rect)
        elif self.game.last_key == 'down':
            self.screen.blit(self.dying_D[self.dying_index], self.rect)

        if self.dying_index == 13:  # dying animation is finished -- reset
            self.dying_index = 0
            self.game.last_img_index = 0
            self.finished = True
