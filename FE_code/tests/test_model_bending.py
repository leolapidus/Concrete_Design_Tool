"""
Test for bending models
"""

from unittest import TestCase
from numpy.testing import assert_almost_equal
import numpy as np

from FE_code.model import Model

class TestQuad(TestCase):
    def setUp(self):
        model = Model(analysis_type='bending')
        model.add_node(id=1, x=0.0, y=0.0)
        model.add_node(id=2, x=1.0, y=0.0)
        model.add_node(id=3, x=0.0, y=1.0)
        model.add_node(id=4, x=1.0, y=1.0)
        model.add_quad(id=1, node_ids=[1, 2, 4, 3], element_type='bending_RM_full')
        model.set_material_parameters(E=1, t=0.1, prxy=0.2)
        model.add_dirichlet_condition(dof=(1, 'w'), value=0)
        model.add_dirichlet_condition(dof=(1, 'phix'), value=0)
        model.add_dirichlet_condition(dof=(1, 'phiy'), value=0)
        model.add_dirichlet_condition(dof=(2, 'w'), value=1) #non-homogenuous
        model.add_dirichlet_condition(dof=(2, 'phix'), value=1) #non-homogenuous
        model.add_dirichlet_condition(dof=(2, 'phiy'), value=1) #non-homogenuous
        model.add_dirichlet_condition(dof=(3, 'w'), value=0)
        model.add_dirichlet_condition(dof=(3, 'phix'), value=0)
        model.add_dirichlet_condition(dof=(3, 'phiy'), value=0)
        model.add_single_load(id=2, node_id=4, fz=1.0, mx=1.0, my = 1.0)
        self.model = model

    def test_solution(self):
        self.model.remove_solution()
        self.model.solve()
        w_actual = max([node.results['w'] for node in self.model.nodes], key=abs)
        w_desired = -595.154452124379
        assert_almost_equal(w_actual, w_desired)

    def test_solution_reduced(self):
        self.model.get_element(1).reduced = True
        self.model.remove_solution()
        self.model.solve()
        w_actual = max([node.results['w'] for node in self.model.nodes], key=abs)
        w_desired = -6991.599999999978
        assert_almost_equal(w_actual, w_desired)

    def test_nodal_stresses(self):
        self.model.remove_solution()
        self.model.solve()
        self.model.calculate_nodal_stresses()

        sigma_xx_max_actual = [node.results['sigma_xx_max'] for node in self.model.nodes]
        sigma_yy_max_actual = [node.results['sigma_yy_max'] for node in self.model.nodes]
        tau_xy_max_actual = [node.results['tau_xy_max'] for node in self.model.nodes]
        tau_xz_max_actual = [node.results['tau_xz_max'] for node in self.model.nodes]
        tau_yz_max_actual = [node.results['tau_yz_max'] for node in self.model.nodes]

        sigma_xx_max_desired = np.array([-4.34738, 16.47111, 48.50112, 69.31962])
        sigma_yy_max_desired = np.array([-21.98691, 82.10556, -11.41721, 92.67527])
        tau_xy_max_desired = np.array([-7.71673, 28.89779, 16.3224, 52.93692])
        tau_xz_max_desired = np.array([-152.2303, 153.7928, -351.04538, 260.09873])
        tau_yz_max_desired = np.array([-60.02827, -249.94801, 66.97337, 224.02854])

        assert_almost_equal(sigma_xx_max_actual, sigma_xx_max_desired, decimal=5,
            err_msg='ERROR in: sigma_xx')
        assert_almost_equal(sigma_yy_max_actual, sigma_yy_max_desired, decimal=5,
            err_msg='ERROR in: sigma_xx')
        assert_almost_equal(tau_xy_max_actual, tau_xy_max_desired, decimal=5,
            err_msg='ERROR in: tau_xy')
        assert_almost_equal(tau_xz_max_actual, tau_xz_max_desired, decimal=5,
            err_msg='ERROR in: tau_xz')
        assert_almost_equal(tau_yz_max_actual, tau_yz_max_desired, decimal=5,
            err_msg='ERROR in: tau_yz')

    def test_nodal_stresses_reduced(self):
        self.model.get_element(1).reduced = True
        self.model.remove_solution()
        self.model.solve()
        self.model.calculate_nodal_stresses()

        sigma_xx_max_actual = [node.results['sigma_xx_max'] for node in self.model.nodes]
        sigma_yy_max_actual = [node.results['sigma_yy_max'] for node in self.model.nodes]
        tau_xy_max_actual = [node.results['tau_xy_max'] for node in self.model.nodes]
        tau_xz_max_actual = [node.results['tau_xz_max'] for node in self.model.nodes]
        tau_yz_max_actual = [node.results['tau_yz_max'] for node in self.model.nodes]

        sigma_xx_max_desired = np.array([-53.37236, 199.43481, 676.2112 , 929.01837])
        sigma_yy_max_desired = np.array([-267.11179, 996.92407, -121.19508, 1142.84078])
        tau_xy_max_desired = np.array([-106.79761, 398.6727, 185.11896, 690.58928])
        tau_xz_max_desired = np.array([-2105.79612, 2107.35862, -4205.98382, 4219.42357])
        tau_yz_max_desired = np.array([-773.86017, -2867.59816, 768.37061, 2888.08547])

        assert_almost_equal(sigma_xx_max_actual, sigma_xx_max_desired, decimal=5,
            err_msg='ERROR in: sigma_xx')
        assert_almost_equal(sigma_yy_max_actual, sigma_yy_max_desired, decimal=5,
            err_msg='ERROR in: sigma_xx')
        assert_almost_equal(tau_xy_max_actual, tau_xy_max_desired, decimal=5,
            err_msg='ERROR in: tau_xy')
        assert_almost_equal(tau_xz_max_actual, tau_xz_max_desired, decimal=5,
            err_msg='ERROR in: tau_xz')
        assert_almost_equal(tau_yz_max_actual, tau_yz_max_desired, decimal=5,
            err_msg='ERROR in: tau_yz')
