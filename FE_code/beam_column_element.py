"""
BeamColumnElement
================

Module contains a beam column element under bending action and axial forces.
"""

import numpy as np
import numpy.linalg as la
from FE_code.element import Element
from FE_code.node import Node
import scipy


class BeamColumnElement(Element):
    """Two dimensional beam column element.

    Attributes
    ----------
    id : int
        Unique ID of the element
    nodes : array_like
        A list of Nodes on the corners of the element
    E : float
        Young's Modulus
    b : float
        width of element [m]
    h : float
        height of element [m]


    Raises
    ------
    RuntimeError
        if the number of nodes given does not equal 4
    RuntimeError
        if the nodes given are not of class `Node`
    """

    def __init__(self, id, nodes, E, b, h):
        """Creates a new element
        Parameters
        ----------
        id : int
            Unique ID of the element
        nodes : array_like
            A list of Nodes at the corners of the element
        """
        if len(nodes) != 2:
            raise RuntimeError(f'Error in creating a beam column element. Given {len(nodes)} nodes instead of 2 nodes')
        for node in nodes:
            if not isinstance(node, Node):
                raise RuntimeError('Error in creating a beam column element. Nodes must be a list of objects of class Node')
        self.id = id
        self.nodes = nodes
        self._E = E
        self._b = b
        self._h = h
        self.local_internal_forces = list ()
        self.global_internal_forces = list ()
        self.load_elements = list()
        self.bending_reinforcement = list()
        self.shear_reinforcement = list()


    @property
    def E(self):
        return self._E
    @E.setter
    def E(self, value):
        self._E = value

    @property
    def b(self):
        return self._b
    @b.setter
    def b(self, value):
        self._b = value

    @property
    def h(self):
        return self._h
    @h.setter
    def h(self, value):
        self._h = value

   
    def _get_dof_tuple_from_node_id(self, node_id):                                 #Aus Elements uebernommen und ueberschrieben
        return [(node_id, 'u'), (node_id, 'v'), (node_id, 'phi')]


    @property
    def node_coords(self):
        """array_like: nodal coordinates matrix
        """
        node_coords = np.array( [node.coords for node in self.nodes] )
        return node_coords

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



    def calculate_elastic_stiffness_matrix_local(self):                                  
        """Calculate local Stiffness Matrix for one beam column element
        using the Euler Bernoulli theory

        Returns
        -------
        K_e_l : array_like
            local element stiffness matrix
        """
        EA = self._E*self._b*self._h
        EI = self._E*(self._b*self._h**3/12)
        l = self.get_length()
        
        K_e_l = np.array([[EA/l, 0, 0, -EA/l, 0, 0],
                        [0, 12*EI/l**3, -6*EI/l**2, 0, -12*EI/l**3, -6*EI/l**2],
                        [0, -6*EI/l**2, 4*EI/l, 0, 6*EI/l**2, 2*EI/l],
                        [-EA/l, 0, 0, EA/l, 0, 0],
                        [0, -12*EI/l**3, 6*EI/l**2, 0, 12*EI/l**3, 6*EI/l**2],
                        [0, -6*EI/l**2, 2*EI/l, 0, 6*EI/l**2, 4*EI/l]])

        return K_e_l

    def calculate_elastic_stiffness_matrix(self):
        """Calculate Stiffness Matrix for one beam column element
        using the Euler Bernoulli theory

        Returns
        -------
        K_e : array_like
            element stiffness matrix
        """
        transform_matrix = self.get_transform_matrix()
        K_e_l = self.calculate_elastic_stiffness_matrix_local()
        a = np.dot(transform_matrix.T, K_e_l)
        K_e = np.dot(a, transform_matrix)
      #  K_e = transform_matrix.T @ K_e_l @ transform_matrix

        return K_e

    def calculate_element_end_forces(self):
        """Calculate global element end forces of one beam column element
        
        Returns
        -------
        f_g : array_like
            element stiffness matrix
        """
        
        u_g = list()
        for i_node in self.nodes:
            u_g.extend( [ i_node.results['u'], i_node.results['v'], i_node.results['phi'] ] )
        K_g = self.calculate_elastic_stiffness_matrix()
        f_g = np.dot(K_g, u_g)
        return f_g
    
    def calculate_local_element_end_forces(self):
        """Calculate local element end forces of one beam column element
        
        Returns
        -------
        f_l : array_like
            element stiffness matrix
        """

        u_e = list()
        for i_node in self.nodes:
            u_e.extend([i_node.results['u'], i_node.results['v'], i_node.results['phi']])
        transform_matrix = self.get_transform_matrix()
        u_l = np.dot(transform_matrix, u_e)
        K_e_l = self.calculate_elastic_stiffness_matrix_local()
        f_l = np.dot(K_e_l, u_l)
        return f_l

    def reset_design(self):
        self.bending_reinforcement = list()
        self.shear_reinforcement = list()