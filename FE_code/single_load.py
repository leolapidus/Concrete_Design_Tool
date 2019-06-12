"""This module only contains the single load element.

"""

import numpy as np

from FE_code.element import Element

class SingleLoad(Element):
    """Creates a Single Load on the Nodes of the Element
    
    Attributes
    ----------
    node : object `Node`
        object of the class Node
    
    load_type : keyword arguments
        load values on the node
        
    Raises
    ------
    RuntimeError
        setting wrong loads
        
    Examples
    --------
    Create a single load on one Node
        >>> SingleLoadBeam(node, fx=4, fy=5, mz=8)
    """

    def __init__(self, id, node, **load_types):
        """Creates a single load
    
        Parameters
        ----------
        node : object
            object of the class Node
        load_type : keyword arguments
            load values on the node
        
        """
        self.id = id
        self._node = node
        self._fx = load_types.get('fx')
        self._fy = load_types.get('fy')
        self._mz = load_types.get('mz')
       

    @property
    def dofs(self):
        node_id = self._node.id

        return [(node_id, 'u'), (node_id, 'v'), (node_id, 'phi')]

    @property 
    def node_id(self):
        return self._node.id

    def get_load_vector(self):
        """Calculate the local vector of nodal loads
        
        Returns
        -------
        load_vector : array_like
            vector of nodal loads
        """
        fx = self._fx
        fy = self._fy
        mz = self._mz
        load_vector = np.array([fx, fy, mz])
        return load_vector

    def _get_dof_tuple_from_node_id(self, node_id):
        return [(node_id, 'u'), (node_id, 'v'), (node_id, 'phi')]
