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
from Sensitivity.objective_as import objective_as
from Sensitivity.steepest_descent_as import steepest_descent_as
from Sensitivity.steepest_descent_mue_eds import steepest_descent_mue_eds



import hyperjet as hj

#============
#Define model
#============
val = Values()
model = Model(analysis_type='beam')
concrete_type = 'c2530'
expositionclass = 'XC3'
b0 = 1.0
h0 = 1.0
load = -100
calculation_as = 'table'
younges_modulus = Values().concrete(concrete_type)['Ecm']
#Beam 1
#------
for i in range(5):
    model.add_node(id=i+1, x=i*0.5, y=0.0)

for i in range(4):      
    model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam')

#Beam 2
#------
# for i in range(5):
#     model.add_node(id=i+22, x=i*0.2+0.2, y=1.1+i*0.1)
# model.add_node(id=6, x=0.0, y=1.0)
# model.add_beam(id=22, node_ids=[6, 22], element_type='beam') 
# for i in range(4):
#     model.add_beam(id=i+23, node_ids=[i+22, i+23], element_type='beam')

#Dirichlet conditions
#--------------------
model.add_dirichlet_condition(dof=(1, 'u'), value=0)
model.add_dirichlet_condition(dof=(1, 'v'), value=0)
model.add_dirichlet_condition(dof=(5, 'v'), value=0)


#=========================
#plotting design space
#=========================
b_min = 0.5
b_max = 3.0
delt_b = 50
b = np.linspace(b_min, b_max, delt_b)   #m

h_min = 0.4
h_max = 3.0
delta_h = 50
h = np.linspace(h_min, h_max, delta_h) #m


#================
#steepest descent
#================
selfweight = True
if selfweight:
    rho =25

use_hyperjet = True
if use_hyperjet:
    b0 = hj.HyperJet(b0, [1,0])
    h0 = hj.HyperJet(h0, [0,1])
    x=(b0, h0)
    

#As = sensitivity_as(model, b, h, younges_modulus, concrete_type, expositionclass, 'table')

#steepest_descent(func = 'mue_eds', x=x, solvertype = 'linear' ,mp =mp)








steepest_descent_as(model, b0, h0, younges_modulus, concrete_type, val, expositionclass)
#steepest_descent_m(model, b0, h0, younges_modulus)
#steepest_descent_mue_eds(model, b0, h0, younges_modulus, concrete_type, val, expositionclass)







#As = sensitivity_as(model, b, h, younges_modulus, concrete_type, expositionclass, 'table')

visualization_sensitivity_as(b, h, As, b_min, b_max, h_min, h_max)

asw = sensitivity_asw(model, b, h, younges_modulus, concrete_type, expositionclass)

visualization_sensitivity_asw(b, h, asw, b_min, b_max, h_min, h_max)



