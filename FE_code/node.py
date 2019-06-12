"""
Node
====

Module contains a 2D node class.
"""

import numpy as np

class Node:
    """Two dimentional Node.
    
    Attributes
    ----------
    id : int
        Unique ID of the node.
    x : float
        X coordinate of the node.
    y : float
        X coordinate of the node.
    results : dict
        dictionary to store nodal results
    """
    
    def __init__(self, id, x, y):
        """Create a new node.

        Parameters
        ----------
        id : int or str
            Unique ID of the node.
        x : float
            Initial X coordinate of the node.
        y : float
            Initial Y coordinate of the node.
        """

        self.id = id
        self._x = x
        self._y = y

        self.results = dict()
        self.force_vectors = dict()
        self.load_element = list()

    @property
    def coords(self):
        """array_like: x and y coordinates of the node"""
        return np.array([self._x, self._y])


    def reset_results(self):
        self.results = dict()
