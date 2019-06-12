"""
Test for membrane models
"""

from unittest import TestCase
from numpy.testing import assert_almost_equal
import numpy as np

from FE_code.model import Model

class TestQuad(TestCase):
    def setUp(self):
        model = Model(analysis_type='membrane')
        model.add_node(id=1, x=0.0, y=0.0)
        model.add_node(id=2, x=1.0, y=0.0)
        model.add_node(id=3, x=0.0, y=1.0)
        model.add_node(id=4, x=1.0, y=1.0)
        model.add_quad(id=1, node_ids=[1, 2, 4, 3], element_type='membrane_plane_stress')
        model.set_material_parameters(E=1, t=0.1, prxy=0.2)
        model.add_dirichlet_condition(dof=(1, 'u'), value=0)
        model.add_dirichlet_condition(dof=(1, 'v'), value=0)
        model.add_dirichlet_condition(dof=(2, 'u'), value=1) #non-homogenuous
        model.add_dirichlet_condition(dof=(2, 'v'), value=1) #non-homogenuous
        model.add_dirichlet_condition(dof=(3, 'u'), value=0)
        model.add_dirichlet_condition(dof=(3, 'v'), value=0)
        model.add_single_load(id=2, node_id=4, fx=1.0, fy=1.0)
        self.model = model

    def test_solution(self):
        self.model.remove_solution()
        self.model.solve()
        u_actual = max([node.results['u'] for node in self.model.nodes])
        u_desired = 15.12517780938833
        assert_almost_equal(u_actual, u_desired)

    def test_nodal_stresses(self):
        self.model.remove_solution()
        self.model.solve()
        self.model.calculate_nodal_stresses()

        nxx_actual = [node.results['nxx'] for node in self.model.nodes]
        nxy_actual = [node.results['nxy'] for node in self.model.nodes]
        nyy_actual = [node.results['nyy'] for node in self.model.nodes]

        nxx_desired = np.array([-0.13178,  5.42101, 14.58195, 20.13474])
        nxy_desired = np.array([-1.73757,  8.4564 ,  4.67423, 14.8682 ])
        nyy_desired = np.array([-5.65888, 22.10506, -2.71613, 25.04781])

        assert_almost_equal(nxx_actual, nxx_desired, decimal=5, err_msg='ERROR in: nxx')
        assert_almost_equal(nxy_actual, nxy_desired, decimal=5, err_msg='ERROR in: nxy')
        assert_almost_equal(nyy_actual, nyy_desired, decimal=5, err_msg='ERROR in: nyy')
