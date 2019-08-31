"""This module contains the objective function for the
longitudinal reinforcement
"""

from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design
from Sensitivity.model_parameters import ModelParameters
from operator import itemgetter



def objective_as(x, mp, parametrization):
    
    As = []
    
    parametrization.define_shape(x)
    
    mp['model'].remove_solution()
    mp['model'].solve()   
    mp['model'].calculate_internal_forces()
    
    design = Design(mp['model'], mp['concrete_type'], mp['expositionclass'])
    design.remove_designing()
    design.bending_design_without_n(mp['calculation_as'])
       
    for ele in mp['model'].elements:
        if type(ele)==BeamColumnElement:
            As.append(ele.bending_reinforcement[0])
              
    return sum(As)