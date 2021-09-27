"""
        Application:    Pac-Man Portal
          File Name:    enemy.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

from sprites import Entity
from sprite_store import SpriteStore

# Enemy Class
class Enemy(Entity):

    # Initialize enemy
    def __init__(self, game, images, graph):

        super().__init__(game=game, images=images)
        self.moving = False

        self.indices = range(2)
        self.graph = graph

        self.next_node = self.graph.nodes[25]
        self.adj_node = self.graph.nodes[24]

        self.move_count = 0
        self.current_animation = []
        self.is_frame_one = False
        self.go_home = False

        self.direction = 'stop'
        self.move(self.direction)
        self.speed = 2

        sprite_store = SpriteStore()
        self.scatter_images = sprite_store.get_ghost_running_away_sprites()
        self.eyes_images = sprite_store.get_ghost_eyes_sprites()

    # Update enemy
    def update(self):
        self.handle_animation()
        if self.game.has_game_started:
            self.calculate_enemy_movement()

    # Move enemy, used only as ENGINE
    def move(self, direction):

        if direction == 'stop':
            self.moving = False
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

    def calculate_enemy_movement(self):

        # Normal node stopping buffer initialized correctly
        if len(self.graph.get_map_buffer(self, self.direction)) > 0:
            collide_point_x = self.graph.get_map_buffer(self, self.direction)[0]
            collide_point_y = self.graph.get_map_buffer(self, self.direction)[1]
        else:
            collide_point_x = 0
            collide_point_y = 0
            self.direction = 'stop'

        if self.direction == 'stop':
            if self.game.has_game_started:
                shortest_path = self.graph.get_shortest_path(self.current_node, self.game.pacman.adj_node)

                if len(shortest_path) > 0:
                    self.adj_node = shortest_path[0].node
                    self.direction = self.graph.get_direction(self.current_node, self.adj_node)

        else:

            # Collided with normal node
            if self.rect.collidepoint(collide_point_x, collide_point_y):

                # Set current node to the node enemy collided with
                self.current_node = self.adj_node
                shortest_path = self.graph.get_shortest_path(self.current_node, self.game.pacman.adj_node)

                # Uncomment below to see debugging of enemy a* paths returned
                #to_print = '[ '
                #for elem in shortest_path:
                    #to_print += str(self.graph.nodes.index(elem.node))
                    #if shortest_path.index(elem) < len(shortest_path) - 1:
                        #to_print += ', '
                #to_print += ' ]'

                if self.current_node is not self.game.pacman.current_node:
                    if len(shortest_path) > 0:
                        self.adj_node = shortest_path[0].node
                        self.direction = self.graph.get_direction(self.current_node, self.adj_node)
                else:
                    self.direction = 'stop'

                # Uncomment below to see debugging of enemy a* paths returned
                #print('Current Node: ' + str(self.graph.nodes.index(self.current_node)) + ', Adj node: ' + str(self.graph.nodes.index(self.adj_node)) + ', Direction: ' + self.direction)
                #print('Moving toward destination..\n')

            self.move(self.direction)

    # Handle enemy animation
    def handle_animation(self):
        if self.go_home:
            if self.direction == 'left' and self.moving:
                indices = (4, 5)
                self.draw(indices=indices)
                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
            elif self.direction == 'right' and self.moving:
                indices = (0, 1)
                self.draw(indices=indices)
                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
            elif self.direction == 'up' and self.moving:
                indices = (6, 7)
                self.draw(indices=indices)

                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
            elif self.direction == 'down' and self.moving:
                indices = (2, 3)
                self.draw(indices=indices)
                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
        else:
            if self.direction == 'left' and self.moving:
                indices = (4, 5)
                self.draw(indices=indices)
                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
            elif self.direction == 'right' and self.moving:
                indices = (0, 1)
                self.draw(indices=indices)
                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
            elif self.direction == 'up' and self.moving:
                indices = (6, 7)
                self.draw(indices=indices)
                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
            elif self.direction == 'down' and self.moving:
                indices = (2, 3)
                self.draw(indices=indices)
                self.game.last_enemy_img_index = indices[self.game.enemy_img_index.frame_index()]
            else:
                if self.game.last_img_index >= 0 and self.game.last_img_index < len(self.images):
                    self.screen.blit(self.images[self.game.last_img_index], self.rect)
                else:
                    self.screen.blit(self.images[0], self.rect)

    def draw(self, indices):
        if self.game.pacman.op and not self.go_home:
            self.screen.blit(self.scatter_images[self.game.enemy_scatter_index.frame_index()], self.rect)
        elif self.go_home:
            self.screen.blit(self.eyes_images[indices[self.game.enemy_img_index.frame_index()]], self.rect)
        else:
            self.screen.blit(self.images[indices[self.game.enemy_img_index.frame_index()]], self.rect)