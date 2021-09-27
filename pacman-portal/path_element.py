"""
        Application:    Pac-Man Portal
          File Name:    path_element.py
             Course:    CS 386 Into to Game Design and Production
           Semester:    Spring 20'
           Due Date:    March 11
            Authors:    David Guido   |  Contact: davidguido@litlabproductions.com
                        Josh Maranan  |  Contact:
"""


# Custom data structure to be created alongside the single instance 'Graph' and 'Node' class obj's.
# Path element obj's are created as the a* algorithm parses across path options from enemy --> pac-man
# Provides a way of storing path data for each unique AI enemy without interfering
# with the single instances of: game.graph and game.graph.nodes
class PathElement:

    # Initialize PathElement obj
    def __init__(self, node, prev_path_element, source_node, destination_node):

        self.node = node
        self.prev_path_element = prev_path_element
        self.source_node = source_node
        self.destination_node = destination_node

        self.weight_from_source = 0
        self.distance_to_goal = 0
        self.total_cost = 0
