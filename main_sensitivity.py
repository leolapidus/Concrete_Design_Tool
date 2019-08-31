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

from Parametrization.parametrization import Parametrization

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
mp.add_parameter("younges_modulus", Values().concrete(mp.concrete_type)['Ecm'])
mp.add_parameter("l1", 4)
mp.add_parameter("l2", 4.0)
mp.add_parameter("h_a", 1.0, is_variable=True)
mp.add_parameter("h_e", 1.0, is_variable=True)
mp.add_parameter("b_a", 4)
mp.add_parameter("b_e", 4.0)
mp.model                    = Model(analysis_type='beam')

mp.concrete_type            = 'c2530'
mp.expositionclass          = 'XC3'
mp.load                     = -100
mp.calculation_as           = 'table'
mp.younges_modulus          = Values().concrete(mp.concrete_type)['Ecm']
mp.l1                       = [4, False]
mp.l2                       = [4, False]
mp.h_a                      = [1.0, True]
mp.h_e                      = [1.0, True]
mp.b_a                      = [1.0, False]
mp.b_e                      = [1.0, False]
mp.beams                    = [2, False]
mp.elements_beam1           = [20, False] 
mp.elements_beam2           = [20, False]
mp.l_c1                     = [0, False]
mp.l_c2                     = [0, False]
a                           = []
solvertype                  = 'linear'
f                           = HyperJetResponseWrapper(objective_as)
selfweight                  = True
plot_design_space           = False
use_hyperjet                = True
parametrization             = Parametrization(mp)

mp.constants()



# #Beam 1
# #------
# for i in range(mp.nodes):
#     mp.model.add_node(id=i+1, x=i*0.25, y=0.0)







# #Dirichlet conditions
# #--------------------
# mp.model.add_dirichlet_condition(dof=(1, 'u'), value=0)
# mp.model.add_dirichlet_condition(dof=(1, 'v'), value=0)
# mp.model.add_dirichlet_condition(dof=(14, 'v'), value=0)
# mp.model.add_dirichlet_condition(dof=(27, 'v'), value=0)


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

    As = sensitivity_as(mp.model, b, h, mp.younges_modulus, mp.concrete_type, mp.expositionclass, 'table')
    visualization_sensitivity_as(b, h, As, b_min, b_max, h_min, h_max)

    asw = sensitivity_asw(mp.model, b, h, mp.younges_modulus, mp.concrete_type, mp.expositionclass)
    visualization_sensitivity_asw(b, h, asw, b_min, b_max, h_min, h_max)

#================
#steepest descent
#================
if selfweight:
    mp.rho =25

if use_hyperjet:
    # b0 = hj.HyperJet(b0, [1,0])
    # h0 = hj.HyperJet(h0, [0,1])
    #create vector of Parameters for all elements
    # for i in range(mp.nodes-1):
    #     a.append([b0, h0])
    a = parametrization.vector_of_parameters(b0,h0)
    

steepest_descent(f.f, a, solvertype, args=(f, mp, parametrization), g=f.g, h=f.h)
#scipy.optimize.minimize(f.f, x, args=(f, mp), method='SLSQP', jac=f.g, hess=f.h)











