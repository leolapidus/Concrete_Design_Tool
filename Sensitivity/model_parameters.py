"""
BeamColumnElement
================

Module contains a beam column element under bending action and axial forces.
"""

from Concrete_Design.values import Values

class ModelParameters():

    """Static variables.

    Attributes
    ----------
    model: class
        FE-Model
    younges_modulus: float

    concrete_type: str
        'C30/37'
    expositionclass: str
        'XC4'
    rho: float
        densitiy of material 
    load: float

    calculation_as: str
        'table' or 'iteration'
    """
    
    
    model = None
    concrete_type = 'c2025'
    expositionclass = 'XD3'
    rho = 25
    load = -100
    calculation_as = 'table'
    younges_modulus = 0

