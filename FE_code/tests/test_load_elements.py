"""
Test for load elements
"""

from unittest import TestCase
from numpy.testing import assert_almost_equal
import numpy as np

from FE_code.node import Node
from FE_code.element import Element
from FE_code.point_load_element import PointLoadElement
from FE_code.surface_load_element import SurfaceLoadElement

class TestLoadElements(TestCase):
    def setUp(self):
        node = Node(id=1, x=0, y=0)
        self.point_load_element_mem = PointLoadElement(
            id=1,
            node=node,
            analysis_type='membrane',
            fx=1.,
            fy=2.,
        )

        self.point_load_element_ben = PointLoadElement(
            id=2,
            node=node,
            analysis_type='bending',
            fz=1.,
            mx=2.,
            my=3.,
        )

        node1 = Node(id=1, x=0, y=0)
        node2 = Node(id=2, x=1, y=0)
        node3 = Node(id=3, x=1, y=1)
        node4 = Node(id=4, x=0, y=1)
        nodes = [node1, node2, node3, node4]
        element = Element()
        element.nodes = nodes
        self.surface_load_element = SurfaceLoadElement(
            id=3,
            structural_element=element,
            pressure=10
        )

    def test_dofs(self):
        self.assertEqual(
            self.point_load_element_mem.dofs,
            [(1, 'u'), (1, 'v')]
        )
        self.assertEqual(
            self.point_load_element_ben.dofs,
            [(1, 'w'), (1, 'phix'), (1, 'phiy')]
        )
        self.assertEqual(
            self.surface_load_element.dofs,
            [
                (1, 'w'), (1, 'phix'), (1, 'phiy'),
                (2, 'w'), (2, 'phix'), (2, 'phiy'),
                (3, 'w'), (3, 'phix'), (3, 'phiy'),
                (4, 'w'), (4, 'phix'), (4, 'phiy'),
            ]
        )

    def test_load_vector(self):
        actual = self.point_load_element_mem.get_load_vector()
        desired = np.array([1., 2.], dtype=float)
        assert_almost_equal(actual, desired)

        actual = self.point_load_element_ben.get_load_vector()
        desired = np.array([1., 2., 3.], dtype=float)
        assert_almost_equal(actual, desired)

        actual = self.surface_load_element.get_load_vector()
        desired = np.array([2.5, 0. , 0. , 2.5, 0. , 0. , 2.5, 0. , 0. , 2.5, 0. , 0. ])
        assert_almost_equal(actual, desired)
