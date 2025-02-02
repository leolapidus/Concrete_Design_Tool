"""This module contains the creating of a sensitivity chart
for the optimum of shear reinforcement
"""
import numpy as np 
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design

def sensitivity_asw(model, b, h, younges_modulus, concrete_type, expositionclass):
    
    asw_max = np.zeros((len(b),len(h)), dtype=object)
    asw = []

    for j in range(len(h)):
        for i in range(len(b)):
            model.set_material_parameters(younges_modulus, b[i], h[j])
            g = 25*b[i]*h[j]
            for a in range(5):
                model.add_distributed_load(id=a+100, structural_element_id=a+22, load=-1000-g)
            model.remove_solution()
            model.solve()   
            model.calculate_internal_forces()
            design = Design(model, concrete_type, expositionclass)
            design.remove_designing()
            #design.bending_design_without_n()
            design.shear_design()
            for ele in model.elements:
                if type(ele)==BeamColumnElement:
                    asw.append(ele.shear_reinforcement[0])
   
            asw_max[j,i] = max(asw)
            asw = []
            model.reset_neumann_conditions()

    return asw_max
