"""
Element
=======

This module contains a base class for Structural Elements and Load Elements.
"""

import numpy as np

class Element:
    """A base class for Structural Elements and Load Element
    """

    def __init__(self):
        self.nodes = None


    @property #TODO: move it back and raise here NotImplementedError
    def dofs(self):
        """array_like: dofs of the element as a list of tuples
        """
        dofs = list()
        for node in self.nodes:
            dofs.extend(self._get_dof_tuple_from_node_id(node.id))
        return dofs


    def _get_dof_tuple_from_node_id(self, node_id):
        raise NotImplementedError('Cannot get dof tuple from node id in the Element Base Class!!')
    

    @property
    def node_coords(self):
        """array_like: nodal coordinates matrix
        """
        node_coords = np.array( [node.coords for node in self.nodes] )
        return node_coords

    @property
    def nodal_ids(self):
        ids = np.array([node.id for node in self.nodes])
        return ids


    def calculate_elastic_stiffness_matrix(self):
        return None

    def get_load_vector(self):
        return None

    def calculate_internal_forces(self):
        return None

    def calculate_element_end_forces(self):
        return None

    def calculate_local_element_end_forces(self):
        return None
    
    def load_elements(self):
        return None

   