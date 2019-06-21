"""
Model
=====

Module contains a model class for Plates in membrane as well as bending action.
"""

import numpy as np
import numpy.linalg as la
from copy import deepcopy
import matplotlib.pyplot as plt 


from FE_code.node import Node
from FE_code.beam_column_element import BeamColumnElement
from FE_code.single_load import SingleLoad
from FE_code.distributed_load import DistributedLoad
from FE_code.linear_load import LinearLoad
from FE_code.assembler import Assembler
from FE_code.element import Element


class Model:
    """
    Model builds up an object to be used for Finite Element Analysis.

    Parameters
    ----------
    analysis_type : str
        String that holds the analysis type. Use 'membrane' or 'bending' 
        or 'beam'.

    Attributes
    ----------
    nodes : dict
        Dictionary that stores { node_id : node object }
    elements : dict
        Dictionary that stores { element_id : element object }
    dirichlet_conditions : dict
        Dictionary that stores { dof : Dirichlet condition value }
    neumann_conditions : dict
        Dictionary that stores { dof : Neumann condition value }
    postprocessing_done : bool
        flag to tell if the nodal stresses are calculated
    material_parameters_set : bool
        flag to tell if the nodal stresses are set
    """ 

    def __init__(self, analysis_type):
        """
        Create a new model.
        """
        self._assembler = None
        self.postprocessing_done = False
        self.material_parameters_set = False

        # Initialize Attributes
        self._nodes = dict()
        self._elements = dict()
        self.dirichlet_conditions = dict()
        self.neumann_conditions = dict()

        if analysis_type == 'beam':
            self.analysis_type = analysis_type
        else:
            raise ValueError(f'analysis_type: {analysis_type} is undefined')

    def invalidate_assembler(self):
        self._assembler = None

    @property
    def assembler(self):
        if self._assembler is None:
            self._assembler = Assembler(self)
        return self._assembler

    @property
    def nodes(self):
        """array_like: List of all nodes in the model.
        """
        return self._nodes.values()

    def get_node(self, id):
        """Get a node by its ID.

        Parameters
        ----------
        id : int
            ID of the node.

        Returns
        -------
        node : object`Node`
            Node with the given ID.
        """
        return self._nodes[id]

    @property
    def nodal_coordinates(self):
        """Get a list of all nodal coordinates in the model.

        Returns
        -------
        x : array_like
            nodal x-coordinates
        y : array_like
            nodal y-coordinates
        """
        nodes = self.nodes
        coord = list()
        for node in nodes:
            coord.append(node.coords)
        x = np.array([column[0] for column in coord])
        y = np.array([column[1] for column in coord])
        return x, y

    @property
    def elements(self):
        """list of objects`Element`: List of all elements in the model.
        """
        return self._elements.values()

    def get_element(self, id):
        """Get an element by its ID.

        Parameters
        ----------
        id : int
            ID of the element.

        Returns
        -------
        element : object`Element`
            Element with the given ID.
        """
        return self._elements[id]

    # === modeling

    def add_node(self, id, x, y):
        """Add a two dimensional node to the model.

        Parameters
        ----------
        id : int
            Unique ID of the node.
        x : float
            X coordinate.
        y : float
            Y coordinate.

        Raises
        ------
        RuntimeError
            if the model already contains a node with the same id

        Examples
        --------
        Add a node with ID 42:

        >>> model.add_node(id=42, x=5, y=2)
        """
        if id in self._nodes:
            raise RuntimeError(f'The model already contains a node with id {id}')

        self._nodes[id] = Node(id, x, y)

    def add_beam(self, id, node_ids, element_type):
        """Add a two dimentional beam column element to the model.

        Parameters
        ----------
        id : int
            Unique ID of the element.
        nodes : objects`Node`
            nodes cornering the element as objects of the class `Node`
        element_type : string
            a string that holds the element type
        
        Raises
        ------
        RuntimeError
            if the model does not contain a given node id
        RuntimeError
            if the element_type is undefined
        """
        nodes = list()
        for node_id in node_ids:
            if node_id not in self._nodes:
                raise RuntimeError(f'The model does not contain a node with id {node_id}')
            nodes.append(self._nodes[node_id])

        if element_type != 'beam':
            raise NotImplementedError(f'Element type {element_type} is not implemented')
            
        self._elements[id] = BeamColumnElement(id, nodes)
        
    def set_material_parameters(self, E, b, h):
        """
        set the material parameter Young's modulus, thickness and Poissons Ratio

        Parameters
        ----------
        E : float
            Young's modulus
        t : float
            Thickness
        prxy : float
            Poisson's ratio
        """
        for element in self.elements:
            if type(element)==BeamColumnElement:
                element.E = E
                element.b = b
                element.h = h
        self.material_parameters_set = True


    def get_material_parameters(self):
        """
        get the material parameter Young's modulus, thickness and Poissons Ratio

        Returns
        -------
        E : float
            Young's modulus
        t : float
            Thickness
        prxy : float
            Poisson's ratio
        """
        if self.material_parameters_set:
            for element in self.elements:
                if type(element)==BeamColumnElement:
                    E = element.E
                    b = element.b
                    h = element.h
                    return E, b, h


    def add_dirichlet_condition(self, dof, value):
        """Apply a Dirichlet condition to the given degree of freedom

        Parameters
        ----------
        dof : tuple
            (node id, dof str)
        value : float
            value of the Dirichlet condition
        """
        self.dirichlet_conditions[dof] = value


    def reset_dirichlet_conditions(self):
        """
        Resets the Dirichlet conditions
        """
        self.dirichlet_conditions = dict()


    def add_single_load(self, id, node_id, **load_types):
        """Add a single force element to the model.

        Parameters
        ----------
        id : int
            id of the load element
        node_id : int
            id of the applied upon node

        Examples
        --------
        Beam:
        >>> add_single_load(id=58, node_id=1, fx=10, fy=25, mz=36)

        Raises
        ------
        RuntimeError
            if the model already contains an elmement with the same id
        RuntimeError
            if the model does not contain a given node id
        """

        if id in self._elements:
            raise RuntimeError(f'The model already contains an element with id {id}')

        if node_id not in self._nodes:
            raise RuntimeError(f'The model does not contain a node with id {node_id}')
    
        if self.analysis_type=='beam':
            self._elements[id] = SingleLoad(id, self._nodes[node_id], **load_types)
            self.neumann_conditions[id] = self._elements[id]
           
    def add_distributed_load(self, id, structural_element_id, load):
        """Add an element load to the model.

        .. note::
            Currently only applies to loads
            perpendicular to the local z direction of the beam.

        Parameters
        ----------
        id : int
            id of the load element
        structural_element_id : int
            id of the applied upon structural element

        Examples
        --------
        Beam:
        >>> add_element_load(id=25, structural_element_id=7, load=10)
        
        Raises
        ------
        RuntimeError
            if the model already contains an elmement with the same id
        RuntimeError
            if the model does not contain a given node id
        """
        if id in self._elements:
            raise RuntimeError(f'The model already contains an element with id {id}')
        if structural_element_id not in self._elements:
            raise RuntimeError(f'The model does not contain an structural element with id {structural_element_id}')

        structural_element = self.get_element(structural_element_id)
                
        if self.analysis_type=='beam':
            self._elements[id] = DistributedLoad(id, structural_element, load)
            self.neumann_conditions[id] = self._elements[id]
            structural_element.load_elements.append(self._elements[id])
        

    def add_linear_load(self, id, structural_element_id, load_left, load_right):
        """Add an element load to the model.

        .. note::
            Currently only applies to loads
            in local z direction of the beam.

        Parameters
        ----------
        id : int
            id of the load element
        structural_element_id : int
            id of the applied upon structural element

        Examples
        --------
        Beam:
        >>> add_linear_load(id=25, structural_element_id=7, load_left = 5, load_right = 14)
        
        Raises
        ------
        RuntimeError
            if the model already contains an elmement with the same id
        RuntimeError
            if the model does not contain a given node id
        """
        if id in self._elements:
            raise RuntimeError(f'The model already contains an element with id {id}')
        if structural_element_id not in self._elements:
            raise RuntimeError(f'The model does not contain an structural element with id {structural_element_id}')

        structural_element = self.get_element(structural_element_id)
                
        if self.analysis_type=='beam':
            self._elements[id] = LinearLoad(id, structural_element, load_left, load_right)
            self.neumann_conditions[id] = self._elements[id]
            structural_element.load_elements.append(self._elements[id])
    
    def reset_neumann_conditions(self):
        """
        Resets the Neumann conditions
        """
        for element_id, element in list(self._elements.items()):
            if type(element)==SingleLoad or type(element)==DistributedLoad or type(element)==LinearLoad:
                del self._elements[element_id]
    
    def solve(self):
        """Assembles the Linear system of equations `K.u=f` and
        solves it using reduction, and calculates the vector of
        external forces in `model.f` as an array_like
        """
        self.invalidate_assembler()
        assembler = self.assembler

        dof_count = assembler.dof_count     # number of dofs
        
        u = np.zeros(dof_count)

        # Applying Dirichlet boundary conditions
        for dof, value in self.dirichlet_conditions.items():
            index = assembler.index_of_dof(dof)
            u[index] = value
        
        k = np.zeros((dof_count, dof_count))
        f = np.zeros(dof_count)
        
        # Assemble k matrix & f vector
        assembler.assemble_matrix(k, lambda element: element.calculate_elastic_stiffness_matrix())
        assembler.assemble_vector(f, lambda element: element.get_load_vector())

        free_count = assembler.free_dof_count

        # Reduce the system and solve it
        a = k[:free_count, :free_count]
        b = f[:free_count] - k[:free_count, free_count:] @ u[free_count:]
        try: u[:free_count] = la.solve(a, b)
        except np.linalg.LinAlgError as err:
            if 'Singular matrix' in str(err): return 'Singular matrix'
            else: raise
        
              
        # Set displacement as attributes of nodes
        for index in range(len(u)):
            node_id, dof_type = assembler.dof_at_index(index)
            node = self.get_node(node_id)
            node.results[dof_type] = u[index]
        #print("node.results", node.results)

             
    def remove_solution(self):
        self.postprocessing_done = False
        if self.nodes:
            for node in self.nodes:
                node.reset_results()
        #TODO: remove element solution

    def calculate_internal_forces(self):
        """Calculate nodal end forces and saves them in 'node.results['nodal_force']'
        """
        if self.postprocessing_done:
            return

        #lokal nodal force vector
        for ele in self.elements:
            beam_end_forces = ele.calculate_local_element_end_forces()
            if beam_end_forces is not None:
                if len(ele.load_elements) is not 0:
                    if type(ele.load_elements[0])==DistributedLoad:
                        external_forces = ele.load_elements[0].get_load_vector_local()
                    if type(ele.load_elements[0])==LinearLoad:
                        external_forces = ele.load_elements[0].get_load_vector_local()
                else:
                    external_forces = np.array([0, 0, 0, 0, 0, 0])
                internal_forces = beam_end_forces - external_forces
                ele.local_internal_forces = internal_forces
                #print(ele.local_internal_forces)
                
        #global nodal force vector
        for ele in self.elements:
            beam_end_forces = ele.calculate_element_end_forces()

            if beam_end_forces is not None:
                if len(ele.load_elements) is not 0:
                    if type(ele.load_elements[0])==DistributedLoad:
                        external_forces = ele.load_elements[0].get_load_vector()
                    if type(ele.load_elements[0])==LinearLoad:
                        external_forces = ele.load_elements[0].get_load_vector()
                else:
                    external_forces = np.array([0, 0, 0, 0, 0, 0])
                internal_forces = beam_end_forces - external_forces
                ele.global_internal_forces = internal_forces
                #print(ele.global_internal_forces)       
