"""This module contains the dimensioning of a beam 
that is loaded by a torque load without normal forces
"""

import numpy as np 
import math as m

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.values import Values 
from Concrete_Design.debug_print import debug


#TODO: Unterscheiden zwischen Feldbereich und Stützbereich 


def bending_without_n_table(As, values, concrete_type, exp):