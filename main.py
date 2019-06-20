from FE_code.model import Model
from Visualization.plot import Plot2D
from Concrete_Design.designing import Design
from Concrete_Design.values import Values


#Define model
model = Model(analysis_type='beam')
val = Values()
concrete_type = 'c2025'
expositionclass = 'XC3'
b = 1   #m
h = 0.5 #m

younges_modulus = val.concrete(concrete_type)['Ecm']

#Beam 1
for i in range(21):
    model.add_node(id=i+1, x=i*0.1, y=0.0)

for i in range(20):      
    model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam')

model.set_material_parameters(younges_modulus, b, h)

model.add_dirichlet_condition(dof=(1, 'u'), value=0)
model.add_dirichlet_condition(dof=(1, 'v'), value=0)
model.add_dirichlet_condition(dof=(21, 'v'), value=0)
model.add_dirichlet_condition(dof=(21, 'u'), value=0)

#loads
#linear load
# for i in range(10):
#     model.add_linear_load(id=i+100, structural_element_id=i+1, load_left=-i*100, load_right=-i*100-100)

#constant distributed load

for i in range(20):
    model.add_linear_load(id=i+100, structural_element_id=i+1, load_left=-1000, load_right=-1000)


model.remove_solution()
model.solve()   
model.calculate_internal_forces()

plot = Plot2D()
                
plot.geometry(model)
# plot.plot_geometry()
plot.internal_forces(model)
plot.plot_internal_forces()


design = Design(model, concrete_type, expositionclass)
design.remove_designing()
design.bending_design()
design.shear_design()

plot.reinforcement(model)
plot.plot_reinforcement()