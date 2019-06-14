"""This module contains the dimensioning of a beam 
that is loaded by a torque load"""

import numpy as np 

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 


@property
def fctm(values, concrete_type):
    fctm = values.concrete.concrete_type['fctm']
    
    return fctm

@property
def fyk(values):
    fyk = values.steel
    
    return fyk

def minimal_shear_reinforcement(values, s, model):
    rho_w_min = 0.16*fctm/fyk

    Asw_min = s*rho_w_min*model.b

def shear_reinforcement(values, s, model):

    z = 0.9*values.static_useable_height(model)