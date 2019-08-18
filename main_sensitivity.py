from FE_code.model import Model
from Visualization.plot import Plot2D
from Concrete_Design.designing import Design
from Concrete_Design.values import Values

import numpy as np

from Sensitivity.model_parameters import ModelParameters
from Sensitivity.sensitivity_as import sensitivity_as
from Visualization.plot_sensitivity import visualization_sensitivity_as
from Sensitivity.sensitivtiy_asw import sensitivity_asw
from Visualization.plot_sensitivity import visualization_sensitivity_asw

from Sensitivity.steepest_descent import steepest_descent
from Sensitivity.steepest_descent_copy import steepest_descent_copy
from Sensitivity.objective_as import objective_as
from Sensitivity.objective_mue_eds import objective_mue_eds
from Sensitivity.hj_wrapper import HyperJetResponseWrapper
import scipy.optimize

import hyperjet as hj

#================
#model definition
#================
mp = ModelParameters()
mp.model = Model(analysis_type='beam')
mp.concrete_type = 'c2530'
mp.expositionclass = 'XC3'
b0 = 1.0
h0 = 1.0
mp.load = -100
mp.calculation_as = 'table'
mp.younges_modulus = Values().concrete(mp.concrete_type)['Ecm']
solvertype = 'linear'
f = HyperJetResponseWrapper(objective_as)
selfweight = True
plot_design_space = False
use_hyperjet = True

#Beam 1
#------
for i in range(5):
    mp.model.add_node(id=i+1, x=i*0.5, y=0.0)

for i in range(4):      
    mp.model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam')


#Dirichlet conditions
#--------------------
mp.model.add_dirichlet_condition(dof=(1, 'u'), value=0)
mp.model.add_dirichlet_condition(dof=(1, 'v'), value=0)
mp.model.add_dirichlet_condition(dof=(5, 'v'), value=0)


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
    b0 = hj.HyperJet(b0, [1,0])
    h0 = hj.HyperJet(h0, [0,1])
    x=[b0, h0]
    

steepest_descent(f.f, x, solvertype, args=(f, mp), g=f.g, h=f.h)
steepest_descent_copy('as', x, 'linear', mp)










