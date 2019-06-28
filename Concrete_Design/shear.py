"""This module contains the dimensioning of a beam 
that is loaded by a torque load"""

import numpy as np 

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 

def minimal_shear_reinforcement(values, model, concrete_type, b):
    """Calculate the minimal necessery shear reinforcment.

    Parameters
    ----------
    model : class
        class method that contains the Finite Element Analysis
    
    concrete_type: str
        string that define the concrete type, e.g. 'c3037'

    Returns
    -------
    asw_min : float
        minimal necessary shear reinforcement
    """

    fctm = values.concrete(concrete_type)['fctm']
    fyk = values.steel()

   
    rho_w_min = 0.16*fctm/fyk
    asw_min = rho_w_min*b*10000
    
    
    return asw_min

def shear_reinforcement(values, model, concrete_type):
    """Calculate the shear reinforcment that is bigger than the minimal
    necessary shear reinforcement.

    Parameters
    ----------
    model : class
        class method that contains the Finite Element Analysis
    
    concrete_type: str
        string that define the concrete type, e.g. 'c3037'
    
    Returns
    -------
    erf_asw : float
        necessary shear reinforcement with respect to the minimal necessary reinforcement
    """

    n = []
    v = []
    erf_asw = []
    fcd = values.concrete(concrete_type)['fcd']
    fck = values.concrete(concrete_type)['fck']
    fyk = values.steel()

    for ele in model.elements:
        if type(ele)==BeamColumnElement:
            z = 0.9*values.static_usable_height(ele.h)

            n.append(ele.local_internal_forces[0])
            n.append(ele.local_internal_forces[3]*-1)
            v.append(ele.local_internal_forces[1])
            v.append(ele.local_internal_forces[4]*-1)

            v_ed = max(abs(v[0]), abs(v[1])) 

            

            for i in n:
                if i < 0:
                    i = 0
                else:
                    pass
            
            n_ed = max(n)

            sigma_cd = n_ed/(ele.b*ele.h)

            v_rdcc = 0.5*0.48*fck**(1/3)*(1-1.2*sigma_cd/fcd)*ele.b*z

            cot_theta = (1.2+1.4*sigma_cd/fcd)/(1-v_rdcc/v_ed)

            if cot_theta <= 1.0:
                cot_theta = 1.0
            elif cot_theta >= 3.0:
                cot_theta = 3.0
            else:
                cot_theta = cot_theta
            
            #Annahme alpha = 90°

            a_sw = (v_ed*0.001)/(fyk/1.15*z*(cot_theta+0)*1)*10**4

            if a_sw >= minimal_shear_reinforcement(values,model,concrete_type,ele.b):
                erf_asw.append(a_sw)
            else:
                erf_asw.append(minimal_shear_reinforcement(values,model,concrete_type,ele.b))

            del n[0]
            del n[0]
            del v[0]
            del v[0]        
                
    
    
    return erf_asw