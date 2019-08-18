"""This module contains the objective function
of the mue eds
"""

from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design
from Concrete_Design.values import Values
from Sensitivity.hyperjetextr import HyperJetExtr

def objective_mue_eds(x, mp):
    
    m = []
    mue_eds = []
    mp.model.reset_neumann_conditions()
    mp.model.set_material_parameters(mp.younges_modulus, x[0], x[1])
    for a in range(3):
        mp.model.add_distributed_load(id=a+100, structural_element_id=a+1, load=mp.load, rho=mp.rho, b=x[0], h=x[1])

    mp.model.remove_solution()
    mp.model.solve()   
    mp.model.calculate_internal_forces()
    fcd = Values().concrete(mp.concrete_type)['fcd']
    for i, ele in enumerate(mp.model.elements):
        if type(ele)==BeamColumnElement:
            m.append(ele.local_internal_forces[2])
            m.append(ele.local_internal_forces[5]*(-1))
            m_ed = max(abs(m[0]), abs(m[1]))
            m_ed = m_ed*0.001

            
            
            mue_eds.append(m_ed/(ele.b*(Values().static_usable_height(ele.h, mp.expositionclass)**2)*fcd))

            del m[0]
            del m[0]
            
    
    f = max(mue_eds)
    
    return HyperJetExtr(f)