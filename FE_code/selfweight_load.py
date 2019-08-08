"""This module only contains the selfweight load element.

"""

import numpy as np
import numpy.linalg as la

from FE_code.element import Element

class SelfweightLoad(Element):
    """Creates a Selfweight Load on the Nodes of the Element
    
    Attributes
    ----------
    id : int
        unique ID of the element

    node : object `Node`
        object of the class Node
    
    load_type : keyword arguments
        load values on the node
             
    Examples
    --------
    Create a single load on one Node
        >>> SelfweightLoadBeam(node, fx=4, fy=5, mz=8)
    """

    def __init__(self, id, structural_element, selfweight_load, b, h):
        """Creates a single load
    
        Parameters
        ----------
        id : int
            Unique ID of the element
        structural_element : object
            Beam Column Element
        selfweight load : keyword arguments
            selfweight load on the element
        b :
        h :
        
        """
        self.id = id
        self.structural_element = structural_element
        self._nodes = structural_element.nodes 
        self._selfweight_load = selfweight_load
        self._b = b
        self._h = h
        

    @property
    def node_coords(self):
        """array_like: nodal coordinates matrix
        """
        node_coords = np.array( [node.coords for node in self._nodes] )
        return node_coords

    @property
    def nodal_ids(self):
        ids = [node.id for node in self._nodes]
        return ids

    def get_vector(self):
        """Get vector between the end nodes.
        
        a = Vector of the first node
        b = Vector of the second node
        
        Returns
        -------
        Vector between the end nodes.
        """
        a = self.node_coords[0]
        b = self.node_coords[1]
       
        return b-a

    def get_length(self):
        """Get length between the end nodes.
        
        a = Vector of the first node
        b = Vector of the second node
        
        Returns
        -------
        length of the element.
        """
        a = self.node_coords[0]
        b = self.node_coords[1]

        
        return la.norm(b-a)

    def get_transform_matrix(self):
        """ Transformation matrix.

        Returns
        -------
        transform_matrix: ndarray
            Transformation matrix.
        """

        element_vector = self.get_vector()
        reference_vector = np.array([1, 0])
        dot_product = np.dot(element_vector, reference_vector)
        length = self.get_length()
        
        angle = np.arccos(dot_product/length)

        s = np.sin(angle)
        c = np.cos(angle)

        transform_matrix = np.array([[c, s, 0, 0, 0, 0],
                                    [-s, c, 0, 0, 0, 0],
                                    [0, 0, 1, 0, 0, 0,],
                                    [0, 0, 0, c, s, 0],
                                    [0, 0, 0, -s, c, 0],
                                    [0, 0, 0, 0, 0, 1]])

        
        
        return transform_matrix

    def get_load_vector_local(self):
        """Calculate the local vector of nodal loads
        
        Returns
        -------
        load_vector : array_like
            vector of nodal loads
        """
        
        l = self.get_length()
        angle = self.get_angle()
        g = -1*self._selfweight_load*self._b*self._h
        fx = g*np.sin(angle)*l/2
        fy = g*np.cos(angle)*l/2
        mz = g*l**2*np.cos(angle)/48
        
        load_vector_l = np.array([fx, fy, -mz, fx, fy, mz])

        return load_vector_l
    
    def get_load_vector(self):
        """Calculate the global vector of nodal loads
        
        Returns
        -------
        load_vector : array_like
            vector of nodal loads
        """
        transform_matrix = self.get_transform_matrix()
        load_vector_l = self.get_load_vector_local()
        load_vector = np.dot(transform_matrix.T, load_vector_l)

        return load_vector
    
    @property
    def dofs(self):
        """array_like: dofs of the element as a list of tuples
        """
        dofs = list()
        for node in self._nodes:
            dofs.extend( [(node.id, 'u'), (node.id, 'v'), (node.id, 'phi')] )
        return dofs

    def _get_dof_tuple_from_node_id(self, node_id):
        return [(node_id, 'u'), (node_id, 'v'), (node_id, 'phi')]
