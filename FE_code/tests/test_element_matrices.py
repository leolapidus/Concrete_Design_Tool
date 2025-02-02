"""
Test for Quadrilateral elements' matrices
"""

from unittest import TestCase
from numpy.testing import assert_almost_equal
import numpy as np

from FE_code.node import Node
from FE_code.quad_plate_membrane import QuadPlateMembrane
from FE_code.quad_plate_bending import QuadPlateBending

print(TestCase)


class TestQuad(TestCase):
    def setUp(self):
        node1 = Node(id=1, x=0, y=0)
        node2 = Node(id=2, x=1, y=0)
        node3 = Node(id=3, x=1, y=1)
        node4 = Node(id=4, x=0, y=1)
        nodes = [node1, node2, node3, node4]
        self.element_membrane = QuadPlateMembrane(id=1, nodes=nodes)
        self.element_membrane.E = 12000
        self.element_membrane.t = 0.1
        self.element_membrane.prxy = 0.2
        self.element_bending = QuadPlateBending(id=1, nodes=nodes, reduced_integration=False)
        self.element_bending.E = 12000
        self.element_bending.t = 0.1
        self.element_bending.prxy = 0.2

    def test_stiffness_membrane(self):
        k_actual = self.element_membrane.calculate_elastic_stiffness_matrix()
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
        assert_almost_equal(k_actual, k_desired, decimal=7)
        print(k_actual)

    def test_stiffness_bending_full_integration(self):
        self.element_bending.reduced = False
        k_actual = self.element_bending.calculate_elastic_stiffness_matrix()
        k_desired = np.array(
            [[ 78.74824, -14.67534,  -4.6519 , -34.72222, -54.76911, -17.36111, -69.44444, -27.38455, -17.36111,  25.41843,  -7.33767,  -4.6519 ],
            [-14.67534,   3.58737,   0.15625,  14.67534,  11.2963 ,  -0.05208,   7.33767,   5.54398,  -0.15625,  -7.33767,   1.58535,   0.05208],
            [ -4.6519 ,   0.15625,   3.58737, -17.36111,   0.05208,  11.6088 ,  17.36111,  -0.15625,   5.54398,   4.6519 ,  -0.05208,   1.27285],
            [-34.72222,  14.67534, -17.36111, 199.02954,  54.76911, -64.79255, -94.86288,  27.38455, -64.79255, -69.44444,   7.33767, -17.36111],
            [-54.76911,  11.2963 ,   0.05208,  54.76911,  43.68114,  -0.15625,  27.38455,  21.63224,  -0.05208, -27.38455,   5.54398,   0.15625],
            [-17.36111,  -0.05208,  11.6088 , -64.79255,  -0.15625,  43.68114,  64.79255,   0.05208,  21.31974,  17.36111,   0.15625,   5.54398],
            [-69.44444,   7.33767,  17.36111, -94.86288,  27.38455,  64.79255, 199.02954,  54.76911,  64.79255, -34.72222,  14.67534,  17.36111],
            [-27.38455,   5.54398,  -0.15625,  27.38455,  21.63224,   0.05208,  54.76911,  43.68114,   0.15625, -54.76911,  11.2963 ,  -0.05208],
            [-17.36111,  -0.15625,   5.54398, -64.79255,  -0.05208,  21.31974,  64.79255,   0.15625,  43.68114,  17.36111,   0.05208,  11.6088 ],
            [ 25.41843,  -7.33767,   4.6519 , -69.44444, -27.38455,  17.36111, -34.72222, -54.76911,  17.36111,  78.74824, -14.67534,   4.6519 ],
            [ -7.33767,   1.58535,  -0.05208,   7.33767,   5.54398,   0.15625,  14.67534,  11.2963 ,   0.05208, -14.67534,   3.58737,  -0.15625],
            [ -4.6519 ,   0.05208,   1.27285, -17.36111,   0.15625,   5.54398,  17.36111,  -0.05208,  11.6088 ,   4.6519 ,  -0.15625,   3.58737]]
        )
        assert_almost_equal(k_actual, k_desired, decimal=5)

    def test_stiffness_bending_reduced_integration(self):
        self.element_bending.reduced = True
        k_actual = self.element_bending.calculate_elastic_stiffness_matrix()
        k_desired = np.array(
            [[ 833.33333, -208.33333, -208.33333,    0.     , -208.33333, -208.33333, -833.33333, -208.33333, -208.33333,    0.     , -208.33333, -208.33333],
            [-208.33333,  104.65278,    0.15625,  208.33333,  103.88889,   -0.05208,  208.33333,  103.92361,   -0.15625, -208.33333,  104.20139,    0.05208],
            [-208.33333,    0.15625,  104.65278, -208.33333,    0.05208,  104.20139,  208.33333,   -0.15625,  103.92361,  208.33333,   -0.05208,  103.88889],
            [   0.     ,  208.33333, -208.33333,  833.33333,  208.33333, -208.33333,    0.     ,  208.33333, -208.33333, -833.33333,  208.33333, -208.33333],
            [-208.33333,  103.88889,    0.05208,  208.33333,  104.65278,   -0.15625,  208.33333,  104.20139,   -0.05208, -208.33333,  103.92361,    0.15625],
            [-208.33333,   -0.05208,  104.20139, -208.33333,   -0.15625,  104.65278,  208.33333,    0.05208,  103.88889,  208.33333,    0.15625,  103.92361],
            [-833.33333,  208.33333,  208.33333,    0.     ,  208.33333,  208.33333,  833.33333,  208.33333,  208.33333,    0.     ,  208.33333,  208.33333],
            [-208.33333,  103.92361,   -0.15625,  208.33333,  104.20139,    0.05208,  208.33333,  104.65278,    0.15625, -208.33333,  103.88889,   -0.05208],
            [-208.33333,   -0.15625,  103.92361, -208.33333,   -0.05208,  103.88889,  208.33333,    0.15625,  104.65278,  208.33333,    0.05208,  104.20139],
            [   0.     , -208.33333,  208.33333, -833.33333, -208.33333,  208.33333,    0.     , -208.33333,  208.33333,  833.33333, -208.33333,  208.33333],
            [-208.33333,  104.20139,   -0.05208,  208.33333,  103.92361,    0.15625,  208.33333,  103.88889,    0.05208, -208.33333,  104.65278,   -0.15625],
            [-208.33333,    0.05208,  103.88889, -208.33333,    0.15625,  103.92361,  208.33333,   -0.05208,  104.20139,  208.33333,   -0.15625,  104.65278]]
        )
        assert_almost_equal(k_actual, k_desired, decimal=5)

    def test_extrapolation_matrix(self):
        k_actual = self.element_membrane._calculate_extrapolation_matrix()
        k_desired = np.array(
            [[ 1.86603, -0.5    ,  0.13397, -0.5    ],
            [-0.5    ,  1.86603, -0.5    ,  0.13397],
            [-0.5    ,  0.13397, -0.5    ,  1.86603],
            [ 0.13397, -0.5    ,  1.86603, -0.5    ]]
        )
        assert_almost_equal(k_actual, k_desired, decimal=5)
