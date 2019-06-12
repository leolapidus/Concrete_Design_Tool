"""
Test for Quadrilateral elements' matrices
"""

from unittest import TestCase
from numpy.testing import assert_almost_equal
import numpy as np

from FE_code.node import Node
from FE_code.beam_column_element import BeamColumnElement

print(TestCase)


class TestQuad(TestCase):
    def setUp(self):
        node1 = Node(id=1, x=0, y=0)
        node2 = Node(id=2, x=1, y=0)
        
        nodes = [node1, node2]
        self.element_beam = BeamColumnElement(id=1, nodes=nodes)
        self.element_beam.E = 12000
        self.element_beam.t = 0.0
        self.element_beam.prxy = 0.0
        self.element_beam.b = 1
        self.element_beam.h = 1
        

    def test_stiffness_beam(self):
        k_actual = self.element_beam.calculate_elastic_stiffness_matrix()
        k_desired = np.array(
            [
                [ 583.33333333,  187.5       , -333.33333333,  -62.5       , -291.66666667,  -187.5       ,   41.66666667,   62.5       ],
                [ 187.5       ,  583.33333333,   62.5       ,   41.66666667, -187.5       ,  -291.66666667,  -62.5       , -333.33333333],
                [-333.33333333,   62.5       ,  583.33333333, -187.5       ,   41.66666667,   -62.5       , -291.66666667,  187.5       ],
                [ -62.5       ,   41.66666667, -187.5       ,  583.33333333,   62.5       ,  -333.33333333,  187.5       , -291.66666667],
                [-291.66666667, -187.5       ,   41.66666667,   62.5       ,  583.33333333,   187.5       , -333.33333333,  -62.5       ],
                [-187.5       , -291.66666667,  -62.5       , -333.33333333,  187.5       ,   583.33333333,   62.5       ,   41.66666667],
                [  41.66666667,  -62.5       , -291.66666667,  187.5       , -333.33333333,    62.5       ,  583.33333333, -187.5       ],
                [  62.5       , -333.33333333,  187.5       , -291.66666667,  -62.5       ,    41.66666667, -187.5       ,  583.33333333]
            ]
        )
        #assert_almost_equal(k_actual, k_desired, decimal=7)
        print(k_actual)
   
