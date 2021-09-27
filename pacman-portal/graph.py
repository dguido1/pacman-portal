"""
        Application:    Pac-Man Portal
          File Name:    graph.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""

from node import Node
from path_element import PathElement
import math
from sprite_store import SpriteStore


# Graph class, defines full graph map of nodes
class Graph:

    # Initialize graph
    def __init__(self, game):

        self.game = game
        self.screen = self.game.screen

        self.nodes = []  # Normal nodes
        self.ghost_nodes = []
        self.special_nodes = []  # Special case nodes
        # i.e.) 0: Inkey start node

        self.pellets = []

        self.power_pellets = []

        self.fruits = self.game.sprite_store.get_fruit_sprites()       # list of 6 fruits [0] ~ [5]
        self.fruits_rect = self.fruits[0].get_rect()
        self.fruits_rect.centerx = 225
        self.fruits_rect.centery = 441

        self.fruit_exists = False
        self.fruit_index = 0

        self.initialize_pellets()
        self.initialize_power_pellets()

        self.initialize_nodes()
        self.initialize_ghosts_room()
        # Set an adjacent weight for all 'n' nodes and 'i' adj_idx in self.nodes[n].adjw[i]
        self.initialize_adj_weight()

        self.initialize_special_nodes()

    # Update graph
    def update(self):

        # for node in self.nodes:  # Update nodes
        #     node.update(kind='no')

        for special_node in self.special_nodes:  # Update nodes
            special_node.update(kind=None)

        for pellet in self.pellets:
            pellet.draw(kind='pe')

        for power_pellet in self.power_pellets:
            power_pellet.draw(kind='pp')

        # spawn fruit when pellets threshold reached
        self.spawn_fruit()

        if self.fruit_exists:
            self.draw_fruit()

    def spawn_fruit(self):
        if (len(self.pellets) + len(self.power_pellets)) == 170:
            self.fruit_index = 0
            self.fruit_exists = True
        elif (len(self.pellets) + len(self.power_pellets)) == 140 and not self.fruit_exists:
            self.fruit_index = 1
            self.fruit_exists = True
        elif (len(self.pellets) + len(self.power_pellets)) == 110 and not self.fruit_exists:
            self.fruit_index = 2
            self.fruit_exists = True
        elif (len(self.pellets) + len(self.power_pellets)) == 80 and not self.fruit_exists:
            self.fruit_index = 3
            self.fruit_exists = True
        elif (len(self.pellets) + len(self.power_pellets)) == 50 and not self.fruit_exists:
            self.fruit_index = 4
            self.fruit_exists = True
        elif (len(self.pellets) + len(self.power_pellets)) == 20 and not self.fruit_exists:
            self.fruit_index = 5
            self.fruit_exists = True

    def draw_fruit(self):
        self.screen.blit(self.fruits[self.fruit_index], self.fruits_rect)

    # Initialize nodes in graph
    # Weight initialization removed from this function.
    # self.initialize_adj_weights() is now called in self.__init__()
    def initialize_nodes(self):

        # [0] ~ [5]
        self.nodes.append(Node(self, x=22, y=24, adj=[1, 6]))
        self.nodes.append(Node(self, x=105, y=24, adj=[0, 2, 7]))
        self.nodes.append(Node(self, x=200, y=24, adj=[1, 9]))
        self.nodes.append(Node(self, x=250, y=24, adj=[4, 10]))
        self.nodes.append(Node(self, x=348, y=24, adj=[3, 5, 12]))
        self.nodes.append(Node(self, x=426, y=24, adj=[4, 13],))

        # [6] ~ [13]
        self.nodes.append(Node(self, x=22, y=89, adj=[0, 7, 14]))
        self.nodes.append(Node(self, x=105, y=89, adj=[1, 6, 8, 15]))
        self.nodes.append(Node(self, x=153, y=89, adj=[7, 9, 16]))
        self.nodes.append(Node(self, x=200, y=89, adj=[2, 8, 10]))
        self.nodes.append(Node(self, x=250, y=89, adj=[3, 9, 11]))
        self.nodes.append(Node(self, x=298, y=89, adj=[10, 12, 19]))
        self.nodes.append(Node(self, x=348, y=89, adj=[4, 11, 13, 20]))
        self.nodes.append(Node(self, x=426, y=89, adj=[5, 12, 21]))

        # [14] ~ [21]
        self.nodes.append(Node(self, x=22, y=138, adj=[6, 15]))
        self.nodes.append(Node(self, x=105, y=138, adj=[7, 14, 26]))
        self.nodes.append(Node(self, x=153, y=138, adj=[8, 17]))
        self.nodes.append(Node(self, x=200, y=138, adj=[16, 23]))
        self.nodes.append(Node(self, x=250, y=138, adj=[19, 24]))
        self.nodes.append(Node(self, x=298, y=138, adj=[11, 18]))
        self.nodes.append(Node(self, x=348, y=138, adj=[12, 21, 29]))
        self.nodes.append(Node(self, x=426, y=138, adj=[13, 20]))

        # [22] ~ [25]
        self.nodes.append(Node(self, x=153, y=188, adj=[23, 27]))
        # self.nodes.append(Node(self, x=200, y=188, adj=[17, 22, 69]))
        # self.nodes.append(Node(self, x=250, y=188, adj=[18, 25, 69]))
        self.nodes.append(Node(self, x=200, y=188, adj=[17, 22, 24]))
        self.nodes.append(Node(self, x=250, y=188, adj=[18, 23, 25]))
        self.nodes.append(Node(self, x=298, y=188, adj=[24, 28]))

        # [26] ~ [29]N==> REMOVED 29 *TEMP*
        self.nodes.append(Node(self, x=105, y=235, adj=[15, 27, 33]))      # [26] special case -- path to [29] => REMOVED 29 FROM ADJ
        self.nodes.append(Node(self, x=153, y=235, adj=[22, 26, 30]))
        self.nodes.append(Node(self, x=298, y=235, adj=[25, 29, 31]))
        self.nodes.append(Node(self, x=348, y=235, adj=[20, 28, 38]))      # [29] special case -- path to [26] => REMOVED 26 FROM ADJ

        # [30] ~ [31]
        self.nodes.append(Node(self, x=153, y=283, adj=[27, 31, 34]))
        self.nodes.append(Node(self, x=298, y=283, adj=[28, 30, 37]))

        # [32] ~ [39]
        self.nodes.append(Node(self, x=22, y=334, adj=[33, 40]))
        self.nodes.append(Node(self, x=105, y=334, adj=[26, 32, 34, 42]))
        self.nodes.append(Node(self, x=153, y=334, adj=[30, 33, 35]))
        self.nodes.append(Node(self, x=200, y=334, adj=[34, 44]))
        self.nodes.append(Node(self, x=250, y=334, adj=[37, 45]))
        self.nodes.append(Node(self, x=298, y=334, adj=[31, 36, 38]))
        self.nodes.append(Node(self, x=348, y=334, adj=[29, 37, 39, 47]))
        self.nodes.append(Node(self, x=426, y=334, adj=[38, 49]))

        # [40] ~ [49]
        self.nodes.append(Node(self, x=22, y=381, adj=[32, 41]))
        self.nodes.append(Node(self, x=56, y=381, adj=[40, 51]))
        self.nodes.append(Node(self, x=105, y=381, adj=[33, 43, 52]))
        self.nodes.append(Node(self, x=153, y=381, adj=[42, 44, 53]))
        self.nodes.append(Node(self, x=200, y=381, adj=[35, 43, 65]))
        self.nodes.append(Node(self, x=250, y=381, adj=[36, 46, 65]))
        self.nodes.append(Node(self, x=298, y=381, adj=[45, 47, 56]))
        self.nodes.append(Node(self, x=348, y=381, adj=[38, 46, 57]))
        self.nodes.append(Node(self, x=395, y=381, adj=[49, 58]))
        self.nodes.append(Node(self, x=426, y=381, adj=[39, 48]))

        # [50] ~ [59]
        self.nodes.append(Node(self, x=22, y=430, adj=[51, 60]))
        self.nodes.append(Node(self, x=56, y=430, adj=[41, 50, 52]))
        self.nodes.append(Node(self, x=105, y=430, adj=[42, 51]))
        self.nodes.append(Node(self, x=153, y=430, adj=[43, 54]))
        self.nodes.append(Node(self, x=200, y=430, adj=[53, 61]))
        self.nodes.append(Node(self, x=250, y=430, adj=[56, 62]))
        self.nodes.append(Node(self, x=298, y=430, adj=[46, 55]))
        self.nodes.append(Node(self, x=348, y=430, adj=[47, 58]))
        self.nodes.append(Node(self, x=395, y=430, adj=[48, 57, 59]))
        self.nodes.append(Node(self, x=426, y=430, adj=[58, 63]))

        # [60] ~ [63]
        self.nodes.append(Node(self, x=22, y=478, adj=[50, 61]))
        self.nodes.append(Node(self, x=200, y=478, adj=[54, 60, 62]))
        self.nodes.append(Node(self, x=250, y=478, adj=[55, 61, 63]))
        self.nodes.append(Node(self, x=426, y=478, adj=[59, 62]))

        # [64] SPECIAL CASE == RETURN FALSE WITH THIS NODE
        self.nodes.append(Node(self, x=0, y=0, adj=[]))

        # [65] SPECIAL CASE -- STARTING NODE (between 44 and 45) -- don't forget to change [44] and [45] adj and adjw!!!
        self.nodes.append(Node(self, x=225, y=381, adj=[44, 45]))

        # Room nodes:
        # [66] Left
        self.nodes.append(Node(self, x=200, y=235, adj=[67]))

        # [67] Center
        self.nodes.append(Node(self, x=225, y=235, adj=[66, 68, 69]))

        # [68] Right
        self.nodes.append(Node(self, x=250, y=235, adj=[67]))

        # [69] Top
        self.nodes.append(Node(self, x=225, y=188, adj=[23, 24]))



    # Set node.adjw value for all 'n' nodes in self.nodes
    def initialize_adj_weight(self):

        # 1. Go through each nodes[n] node element, for 'n' number of nodes on graph
        #   2. Go through 'i' number of adj_node_idx in nodes[n]:
        #       3. Set nodes[n].adjw[i] matching the distance from:
        #           a. nodes[n].x to nodes[nodes[n].adj[i]].x   *(if distance between node and adj node is horizontal)
        #               or:
        #           b. nodes[n].y to nodes[nodes[n].adj[i]].y   *(if distance between node and adj node iis vertical)

        for node in self.nodes:

            #print('\n\nCurrent Node: ' + str(self.nodes.index(node)) + '\nAdjacent Nodes: ')
            adj_idx = 0

            for adj_node_idx in node.adj:                         # graph.node idx to get array spot in unit nodes list

                if node.x == self.nodes[adj_node_idx].x:  # x is the same, weight is in vertical direction
                    # print('\nAdj Node: ' + str(adj_node_idx)
                    # + ', Weight: ' + str(abs(self.nodes[adj_node_idx].y - node.y)))
                    # print('x is the same, weight is in vertical direction')

                    weight = abs(self.nodes[adj_node_idx].y - node.y)
                    node.adjw.append(weight)
                    # node.adjw[adj_idx] = abs(self.nodes[adj_node_idx].y - node.y)

                elif node.y == self.nodes[adj_node_idx].y:  # y is the same, weight is in horizontal direction
                    # node.adjw[adj_idx] = abs(self.nodes[adj_node_idx].x - node.x)
                    # print('\nAdj Node: ' + str(self.nodes.index(adj_node_idx))
                    # + ', Weight: ' + str(node.adjw[adj_idx]))
                    # print('\nAdj Node: ' + str(adj_node_idx)
                    # + ', Weight: ' + str(abs(self.nodes[adj_node_idx].x - node.x)))
                    # print('y is the same, weight is in horizontal direction')

                    weight = abs(self.nodes[adj_node_idx].x - node.x)
                    node.adjw.append(weight)

                adj_idx += 1

    # Initialize special case nodes in graph
    def initialize_special_nodes(self):
        self.special_nodes.append(Node(self, x=225, y=188, adj=[22, 24], adjw=[25, 25]))

    def initialize_pellets(self):

        # horizontal                                      # corresponding graph nodes
        self.pellets.append(Node(self, x=22, y=24))  # [0]

        self.pellets.append(Node(self, x=42, y=24))
        self.pellets.append(Node(self, x=62, y=24))
        self.pellets.append(Node(self, x=82, y=24))

        self.pellets.append(Node(self, x=105, y=24))  # [1]

        self.pellets.append(Node(self, x=125, y=24))
        self.pellets.append(Node(self, x=145, y=24))
        self.pellets.append(Node(self, x=165, y=24))
        self.pellets.append(Node(self, x=185, y=24))

        self.pellets.append(Node(self, x=200, y=24))  # [2]
        self.pellets.append(Node(self, x=250, y=24))  # [3]

        self.pellets.append(Node(self, x=270, y=24))
        self.pellets.append(Node(self, x=290, y=24))
        self.pellets.append(Node(self, x=310, y=24))
        self.pellets.append(Node(self, x=330, y=24))

        self.pellets.append(Node(self, x=348, y=24))  # [4]

        self.pellets.append(Node(self, x=368, y=24))
        self.pellets.append(Node(self, x=388, y=24))
        self.pellets.append(Node(self, x=408, y=24))

        self.pellets.append(Node(self, x=426, y=24))  # [5]

        self.pellets.append(Node(self, x=22, y=89))  # [6]

        self.pellets.append(Node(self, x=42, y=89))
        self.pellets.append(Node(self, x=62, y=89))
        self.pellets.append(Node(self, x=82, y=89))

        self.pellets.append(Node(self, x=105, y=89))  # [7]

        self.pellets.append(Node(self, x=125, y=89))

        self.pellets.append(Node(self, x=153, y=89))  # [8]

        self.pellets.append(Node(self, x=173, y=89))

        self.pellets.append(Node(self, x=200, y=89))  # [9]

        self.pellets.append(Node(self, x=220, y=89))

        self.pellets.append(Node(self, x=250, y=89))  # [10]

        self.pellets.append(Node(self, x=270, y=89))

        self.pellets.append(Node(self, x=298, y=89))  # [11]

        self.pellets.append(Node(self, x=318, y=89))

        self.pellets.append(Node(self, x=348, y=89))  # [12]

        self.pellets.append(Node(self, x=368, y=89))
        self.pellets.append(Node(self, x=388, y=89))
        self.pellets.append(Node(self, x=408, y=89))

        self.pellets.append(Node(self, x=426, y=89))  # [13]

        self.pellets.append(Node(self, x=22, y=138))  # [14]

        self.pellets.append(Node(self, x=42, y=138))
        self.pellets.append(Node(self, x=62, y=138))
        self.pellets.append(Node(self, x=82, y=138))

        self.pellets.append(Node(self, x=105, y=138))  # [15]
        self.pellets.append(Node(self, x=153, y=138))  # [16]

        self.pellets.append(Node(self, x=173, y=138))

        self.pellets.append(Node(self, x=200, y=138))  # [17]
        self.pellets.append(Node(self, x=250, y=138))  # [18]

        self.pellets.append(Node(self, x=270, y=138))

        self.pellets.append(Node(self, x=298, y=138))  # [19]
        self.pellets.append(Node(self, x=348, y=138))  # [20]

        self.pellets.append(Node(self, x=368, y=138))
        self.pellets.append(Node(self, x=388, y=138))
        self.pellets.append(Node(self, x=408, y=138))

        self.pellets.append(Node(self, x=426, y=138))  # [21]

        self.pellets.append(Node(self, x=153, y=188))  # [22]

        self.pellets.append(Node(self, x=173, y=188))

        self.pellets.append(Node(self, x=200, y=188))  # [23]

        self.pellets.append(Node(self, x=220, y=188))

        self.pellets.append(Node(self, x=250, y=188))  # [24]

        self.pellets.append(Node(self, x=270, y=188))

        self.pellets.append(Node(self, x=298, y=188))  # [25]

        self.pellets.append(Node(self, x=105, y=235))  # [26]

        self.pellets.append(Node(self, x=125, y=235))

        self.pellets.append(Node(self, x=153, y=235))  # [27]
        self.pellets.append(Node(self, x=298, y=235))  # [28]

        self.pellets.append(Node(self, x=318, y=235))

        self.pellets.append(Node(self, x=348, y=235))  # [29]

        self.pellets.append(Node(self, x=153, y=283))  # [30]

        self.pellets.append(Node(self, x=173, y=283))
        self.pellets.append(Node(self, x=193, y=283))
        self.pellets.append(Node(self, x=213, y=283))
        self.pellets.append(Node(self, x=233, y=283))
        self.pellets.append(Node(self, x=253, y=283))
        self.pellets.append(Node(self, x=273, y=283))

        self.pellets.append(Node(self, x=298, y=283))  # [31]

        self.pellets.append(Node(self, x=22, y=334))  # [32]

        self.pellets.append(Node(self, x=42, y=334))
        self.pellets.append(Node(self, x=62, y=334))
        self.pellets.append(Node(self, x=82, y=334))

        self.pellets.append(Node(self, x=105, y=334))  # [33]

        self.pellets.append(Node(self, x=125, y=334))

        self.pellets.append(Node(self, x=153, y=334))  # [34]

        self.pellets.append(Node(self, x=173, y=334))

        self.pellets.append(Node(self, x=200, y=334))  # [35]
        self.pellets.append(Node(self, x=250, y=334))  # [36]

        self.pellets.append(Node(self, x=270, y=334))

        self.pellets.append(Node(self, x=298, y=334))  # [37]

        self.pellets.append(Node(self, x=318, y=334))

        self.pellets.append(Node(self, x=348, y=334))  # [38]

        self.pellets.append(Node(self, x=368, y=334))
        self.pellets.append(Node(self, x=388, y=334))
        self.pellets.append(Node(self, x=408, y=334))

        self.pellets.append(Node(self, x=426, y=334))  # [39]

        self.pellets.append(Node(self, x=22, y=381))  # [40]
        self.pellets.append(Node(self, x=56, y=381))  # [41]
        self.pellets.append(Node(self, x=105, y=381))  # [42]

        self.pellets.append(Node(self, x=125, y=381))

        self.pellets.append(Node(self, x=153, y=381))  # [43]

        self.pellets.append(Node(self, x=173, y=381))

        self.pellets.append(Node(self, x=200, y=381))  # [44]

        # self.pellets.append(Node(self, x=220, y=381))         # REMOVE -- Pacman starting location

        self.pellets.append(Node(self, x=250, y=381))  # [45]

        self.pellets.append(Node(self, x=270, y=381))

        self.pellets.append(Node(self, x=298, y=381))  # [46]

        self.pellets.append(Node(self, x=318, y=381))

        self.pellets.append(Node(self, x=348, y=381))  # [47]
        self.pellets.append(Node(self, x=395, y=381))  # [48]
        self.pellets.append(Node(self, x=426, y=381))  # [49]

        self.pellets.append(Node(self, x=22, y=430))  # [50]
        self.pellets.append(Node(self, x=56, y=430))  # [51]

        self.pellets.append(Node(self, x=76, y=430))

        self.pellets.append(Node(self, x=105, y=430))  # [52]
        self.pellets.append(Node(self, x=153, y=430))  # [53]

        self.pellets.append(Node(self, x=173, y=430))

        self.pellets.append(Node(self, x=200, y=430))  # [54]
        self.pellets.append(Node(self, x=250, y=430))  # [55]

        self.pellets.append(Node(self, x=270, y=430))

        self.pellets.append(Node(self, x=298, y=430))  # [56]
        self.pellets.append(Node(self, x=348, y=430))  # [57]

        self.pellets.append(Node(self, x=368, y=430))

        self.pellets.append(Node(self, x=395, y=430))  # [58]
        self.pellets.append(Node(self, x=426, y=430))  # [59]

        self.pellets.append(Node(self, x=22, y=478))  # [60]

        self.pellets.append(Node(self, x=42, y=478))
        self.pellets.append(Node(self, x=62, y=478))
        self.pellets.append(Node(self, x=82, y=478))
        self.pellets.append(Node(self, x=102, y=478))
        self.pellets.append(Node(self, x=122, y=478))
        self.pellets.append(Node(self, x=142, y=478))
        self.pellets.append(Node(self, x=162, y=478))
        self.pellets.append(Node(self, x=182, y=478))

        self.pellets.append(Node(self, x=200, y=478))  # [61]

        self.pellets.append(Node(self, x=224, y=478))

        self.pellets.append(Node(self, x=250, y=478))  # [62]

        self.pellets.append(Node(self, x=270, y=478))
        self.pellets.append(Node(self, x=290, y=478))
        self.pellets.append(Node(self, x=310, y=478))
        self.pellets.append(Node(self, x=330, y=478))
        self.pellets.append(Node(self, x=350, y=478))
        self.pellets.append(Node(self, x=370, y=478))
        self.pellets.append(Node(self, x=395, y=478))

        self.pellets.append(Node(self, x=426, y=478))  # [63]

        # vertical                                          # corresponding graph nodes (already included in horizontal
        # self.pellets.append(Node(self, x=22, y=24))       # [0]


        # self.pellets.append(Node(self, x=22, y=89))       # [6]

        self.pellets.append(Node(self, x=22, y=109))

        # self.pellets.append(Node(self, x=22, y=138))      # [14]
        # self.pellets.append(Node(self, x=105, y=24))      # [1]

        self.pellets.append(Node(self, x=105, y=44))
        self.pellets.append(Node(self, x=105, y=64))

        # self.pellets.append(Node(self, x=105, y=89))      # [7]

        self.pellets.append(Node(self, x=105, y=109))

        # self.pellets.append(Node(self, x=105, y=138))     # [15]

        self.pellets.append(Node(self, x=105, y=158))
        self.pellets.append(Node(self, x=105, y=178))
        self.pellets.append(Node(self, x=105, y=198))
        self.pellets.append(Node(self, x=105, y=218))

        # self.pellets.append(Node(self, x=105, y=235))     # [26]

        self.pellets.append(Node(self, x=105, y=255))
        self.pellets.append(Node(self, x=105, y=275))
        self.pellets.append(Node(self, x=105, y=295))
        self.pellets.append(Node(self, x=105, y=315))

        # self.pellets.append(Node(self, x=105, y=334))     # [33]

        self.pellets.append(Node(self, x=105, y=354))

        # self.pellets.append(Node(self, x=105, y=381))     # [42]

        self.pellets.append(Node(self, x=105, y=401))

        # self.pellets.append(Node(self, x=105, y=430))     # [52]
        # self.pellets.append(Node(self, x=200, y=24))      # [2]

        self.pellets.append(Node(self, x=200, y=44))
        self.pellets.append(Node(self, x=200, y=64))

        # self.pellets.append(Node(self, x=200, y=89))      # [9]
        # self.pellets.append(Node(self, x=250, y=24))      # [3]

        self.pellets.append(Node(self, x=250, y=44))
        self.pellets.append(Node(self, x=250, y=64))

        # self.pellets.append(Node(self, x=250, y=89))      # [10]
        # self.pellets.append(Node(self, x=348, y=24))      # [4]

        self.pellets.append(Node(self, x=348, y=44))
        self.pellets.append(Node(self, x=348, y=64))

        # self.pellets.append(Node(self, x=348, y=89))      # [12]

        self.pellets.append(Node(self, x=348, y=109))

        # self.pellets.append(Node(self, x=348, y=138))     # [20]

        self.pellets.append(Node(self, x=348, y=158))
        self.pellets.append(Node(self, x=348, y=178))
        self.pellets.append(Node(self, x=348, y=198))
        self.pellets.append(Node(self, x=348, y=218))

        # self.pellets.append(Node(self, x=348, y=235))     # [29]

        self.pellets.append(Node(self, x=348, y=255))
        self.pellets.append(Node(self, x=348, y=275))
        self.pellets.append(Node(self, x=348, y=295))
        self.pellets.append(Node(self, x=348, y=315))

        # self.pellets.append(Node(self, x=348, y=334))     # [38]

        self.pellets.append(Node(self, x=348, y=354))

        # self.pellets.append(Node(self, x=348, y=381))     # [47]

        self.pellets.append(Node(self, x=348, y=401))

        # self.pellets.append(Node(self, x=348, y=430))     # [57]
        # self.pellets.append(Node(self, x=426, y=24))      # [5]


        # self.pellets.append(Node(self, x=426, y=89))      # [13]

        self.pellets.append(Node(self, x=426, y=109))

        # self.pellets.append(Node(self, x=426, y=138))     # [21]
        # self.pellets.append(Node(self, x=153, y=89))      # [8]

        self.pellets.append(Node(self, x=153, y=109))

        # self.pellets.append(Node(self, x=153, y=138))     # [16]
        # self.pellets.append(Node(self, x=298, y=89))      # [11]

        self.pellets.append(Node(self, x=298, y=109))

        # self.pellets.append(Node(self, x=298, y=138))     # [19]
        # self.pellets.append(Node(self, x=200, y=138))     # [17]

        self.pellets.append(Node(self, x=200, y=158))

        # self.pellets.append(Node(self, x=200, y=188))     # [23]
        # self.pellets.append(Node(self, x=250, y=138))     # [18]

        self.pellets.append(Node(self, x=250, y=158))

        # self.pellets.append(Node(self, x=250, y=188))     # [24]
        # self.pellets.append(Node(self, x=153, y=188))     # [22]

        self.pellets.append(Node(self, x=153, y=208))

        # self.pellets.append(Node(self, x=153, y=235))     # [27]

        self.pellets.append(Node(self, x=153, y=255))

        # self.pellets.append(Node(self, x=153, y=283))     # [30]

        self.pellets.append(Node(self, x=153, y=303))

        # self.pellets.append(Node(self, x=153, y=334))     # [34]
        # self.pellets.append(Node(self, x=298, y=188))     # [25]

        self.pellets.append(Node(self, x=298, y=208))

        # self.pellets.append(Node(self, x=298, y=235))     # [28]

        self.pellets.append(Node(self, x=298, y=255))

        # self.pellets.append(Node(self, x=298, y=283))     # [31]

        self.pellets.append(Node(self, x=298, y=303))

        # self.pellets.append(Node(self, x=298, y=334))     # [37]
        # self.pellets.append(Node(self, x=22, y=334))      # [32]


        # self.pellets.append(Node(self, x=22, y=381))      # [40]
        # self.pellets.append(Node(self, x=200, y=334))     # [35]

        self.pellets.append(Node(self, x=200, y=354))

        # self.pellets.append(Node(self, x=200, y=381))     # [44]
        # self.pellets.append(Node(self, x=250, y=334))     # [36]

        self.pellets.append(Node(self, x=250, y=354))

        # self.pellets.append(Node(self, x=250, y=381))     # [45]
        # self.pellets.append(Node(self, x=426, y=334))     # [39]


        # self.pellets.append(Node(self, x=426, y=381))     # [49]
        # self.pellets.append(Node(self, x=56, y=381))      # [41]

        self.pellets.append(Node(self, x=56, y=401))

        # self.pellets.append(Node(self, x=56, y=430))      # [51]
        # self.pellets.append(Node(self, x=153, y=381))     # [43]

        self.pellets.append(Node(self, x=153, y=401))

        # self.pellets.append(Node(self, x=153, y=430))     # [53]
        # self.pellets.append(Node(self, x=298, y=381))     # [46]

        self.pellets.append(Node(self, x=298, y=401))

        # self.pellets.append(Node(self, x=298, y=430))     # [56]
        # self.pellets.append(Node(self, x=395, y=381))     # [48]

        self.pellets.append(Node(self, x=395, y=401))

        # self.pellets.append(Node(self, x=395, y=430))     # [58]
        # self.pellets.append(Node(self, x=22, y=430))      # [50]

        self.pellets.append(Node(self, x=22, y=450))

        # self.pellets.append(Node(self, x=22, y=478))      # [60]
        # self.pellets.append(Node(self, x=200, y=430))     # [54]

        self.pellets.append(Node(self, x=200, y=450))

        # self.pellets.append(Node(self, x=200, y=478))     # [61]
        # self.pellets.append(Node(self, x=250, y=430))     # [55]

        self.pellets.append(Node(self, x=250, y=450))

        # self.pellets.append(Node(self, x=250, y=478))     # [62]
        # self.pellets.append(Node(self, x=426, y=430))     # [59]

        self.pellets.append(Node(self, x=426, y=450))

        # self.pellets.append(Node(self, x=426, y=478))     # [63]

    def initialize_power_pellets(self):
        self.power_pellets.append(Node(self, x=22, y=54))
        self.power_pellets.append(Node(self, x=22, y=354))
        self.power_pellets.append(Node(self, x=426, y=354))
        self.power_pellets.append(Node(self, x=426, y=54))

    def initialize_ghosts_room(self):
        # SPECIAL CASE -- ghosts' room
        self.ghost_nodes.append(Node(self, x=198, y=237, adj=[67]))       # [0] -- room LEFT
        self.ghost_nodes.append(Node(self, x=225, y=237, adj=[66, 68, 69]))   # [1] -- room CENTER
        self.ghost_nodes.append(Node(self, x=252, y=237, adj=[67]))       # [2] -- room RIGHT
        self.ghost_nodes.append(Node(self, x=225, y=190, adj=[23, 24, 67]))   # [3] -- CORRIDOR

    # Return a direction
    # From (node) to (node)
    def get_direction(self, start_node, end_node):

        found = False

        for adj_idx in start_node.adj:
            if self.nodes.index(end_node) == adj_idx:
                found = True

        if found:
            if start_node.x > end_node.x and start_node.y == end_node.y:
                direction = 'left'
            elif start_node.x < end_node.x and start_node.y == end_node.y:
                direction = 'right'
            elif start_node.y < end_node.y and start_node.x == end_node.x:
                direction = 'down'
            elif start_node.y > end_node.y and start_node.x == end_node.x:
                direction = 'up'
        else:
            return False

        return direction

    # Return if a move is valid
    # From (node) to (direction)
    def is_valid_move(self, node, direction):

        found = False

        current_node = node

        for adj_node in current_node.adj:
            if direction == 'left' and self.nodes[adj_node].x < current_node.x and self.nodes[adj_node].y == current_node.y\
            or direction == 'right' and self.nodes[adj_node].x > current_node.x and self.nodes[adj_node].y == current_node.y\
            or direction == 'up' and self.nodes[adj_node].y < current_node.y and self.nodes[adj_node].x == current_node.x\
            or direction == 'down' and self.nodes[adj_node].y > current_node.y and self.nodes[adj_node].x == current_node.x:
                current_node = self.nodes[adj_node]
                found = True

        return found

    # Return list of adj nodes in param-defined direction
    def get_adj_path(self, node, direction):

        done = False
        found = False

        current_node = node
        matching_nodes = []

        while not done:
            for adj_node in current_node.adj:
                if direction == 'left' and self.nodes[adj_node].x < current_node.x and self.nodes[adj_node].y == current_node.y\
                or direction == 'right' and self.nodes[adj_node].x > current_node.x and self.nodes[adj_node].y == current_node.y\
                or direction == 'up' and self.nodes[adj_node].y < current_node.y and self.nodes[adj_node].x == current_node.x\
                or direction == 'down' and self.nodes[adj_node].y > current_node.y and self.nodes[adj_node].x == current_node.x:

                    current_node = self.nodes[adj_node]
                    matching_nodes.append(current_node)
                    found = True

            if not found:
                done = True    # Cant go any further
            else:
                found = False  # Reset

        return matching_nodes

    # Return a 'buffer' distance depending on
    # the direction the entity is traveling
    def get_map_buffer(self, entity, direction):

        buffer = 10

        buffers = []

        if direction == 'left':
            buffers.append(entity.adj_node.x - buffer)
            buffers.append(entity.adj_node.y)
        elif direction == 'right':
            buffers.append(entity.adj_node.x + buffer)
            buffers.append(entity.adj_node.y)
        elif direction == 'up':
            buffers.append(entity.adj_node.x)
            buffers.append(entity.adj_node.y - buffer)
        elif direction == 'down':
            buffers.append(entity.adj_node.x)
            buffers.append(entity.adj_node.y + buffer)

        return buffers

    # ******************
    # ******* AI *******
    # ******************

    #   A* Aide
    #       Set weight_from_source and total_cost of the node_path_element
    def initialize_path_element(self, node_path_element):

        original_path_element = node_path_element

        distance = 0    # Total weight from node_path_element.node to node_path_element.source_node

        if node_path_element.node is not node_path_element.source_node:     # Not the source node

            #print ('not the source node')

            while node_path_element.node is not node_path_element.source_node:  # Current not to the source yet, keep backing up

                #print('Looping until source is found')
                # Loop through the prev node in paths adj list and find the idx matching current_path_elem.node

                i = 0
                found = False

                for prev_node_idx in node_path_element.prev_path_element.node.adj:
                    #print('\nPrev Node IDX: ' + str(prev_node_idx))

                    if not found:

                        if node_path_element.prev_path_element.node.adj[i] == self.nodes.index(node_path_element.node):  # Adj idx of prev node matching current found
                            distance += node_path_element.prev_path_element.node.adjw[i]                        # Add corresponding adjw (weight) to the dist from source
                            #print('Setting distance to: ' + str(distance))
                            found = True
                        else:
                            i += 1

                temp_path_element = node_path_element
                node_path_element = node_path_element.prev_path_element   # Set current path elem to the previous path pos

        #print('this is the source node')
        # Arrived at the source element (node)
        original_path_element.weight_from_source = distance                                                                     # Set PathElement dist from source to calc weight
        original_path_element.distance_to_goal = self.get_distance(original_path_element.node, original_path_element.destination_node)  # Set PathElement dist from source to calc weight

        # If this is not the destination node
        if not self.nodes.index(original_path_element.node) == self.nodes.index(original_path_element.destination_node):
            original_path_element.total_cost = original_path_element.weight_from_source + original_path_element.distance_to_goal                                                                            # Set PathElement's total distance
        else:
            original_path_element.total_cost = 0                                                                            # Set PathElement's total distance
        return original_path_element

    # Returns distance from starting_node to destination_node
    # Returns sqrt[ (x2-x1)^2 + (y2-y1)^2 ]
    def get_distance(self, starting_node, destination_node):

        # Return distance formula result
        return math.sqrt((math.pow(destination_node.x - starting_node.x, 2))
                         + (math.pow(destination_node.y - starting_node.y, 2)))

    # Loops through list of costs and returns the node with the shortest combined weight cost
    # Should have implemented a queue or stack data structure for O(1) time but this will do
    def get_front_of_queue(self, path_elem_open_list):

        if len(path_elem_open_list) <= 0:       # Empty
            return False

        lowest_cost = 1000     # Set lowest
        front_of_queue = path_elem_open_list[0]
        #print('\nQueue:')

        i = 1

        for path_elem in path_elem_open_list:
            if path_elem.total_cost < lowest_cost:
                lowest_cost = path_elem.total_cost
               # print(str(lowest_cost))
                front_of_queue = path_elem

            #print(str(i) + '.) Node: ' + str(self.nodes.index(path_elem.node)) + ', Weight from source: '
                  #+ str(path_elem.weight_from_source)
                  #+ ', Distance to destination: ' + str(path_elem.distance_to_goal)
                  #+ ', Total cost: ' + str(path_elem.total_cost) + '\n')  # Add to shortest route list
            i += 1
        return front_of_queue

    def weight_from_to(self, start_node, destination_node):

        adj_idx = 0

        for adj_node_idx in start_node.adj:  # graph.node idx to get array spot in unit nodes list

            if adj_node_idx == self.nodes.index(destination_node):  # x is the same, weight is in vertical direction
                # print('\nAdj Node: ' + str(adj_node_idx)
                # + ', Weight: ' + str(abs(self.nodes[adj_node_idx].y - node.y)))
                # print('x is the same, weight is in vertical direction')

                return start_node.adjw[adj_idx]

                # node.adjw[adj_idx] = abs(self.nodes[adj_node_idx].y - node.y)

            adj_idx += 1

    # A* algorithm
    #   Return list of nodes with shortest path to pac-man
    def get_shortest_path(self, starting_node, destination_node):

        #   Uses a 'PathElement' data structure to parse paths more efficiently
        #       ==> PathElement(node, prev_path_element, source_node, destination_node)
        #
        # 1.) open-list consists of nodes that have been visited but not expanded (meaning that successors
        #     have not been explored yet). This is the list of pending tasks.
        #
        # 2.) closed-list consists on nodes that have been visited and expanded (successors
        #     have been explored already and included in the open list, if this was the case)
        #
        # 3.) current_path_element holds the values of the current node being parsed

        # Put node_start in the OPEN list with f(node_start) = h(node_start)
        starting_path_elem = PathElement(starting_node, None, starting_node, destination_node)
        starting_path_elem.prev_path_element = starting_path_elem

        open_list = [starting_path_elem]                            # Open list of path element obj's
        open_list[0] = self.initialize_path_element(open_list[0])   # Initialize: Set distance_from_source & total_cost

        closed_list = []    # Closed list, already expanded

        # While the OPEN list is not empty
        while len(open_list) > 0:

            #    Take from the open list the node with the lowest:
            #       f(node_current) = g(node_current) + h(node_current)
            current_path_elem = self.get_front_of_queue(open_list)                              # Get top priority node
            #print('\nCurrent path element: ' + str(self.nodes.index(current_path_elem.node)))   # from PathElement list

            # Switch it to the closed list.
            closed_list.append(current_path_elem)
            open_list.remove(current_path_elem)

            # If node_current is node_goal we have found the solution
            if current_path_elem.node is destination_node:              # The current node is the destination
                #print('we have arrived')
                shortest_path = []              # List to store path_elements with shortest path

                # Back up until we find the source node
                while current_path_elem is not None \
                        and current_path_elem.node is not current_path_elem.source_node:
                    shortest_path.append(current_path_elem)
                    #print(str(self.nodes.index(current_path_elem.node)) + ' appended to the list')
                    current_path_elem = current_path_elem.prev_path_element

                shortest_path.reverse()     # Now that current_path_elem is the destination node, reverse list.

                return shortest_path        # Return shortest path from (source_node, destination_node)

            # Hold the current adjacent pathfinder elements in a list
            adj_path_elements = []

            # Create list of PathElement obj's for adj nodes
            for adj_node_idx in current_path_elem.node.adj:

                # No need to create a path elem for the start node
                if not adj_node_idx == self.nodes.index(current_path_elem.source_node):
                    path_elem = PathElement(self.nodes[adj_node_idx], current_path_elem,
                                            starting_node, destination_node)
                    self.initialize_path_element(path_elem)
                    adj_path_elements.append(path_elem)
                    #print('\nCreating adj path element at node: ' + str(adj_node_idx))  # Add to shortest route list
                    #print('\nWeight from source: ' + str(path_elem.weight_from_source)
                         # + ', Distance to destination: ' + str(path_elem.distance_to_goal)
                         # + ', Total cost: ' + str(path_elem.total_cost))  # Add to shortest route list

                #else:
                    #print('\n' + str(self.nodes.index(current_path_elem.source_node))
                          #+ ' is the source node, not adding to adj list')  # Add to shortest route list

            # For all the adj PathElement obj's of current_path_elem
            # Generate each nodes adj successors that come after current_path_elem
            for path_elem in adj_path_elements:

                in_open_list = False
                in_closed_list = False
                open_list_pos = 0

                # Check if the current element is is the closed list
                for cl_elem in closed_list:

                    if self.nodes.index(path_elem.node) == self.nodes.index(cl_elem.node):
                        #print(str(self.nodes.index(path_elem.node)) + ' is in the closed list')
                        in_closed_list = True

                # Check if the current element is is the open list
                for ol_elem in open_list:

                    if self.nodes.index(path_elem.node) == self.nodes.index(ol_elem.node):
                        #print(str(self.nodes.index(path_elem.node)) + ' is in the open list')
                        in_open_list = True
                        open_list_pos = open_list.index(ol_elem)        # Set position of our open list match

                # Not in the closed list and not the source node of our path
                if not in_closed_list:

                    #print(str(self.nodes.index(path_elem.node)) + ' is not in the closed list')

                    # Element found in the open list with an element.node idx matching our current adj_path_element
                    if in_open_list:

                        # We found this path_element (node) before.
                        # Check if the new path to it from source element is shorter
                        # than the current path_elem.weight from source
                        if path_elem.weight_from_source < open_list[open_list_pos].weight_from_source:
                            #print(str(self.nodes.index(path_elem.node)) + ' had a weight g weight of'
                                  #+ str(open_list[open_list_pos].weight_from_source) + ' and now has a weight of: '
                                  #+ str(open_list[open_list_pos].weight_from_source))
                            open_list[open_list.index(open_list[open_list_pos])] = path_elem

                        # If not, ignore it.

                    else:
                        #print(str(self.nodes.index(path_elem.node)) + ' is being added to the open list')
                        open_list.append(path_elem)

       # print('no path')

    # For debugging purposes only
    # New initialization was confirmed working
    def test_adj_weights(self):

        for node in self.nodes:

            print('\n\nCurrent Node: ' + str(self.nodes.index(node)) + '\nAdjacent Nodes: ')
            adj_idx = 0

            for adj_node_idx in node.adj:                         # graph.node idx to get array spot in unit nodes list

                print('\nAdj Node: ' + str(adj_node_idx)
                          + ', Weight: ' + str(node.adjw[adj_idx]))

                adj_idx += 1
