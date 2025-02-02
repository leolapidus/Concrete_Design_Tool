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
    fcd = values.concrete(concrete_type)['fcd']
    for i, ele in enumerate(model.elements):
        if type(ele)==BeamColumnElement:
            m.append(ele.local_internal_forces[2])
            m.append(ele.local_internal_forces[5]*-1)
            m_ed = max(abs(m[0]), abs(m[1]))
            
            # initial values for eps
            eps_c_2 = -3.5
            eps_s_1 = 25
            sigma_c = 3.4
            sigma_s = 24
            

            # first iteration step
            alpha_r = (3*abs(eps_c_2)-2)/(3*abs(eps_c_2))
            k_a = (abs(eps_c_2)*(3*abs(eps_c_2)-4)+2)/(2*abs(eps_c_2)*(3*abs(eps_c_2)-2))
            x_c = abs(eps_c_2)/(abs(eps_c_2)+abs(eps_s_1))*values.static_usable_height(ele.h, exp)
            F_cd = -1*alpha_r*ele.b*x_c*fcd
            z = values.static_usable_height(ele.h, exp)-k_a*x_c
            m_rds = -1*F_cd*z*1000           
            
            diff = abs(m_rds-m_ed)

            if m_rds > m_ed:
                eps_s_1 = 25
                while diff > 0.001:
                 
                    x_c = abs(eps_c_2)/(abs(eps_c_2)+abs(eps_s_1))*values.static_usable_height(ele.h, exp)

                    if abs(eps_c_2)<= 2:
                        alpha_r = 1/12*abs(eps_c_2)*(6-abs(eps_c_2))
                        k_a = (8-abs(eps_c_2))/(4*(6-abs(eps_c_2)))
                    elif abs(eps_c_2)>2 or abs(eps_c_2)<=3.5:
                        alpha_r = (3*abs(eps_c_2)-2)/(3*abs(eps_c_2))
                        k_a = (abs(eps_c_2)*(3*abs(eps_c_2)-4)+2)/(2*abs(eps_c_2)*(3*abs(eps_c_2)-2))

                    F_cd = -1*alpha_r*ele.b*x_c*fcd
                    z = values.static_usable_height(ele.h, exp)-k_a*x_c
                    m_rds = -1*F_cd*z*1000

                    diff = abs(m_rds-m_ed)

                    if m_rds > m_ed:
                        eps_c_2 = eps_c_2 + sigma_c                       
                    else:
                        eps_c_2 = eps_c_2 - sigma_c
                    if eps_c_2 < -3.5:
                        eps_c_2 = -3.5
                    sigma_c = sigma_c/2
               
            elif m_rds < m_ed:
                print('Betondruckzone zu gering')
                eps_c_2 = -3.5
                while diff > 0.001:
                    
                    x_c = abs(eps_c_2)/(abs(eps_c_2)+abs(eps_s_1))*values.static_usable_height(ele.h, exp)
                    alpha_r = (3*abs(eps_c_2)-2)/(3*abs(eps_c_2))
                    k_a = (abs(eps_c_2)*(3*abs(eps_c_2)-4)+2)/(2*abs(eps_c_2)*(3*abs(eps_c_2)-2))
                    F_cd = -1*alpha_r*ele.b*x_c*fcd
                    z = values.static_usable_height(ele.h, exp)-k_a*x_c
                    m_rds = -1*F_cd*z*1000
                    diff = abs(m_rds-m_ed)
                    if m_rds < m_ed:
                        eps_s_1 = eps_s_1 - sigma_s
                    else:
                        eps_s_1 = eps_s_1 + sigma_s
                    if eps_s_1 > 25:
                        eps_s_1 = 25
                    sigma_s = sigma_s/2
              
            #Stahlspannung
            sigma_s1d = 435+(525/1.15-500/1.15)/(25-2.175)*(eps_s_1-2.175)

            
            #Benötigte Bewehrung
            s = eps_c_2 /(eps_c_2-eps_s_1)
            mue2 = m_ed*0.001*fcd/(ele.b*values.static_usable_height(ele.h, exp)**2*fcd*sigma_s1d*(1-k_a*s))
            As=mue2*ele.b*values.static_usable_height(ele.h, exp)*10000
            #a ist richtig ist beim Leonhardt auf Seite 171
            
            
            
            
           

            erf_As.append(As)
            
          

            #TODO: if abfrage für hyperjet
           
            #diff_erf_As.append(erf_As[i].g)
            #debug('As')

            del m[0]
            del m[0]
    
    return erf_As

