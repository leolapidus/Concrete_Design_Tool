from FE_code.model import Model
from Visualization.plot import Plot2D
from Concrete_Design.bending_without_n import m_eds
from Concrete_Design.values import Values



model = Model(analysis_type='beam')

# model.add_node(id=1, x=0.0, y=0.0)
# model.add_node(id=2, x=0.1, y=0.1)
# model.add_node(id=3, x=0.2, y=0.2)
# model.add_node(id=4, x=0.3, y=0.3)
# model.add_node(id=5, x=0.4, y=0.4)
# model.add_node(id=6, x=0.5, y=0.5)
# model.add_node(id=7, x=0.6, y=0.6)
# model.add_node(id=8, x=0.7, y=0.7)
# model.add_node(id=9, x=0.8, y=0.8)
# model.add_node(id=10, x=0.9, y=0.9)
# model.add_node(id=11, x=1.0, y=1.0)

model.add_node(id=1, x=0.0, y=0.0)
model.add_node(id=2, x=0.1, y=0.0)
model.add_node(id=3, x=0.2, y=0.0)
model.add_node(id=4, x=0.3, y=0.0)
model.add_node(id=5, x=0.4, y=0.0)
model.add_node(id=6, x=0.5, y=0.0)
model.add_node(id=7, x=0.6, y=0.0)
model.add_node(id=8, x=0.7, y=0.0)
model.add_node(id=9, x=0.8, y=0.0)
model.add_node(id=10, x=0.9, y=0.0)
model.add_node(id=11, x=1.0, y=0.0)
      
model.add_beam(id=1, node_ids=[1, 2], element_type='beam')
model.add_beam(id=2, node_ids=[2, 3], element_type='beam')
model.add_beam(id=3, node_ids=[3, 4], element_type='beam')
model.add_beam(id=4, node_ids=[4, 5], element_type='beam')
model.add_beam(id=5, node_ids=[5, 6], element_type='beam')
model.add_beam(id=6, node_ids=[6, 7], element_type='beam')
model.add_beam(id=7, node_ids=[7, 8], element_type='beam')
model.add_beam(id=8, node_ids=[8, 9], element_type='beam')
model.add_beam(id=9, node_ids=[9, 10], element_type='beam')
model.add_beam(id=10, node_ids=[10, 11], element_type='beam')

model.set_material_parameters(E=1000, b=1, h=2.5)

model.add_dirichlet_condition(dof=(1, 'u'), value=0)
model.add_dirichlet_condition(dof=(1, 'v'), value=0)
model.add_dirichlet_condition(dof=(11, 'v'), value=0)
model.add_dirichlet_condition(dof=(11, 'u'), value=0)

#model.add_single_load(id=8, node_id=4, fx=0.0, fy=5.0, mz=0.0)
#model.add_element_load(id=4, structural_element_id=1, pressure=-200)
#model.add_element_load(id=5, structural_element_id=2, pressure=200)
model.add_linear_load(id=11, structural_element_id=1, load_left=0, load_right=-100)
model.add_linear_load(id=12, structural_element_id=2, load_left=-100, load_right=-200)
model.add_linear_load(id=13, structural_element_id=3, load_left=-200, load_right=-300)
model.add_linear_load(id=14, structural_element_id=4, load_left=-300, load_right=-400)
model.add_linear_load(id=15, structural_element_id=5, load_left=-400, load_right=-500)
model.add_linear_load(id=16, structural_element_id=6, load_left=-500, load_right=-600)
model.add_linear_load(id=17, structural_element_id=7, load_left=-600, load_right=-700)
model.add_linear_load(id=18, structural_element_id=8, load_left=-700, load_right=-800)
model.add_linear_load(id=19, structural_element_id=9, load_left=-800, load_right=-900)
model.add_linear_load(id=20, structural_element_id=10, load_left=-900, load_right=-1000)

model.remove_solution()
model.solve()   
model.calculate_internal_forces()

plot = Plot2D()
                
plot.geometry(model=model)
# #plot.plot_geometry()
plot.internal_forces(model=model)
plot.plot_internal_forces()



values = Values()
m_eds(model=model, values=values, concrete_type='c3037', EXP='XD1')