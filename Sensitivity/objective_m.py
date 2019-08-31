"""This module contains the objective function
for the bending moment
"""
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design


def objective_m(x, mp):
    
    m = []
    mp.model.reset_neumann_conditions()
    mp.model.set_material_parameters(mp.younges_modulus, x[0], x[1])
    for a in range(4):
        mp.model.add_distributed_load(id=a+100, structural_element_id=a+1, load=mp.load, rho=mp.rho, b=x[0], h=x[1])

    mp.model.remove_solution()
    mp.model.solve()   
    mp.model.calculate_internal_forces()

    for ele in mp.model.elements:
        if type(ele)==BeamColumnElement:
            m.append(ele.local_internal_forces[2])
            m.append(ele.local_internal_forces[5]*-1)

    f = max([abs(x) for x in m]) 

    return f