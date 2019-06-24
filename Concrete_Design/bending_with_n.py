"""This module contains the dimensioning of a beam 
that is loaded by a torque load and normal forces
"""

import numpy as np 

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 


#TODO: Unterscheiden zwischen Feldbereich und Stützbereich 


def bending_with_n(model, values, concrete_type, exp):
    """Calculate the necessery longitudial reinforcment of a
    beam that is loaded by a torque load without normal forces.

    Parameters
    ----------
    model : class
        class method that contains the Finite Element Analysis

    Returns
    -------
    erf_As : float
        necessary longitudial reinforcement
    """
    m = []
    n = []
    erf_As = []
    fcd = values.concrete(concrete_type)['fcd']
    for ele in model.elements:
        if type(ele)==BeamColumnElement:
            m.append(ele.local_internal_forces[2])
            m.append(ele.local_internal_forces[5]*-1)
            m_ed = max(abs(m[0]), abs(m[1]))

            n.append(ele.local_internal_forces[0]*-1)
            n.append(ele.local_internal_forces[3])

            n_ed_min = min(n)
            n_ed_max = max(n)

            if abs(n_ed_min)> n_ed_max:
                n_ed = n_ed_min
            else:
                n_ed = n_ed_max

            _calculate_concrete_cover = values.concrete_cover(exp)

            z = values.static_usable_height(ele.h)-ele.h/2

            m_eds = m_ed - n_ed*z
            
            mue_eds = m_eds*0.001/(ele.b*(values.static_usable_height(ele.h)**2)*fcd)

            _table=values.design_table_values()

            omega = values.interpolate_omega(mue_eds)
            sigma = values.interpolate_sigma(mue_eds)

            erf_As.append(1/sigma*(omega*ele.b*values.static_usable_height(ele.h)*fcd+n_ed)*10000) # cm²

            del m[0]
            del m[0]
            del n[0]
            del n[0]
    
    print(erf_As)
    return erf_As

