from FE_code.model import Model
from Visualization.plot import Plot2D
from Concrete_Design.designing import Design
from Concrete_Design.values import Values
import numpy as np

from Sensitivity.sensitivity_as import sensitivity_as
from Visualization.plot_sensitivity import visualization_sensitivity_as
from Sensitivity.sensitivtiy_asw import sensitivity_asw
from Visualization.plot_sensitivity import visualization_sensitivity_asw

import hyperjet as hj


#Define model
model = Model(analysis_type='beam')
val = Values()
concrete_type = 'c2530'
expositionclass = 'XC3'

b_min = 1.0
b_max = 3.0
delt_b = 50
b = np.linspace(b_min, b_max, delt_b)   #m

h_min = 0.4
h_max = 1.8
delta_h = 50
h = np.linspace(h_min, h_max, delta_h) #m

use_hyperjet = False
if use_hyperjet:
    b = hj.HyperJet(b, [1,0])
    h = hj.HyperJet(h, [0,1])
    

younges_modulus = val.concrete(concrete_type)['Ecm']

# #Beam 1
# for i in range(6):
#     model.add_node(id=i+1, x=0, y=i*0.2)

# for i in range(5):      
#     model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam')

#Beam 2

for i in range(5):
    model.add_node(id=i+22, x=i*0.2+0.2, y=1.1+i*0.1)
model.add_node(id=6, x=0.0, y=1.0)
model.add_beam(id=22, node_ids=[6, 22], element_type='beam')
    
for i in range(4):
    model.add_beam(id=i+23, node_ids=[i+22, i+23], element_type='beam')

model.add_dirichlet_condition(dof=(22, 'u'), value=0)
model.add_dirichlet_condition(dof=(22, 'v'), value=0)
model.add_dirichlet_condition(dof=(26, 'v'), value=0)
#model.add_dirichlet_condition(dof=(26, 'u'), value=0)





As = sensitivity_as(model, b, h, younges_modulus, concrete_type, expositionclass)
print(As)

visualization_sensitivity_as(b, h, As, b_min, b_max, h_min, h_max)

asw = sensitivity_asw(model, b, h, younges_modulus, concrete_type, expositionclass)

visualization_sensitivity_asw(b, h, asw, b_min, b_max, h_min, h_max)



