"""
Test for load elements
"""

from unittest import TestCase
from numpy.testing import assert_almost_equal
import numpy as np

from FE_code.node import Node
from FE_code.element import Element
from FE_code.single_load_beam import SingleLoadBeam
from FE_code.distributed_load_beam import DistributedLoadBeam

class TestLoadElements(TestCase):
    def setUp(self):
        node = Node(id=1, x=0, y=0)
        self.single_load_beam = SingleLoadBeam(
            id=1,
            node=node,
            #analysis_type='membrane',
            fx=1.,
            fy=2.,
            mz=35
        )

        node1 = Node(id=1, x=0, y=0)
        node2 = Node(id=2, x=1, y=0)
        
        nodes = [node1, node2]
        element = Element()
        element.nodes = nodes
        self.distributed_load_beam = DistributedLoadBeam(
            id=3,
            structural_element=beam,
            distributed_load=10
        )

    def test_dofs(self):
        self.assertEqual(
            self.single_load_beam.dofs,
            [(1, 'u'), (1, 'v'),(1, 'phi')]
        )
        
        self.assertEqual(
            self.surface_load_element.dofs,
            [
                (2, 'u'), (2, 'v'), (2, 'phi'),]
        )

    def test_load_vector(self):
        actual1 = self.single_load_beam.get_load_vector()
        #desired = np.array([1., 2.], dtype=float)
        #assert_almost_equal(actual, desired)
        print(actual1)

        actual2 = self.distributed_load_beam.get_load_vector()
        #desired = np.array([2.5, 0. , 0. , 2.5, 0. , 0. , 2.5, 0. , 0. , 2.5, 0. , 0. ])
        #assert_almost_equal(actual, desired)
