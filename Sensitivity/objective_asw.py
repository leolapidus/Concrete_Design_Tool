"""This module contains the objective function for the
longitudinal reinforcement
"""

from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design
from Sensitivity.model_parameters import ModelParameters
from Sensitivity.hyperjetextr import HyperJetExtr



def objective_asw(x, mp, **kwargs):
    
    asw = []
    for i in range(mp.nodes-1):      
        mp.model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam', E=mp.younges_modulus, b=x[i][0], h=x[i][1])
    mp.model.reset_neumann_conditions()
    #mp.model.set_material_parameters(mp.younges_modulus, x[0], x[1])
    
    for a in range(mp.nodes-1):
        mp.model.add_distributed_load(id=a+100, structural_element_id=a+1, load=mp.load, rho=mp.rho)

    mp.model.remove_solution()
    mp.model.solve()   
    mp.model.calculate_internal_forces()

    design = Design(mp.model, mp.concrete_type, mp.expositionclass)
    design.remove_designing()
    design.shear_design()

    if mp.reinforce_global_opti:
        for ele in mp.model.elements:
            if type(ele)==BeamColumnElement:
                asw.append(ele.shear_reinforcement[0])
        f = list()
        for i in enumerate(asw):
            f.append([i[1].f, i[0]])
        f = max(f)
        f = asw[f[1]]
        return HyperJetExtr(f)
        
    else:
        for ele in mp.model.elements:
            if type(ele)==BeamColumnElement:
                asw.append(ele.shear_reinforcement[0])

    
    return asw