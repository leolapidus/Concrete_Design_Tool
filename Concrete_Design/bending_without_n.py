"""This module contains the dimensioning of a beam 
that is loaded by a torque load"""

import numpy as np 

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 


#TODO: Unterscheiden zwischen Feldbereich und Stützbereich 


def m_eds(model, values, concrete_type, EXP):
    m = []
    erf_As = []
    c = values.concrete(concrete_type)
    fcd = c['fcd']
    for ele in model.elements:
        if type(ele)==BeamColumnElement:
            m.append(ele.local_internal_forces[2])
            m.append(ele.local_internal_forces[5]*-1)
            m_ed = abs(max(m))*0.001

            b = ele.b
            h = ele.h 
            _calculate_concrete_cover = values.concrete_cover(EXP)
            

            mue_eds = m_ed/(b*(values.static_usable_height(h)**2)*fcd)


            print(mue_eds)

            table=values.design_table_values()

            omega = values.interpolate_omega(mue_eds)
            sigma = values.interpolate_sigma(mue_eds)

            erf_As.append(1/sigma*(omega*b*values.static_usable_height(h)*fcd)*10000) # cm²

            del m[0]
            del m[0]
    
    print(erf_As)
    return erf_As

