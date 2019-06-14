"""This module contains the dimensioning of a beam 
that is loaded by a torque load"""

import numpy as np 

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 

#TODO: Unterscheiden zwischen Feldbereich und Stützbereich 

@property
def fcd(values, concrete_type):
    fcd = values.concrete.concrete_type['fcd']
    
    return fcd


def m_eds(model, values):
    m = []
    erf_As = []
    for ele in model.elements:
        if type(ele)==BeamColumnElement:
            m.append(ele.local_internal_forces[2])
            m.append(ele.local_internal_forces[5]*-1)
            m_ed = abs(max(m))
            
            mue_eds = m_ed/(model.b*values.static_usable_height(model)**2*fcd)

            print(mue_eds)

            omega = values.interpolate_omega(mue_eds)
            sigma = values.interpolate_sigma(mue_eds)

            erf_As.append(1/sigma*(omega*model.b*values.static_usable_height*fcd)*10000) # cm²
    
    return erf_As