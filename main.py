from FE_code.model import Model
from Visualization.plot import Plot2D
from Concrete_Design.designing import Design
from Concrete_Design.values import Values

import hyperjet as hj


#Define model
model = Model(analysis_type='beam')
val = Values()
concrete_type = 'c2530'
expositionclass = 'XC3'
b = 1.0   #m
h = 0.4 #m

self_weight = True
if self_weight:
    rho = 25
else:
    rho = 0

use_hyperjet = True
if use_hyperjet:
    b = hj.HyperJet(b, [1,0])
    h = hj.HyperJet(h, [0,1])
    

younges_modulus = val.concrete(concrete_type)['Ecm']
print(younges_modulus)

#Beam 1
for i in range(5):
    model.add_node(id=i+1, x=i*0.5, y=0.0)

for i in range(4):      
    model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam')




# for i in range(7):
#     model.add_node(id=i+1, x=i*0.25, y=0)

# for i in range(6):      
#     model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam')

# #Beam 2

# for i in range(5):
#     model.add_node(id=i+22, x=i*0.2+0.2, y=1.0)

# model.add_beam(id=22, node_ids=[6, 22], element_type='beam')
    
# for i in range(4):
#     model.add_beam(id=i+23, node_ids=[i+22, i+23], element_type='beam')

model.set_material_parameters(younges_modulus, b, h)

model.add_dirichlet_condition(dof=(1, 'u'), value=0)
model.add_dirichlet_condition(dof=(1, 'v'), value=0)
model.add_dirichlet_condition(dof=(5, 'v'), value=0)
#model.add_dirichlet_condition(dof=(26, 'u'), value=0)

#loads
#linear load
# for i in range(10):
#     model.add_linear_load(id=i+100, structural_element_id=i+1, load_left=-i*100, load_right=-i*100-100)

#constant distributed load

for i in range(3):
    #model.add_distributed_load(id=i+100, structural_element_id=i+22, load=-100, rho=rho, b=b,h=h)
    model.add_distributed_load(id=i+200, structural_element_id=i+1, load=-100, rho=rho, b=b,h=h)


model.remove_solution()
model.solve()   
model.calculate_internal_forces()

plot = Plot2D()
                
plot.geometry(model)
plot.internal_forces(model)
plot.plot_internal_forces(model)


design = Design(model, concrete_type, expositionclass)
design.remove_designing()
design.bending_design_without_n('table')
design.shear_design()

plot.reinforcement(model)
plot.plot_reinforcement()

