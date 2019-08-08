"""This module contains the dimensioning of a beam 
that is loaded by a torque load without normal forces
"""

import numpy as np 

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 
from Concrete_Design.debug_print import debug


#TODO: Unterscheiden zwischen Feldbereich und Stützbereich 


def bending_without_n_iteration(model, values, concrete_type, exp):
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
            m.append(ele.local_internal_forces[5]*-1)
            m_ed = max(abs(m[0]), abs(m[1]))
            # m_ed = m_ed*0.001
            _calculate_concrete_cover = values.concrete_cover(exp)
            d = values.static_usable_height(ele.h)
            # initial values for eps
            eps_c_2 = -3.5
            eps_s_1 = 25
            a = 3.4
            b = 24
            

            # first iteration step
            x = abs(eps_c_2)/(abs(eps_c_2)+abs(eps_s_1))*d

            alpha_r = (3*abs(eps_c_2)-2)/(3*abs(eps_c_2))
            k_a = (abs(eps_c_2)*(3*abs(eps_c_2)-4)+2)/(2*abs(eps_c_2)*(3*abs(eps_c_2)-2))

            F_cd = -1*alpha_r*ele.b*x*fcd

            z = d-k_a*x

            m_rds = -1*F_cd*z*1000

            diff = abs(m_rds-m_ed)

            if m_rds > m_ed:
                eps_s_1 = 25
                while diff > 0.001:
                 
                    x = abs(eps_c_2)/(abs(eps_c_2)+abs(eps_s_1))*d

                    if abs(eps_c_2)<= 2:
                        alpha_r = 1/12*abs(eps_c_2)*(6-abs(eps_c_2))
                        k_a = (8-abs(eps_c_2))/(4*(6-abs(eps_c_2)))
                    elif abs(eps_c_2)>2 or abs(eps_c_2)<=3.5:
                        alpha_r = (3*abs(eps_c_2)-2)/(3*abs(eps_c_2))
                        k_a = (abs(eps_c_2)*(3*abs(eps_c_2)-4)+2)/(2*abs(eps_c_2)*(3*abs(eps_c_2)-2))

                    F_cd = -1*alpha_r*ele.b*x*fcd
                    z = d-k_a*x
                    m_rds = -1*F_cd*z*1000

                    diff = abs(m_rds-m_ed)

                    if m_rds > m_ed:
                        eps_c_2 = eps_c_2 + a                       
                    else:
                        eps_c_2 = eps_c_2 - a
                    if eps_c_2 < -3.5:
                        eps_c_2 = -3.5
                    a = a/2
                    
                m_rds = m_rds
                eps_c_2 = eps_c_2
                eps_s_1 = eps_s_1
                F_cd = F_cd
                
            elif m_rds < m_ed:
                eps_c_2 = -3.5
                while diff > 0.001:
                    
                    x = abs(eps_c_2)/(abs(eps_c_2)+abs(eps_s_1))*d
                    alpha_r = (3*abs(eps_c_2)-2)/(3*abs(eps_c_2))
                    k_a = (abs(eps_c_2)*(3*abs(eps_c_2)-4)+2)/(2*abs(eps_c_2)*(3*abs(eps_c_2)-2))
                    F_cd = -1*alpha_r*ele.b*x*fcd
                    z = d-k_a*x
                    m_rds = -1*F_cd*z*1000
                    diff = abs(m_rds-m_ed)
                    if m_rds < m_ed:
                        eps_s_1 = eps_s_1 - b
                    else:
                        eps_s_1 = eps_s_1 + b
                    if eps_s_1 > 25:
                        eps_s_1 = 25
                    b = b/2
                m_rds = m_rds
                eps_c_2 = eps_c_2
                eps_s_1 = eps_s_1
                
                F_cd = F_cd
            elif abs(m_rds-m_ed)<0.001:
                m_rds=m_rds
                eps_c_2 = eps_c_2
                eps_s_1 = eps_s_1
                F_cd = F_cd

            #Stahlspannung
            sigma_s1d = 435+(525/1.15-500/1.15)/(25-2.175)*(eps_s_1-2.175)
            #Benötigte Bewehrungg
            As = (abs(F_cd)/(sigma_s1d))*10000

            erf_As.append(As)

            #TODO: if abfrage für hyperjet
           
            #diff_erf_As.append(erf_As[i].g)
            #debug('As')

            del m[0]
            del m[0]
    
    return erf_As

