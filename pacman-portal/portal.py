"""
        Application:    Pac-Man Portal
          File Name:    portal.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

from sprites import Entity


# Portal Class
class Portal(Entity):
    def __init__(self, game, images):
        super().__init__(game=game, images=images)
        self.exists = False
        self.current_node = None
        self.destination_node = None
        self.graph = game.graph
        self.speed = 5
        self.indices = range(6)     # indices are 0 to 5
        self.open = False       # if open for teleporting

    def move(self):
        if self.direction == 'left':
            if self.rect.centerx >= self.destination_node.x:
                self.rect.centerx -= self.speed
            else:
                self.current_node = self.destination_node
                self.open = True

        elif self.direction == 'right':
            if self.rect.centerx <= self.destination_node.x:
                self.rect.centerx += self.speed
            else:
                self.current_node = self.destination_node
                self.open = True

        elif self.direction == 'up':
            if self.rect.centery >= self.destination_node.y:
                self.rect.centery -= self.speed
            else:
                self.current_node = self.destination_node
                self.open = True

        elif self.direction == 'down':
            if self.rect.centery <= self.destination_node.y:
                self.rect.centery += self.speed
            else:
                self.current_node = self.destination_node
                self.open = True

    def fire(self):
        self.game.portal_shoot.set_volume(.4)
        self.game.portal.play(self.game.portal_shoot)
        self.open = False
        self.exists = True
        self.direction = self.game.pacman.direction
        self.current_node = self.game.pacman.next_node
        self.rect.centerx = self.game.pacman.rect.centerx
        self.rect.centery = self.game.pacman.rect.centery

        if self.graph.is_valid_move(self.current_node, self.direction):
            adj_list = self.graph.get_adj_path(self.current_node, self.game.last_key)
            self.next_node = adj_list[len(adj_list) - 1]

        self.destination_node = self.current_node

    def draw(self, indices):        # overwrite for ghost because more animations (e.g. blue/white or just eyes)
        self.screen.blit(self.images[indices[self.game.portal_img_index.frame_index()]], self.rect)

    def update(self):
        if not self.exists:
            pass
        else:
            self.move()
            self.draw(self.indices)
