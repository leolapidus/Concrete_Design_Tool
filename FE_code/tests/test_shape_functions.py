"""
Test for shape functions
"""

from unittest import TestCase
from numpy.testing import assert_almost_equal
import numpy as np

from FE_code.node import Node
from FE_code.element import Element

class TestShapeFunctions(TestCase):
    def setUp(self):
        node1 = Node(id=1, x=0, y=0)
        node2 = Node(id=2, x=1, y=0)
        node3 = Node(id=3, x=1, y=1)
        node4 = Node(id=4, x=0, y=1)
        nodes = [node1, node2, node3, node4]
        self.element = Element()
        self.element.nodes = nodes

    def test_shape_functions(self):
        sf_actual = self.element.calculate_shape_functions(-0.577350269189626, -0.577350269189626)
        sf_desired = np.array([0.62201, 0.16667, 0.04466, 0.16667])
        assert_almost_equal(sf_actual, sf_desired, decimal=5)

    def test_shape_function_derivatives(self):
        dsf_actual = self.element.calculate_shapefunctions_derivatives(-0.577350269189626, -0.577350269189626)
        dsf_desired = np.array(
            [[-0.39434,  0.39434,  0.10566, -0.10566],
            [-0.39434, -0.10566,  0.10566,  0.39434]]
        )
        assert_almost_equal(dsf_actual, dsf_desired, decimal=5)
    
    def test_jacobian(self):
        j_actual = self.element._calculate_Jacobian(-0.577350269189626, -0.577350269189626)
        j_desired = np.array(
            [[0.5, 0.],
            [0., 0.5]]
        )
        assert_almost_equal(j_actual, j_desired, decimal=5)
