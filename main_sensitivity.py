import numpy as np

from FE_code.model import Model

from Concrete_Design.designing import Design
from Concrete_Design.values import Values

from Visualization.plot import Plot2D
from Visualization.plot_sensitivity import visualization_sensitivity_as
from Visualization.plot_sensitivity import visualization_sensitivity_asw

import hyperjet as hj

from Sensitivity.hj_wrapper import HyperJetResponseWrapper
from Sensitivity.model_parameters import ModelParameters
from Sensitivity.sensitivity_as import sensitivity_as
from Sensitivity.sensitivtiy_asw import sensitivity_asw
from Sensitivity.steepest_descent import steepest_descent
from Sensitivity.objective_as import objective_as
from Sensitivity.objective_mue_eds import objective_mue_eds
from Sensitivity.objective_asw import objective_asw
from Sensitivity.objective_m import objective_m

from Parametrization.parametrization import ParametrizationTwoSpanBeam

import scipy.optimize

#================
#model definition
#================
mp = ModelParameters()
mp.add_parameter("model", Model(analysis_type='beam'))
mp.add_parameter("concrete_type", 'c2530')
mp.add_parameter("expositionclass", 'XC3')
mp.add_parameter("load", -100)
mp.add_parameter("calculation_as", 'table')
mp.add_parameter("younges_modulus", Values().concrete(mp.parameters['concrete_type'][0])['Ecm'])
mp.add_parameter("beams", 2)
mp.add_parameter("elements_beam1", 20)
mp.add_parameter("elements_beam2", 20)
mp.add_parameter("l1", 4)
mp.add_parameter("l2", 4.0)

mp.add_parameter("shape", "linear")

mp.add_parameter("h_a", 1.0, is_variable=True)
mp.add_parameter("h_e", 1.0, is_variable=True)
mp.add_parameter("b_a", 1.0)
mp.add_parameter("b_e", 1.0)
mp.add_parameter("lc1", 1.0)
mp.add_parameter("lc2", 1.0)
mp.initialize()

solvertype                  = 'linear'
f                           = HyperJetResponseWrapper(objective_as)
selfweight                  = True
plot_design_space           = False
parametrization             = ParametrizationTwoSpanBeam(mp) 
if selfweight:
    mp.add_parameter('rho', 25)


#=========================
#plotting design space
#=========================
if plot_design_space:
    b_min = 0.5
    b_max = 3.0
    delt_b = 50
    b = np.linspace(b_min, b_max, delt_b)   #m

    h_min = 0.4
    h_max = 3.0
    delta_h = 50
    h = np.linspace(h_min, h_max, delta_h) #m

    As = sensitivity_as(mp.parameters['model'][0], b, h, mp.parameters['younges_modulus'][0], mp.parameters['concrete_type'][0], mp.parameters['expositionclass'][0], 'table')
    visualization_sensitivity_as(b, h, As, b_min, b_max, h_min, h_max)

    asw = sensitivity_asw(mp.parameters['model'][0], b, h, mp.parameters['younges_modulus'][0], mp.parameters['concrete_type'][0], mp.parameters['expositionclass'][0])
    visualization_sensitivity_asw(b, h, asw, b_min, b_max, h_min, h_max)

#================
#steepest descent
#================
steepest_descent(f.f, mp.get_variables(), solvertype, args=(f, mp, parametrization), g=f.g, h=f.h)
#scipy.optimize.minimize(f.f, x, args=(f, mp), method='SLSQP', jac=f.g, hess=f.h)











