"""This module contains the objective function for the
longitudinal reinforcement
"""

from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design
from Sensitivity.model_parameters import ModelParameters
from Sensitivity.hyperjetextr import HyperJetExtr



def objective_as(x, mp, **kwargs):
    
    As = []
    mp.model.reset_neumann_conditions()
    mp.model.set_material_parameters(mp.younges_modulus, x[0], x[1])
    
    for a in range(3):
        mp.model.add_distributed_load(id=a+100, structural_element_id=a+1, load=mp.load, rho=mp.rho, b=x[0], h=x[1])

    mp.model.remove_solution()
    mp.model.solve()   
    mp.model.calculate_internal_forces()

    design = Design(mp.model, mp.concrete_type, mp.expositionclass)
    design.remove_designing()
    design.bending_design_without_n(mp.calculation_as)

    for ele in mp.model.elements:
        if type(ele)==BeamColumnElement:
            As.append(ele.bending_reinforcement[0])

    f = max(As)
      
    return HyperJetExtr(f)