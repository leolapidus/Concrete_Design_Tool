"""This module contains the dimensioning of a beam 
that is loaded by a torque load without normal forces
"""

import numpy as np 

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 
from Concrete_Design.debug_print import debug


#TODO: Unterscheiden zwischen Feldbereich und Stützbereich 


def bending_without_n_table(model, values, concrete_type, exp):
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
    erf_As = []
    diff_erf_As = []
    fcd = values.concrete(concrete_type)['fcd']
    for i, ele in enumerate(model.elements):
        if type(ele)==BeamColumnElement:
            m.append(ele.local_internal_forces[2])
            m.append(ele.local_internal_forces[5]*(-1))
            m_ed = max(abs(m[0]), abs(m[1]))
            m_ed = m_ed*0.001

            #TODO: if abfrage für hyperjet
            #diff_m_ed = m_ed.g

            #debug('m_ed')

            _calculate_concrete_cover = values.concrete_cover(exp)
            
            mue_eds = m_ed/(ele.b*(values.static_usable_height(ele.h)**2)*fcd)

            #debug('mue_eds')

            _table=values.design_table_values()

            omega = values.interpolate_omega(mue_eds)
            sigma = values.interpolate_sigma(mue_eds)

            As = 1/sigma*(omega*ele.b*values.static_usable_height(ele.h)*fcd)*10000

            erf_As.append(1/sigma*(omega*ele.b*values.static_usable_height(ele.h)*fcd)*10000) # cm²

            #diff_erf_As.append(erf_As[i].g)
            #debug('As')

            del m[0]
            del m[0]
    
    return erf_As

