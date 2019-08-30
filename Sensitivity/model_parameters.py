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
    def __init__(self):
        self.parameters = {}
        self.variable_indices = {}



    def add_parameter(self, key, value, is_variable=False):

        if key in self.parameters:
            raise RuntimeError("Key {} already exists!".format(key))

        self.parameters[key] = (value, is_variable)



    def __getitem__(self, key):

        return self.parameters[key][0]



    def initialize(self):

        for key, val in self.parameters.items():
            if val[1]:
                self.variable_indices[key] = len(self.variable_indices)

        for key, i in self.variable_indices.items():
            self.parameters[key] = HJ(self.parameters[key][0],len(self.variable_indices), i)

    def get_variables(self):

        x = []
        for key in self.variable_indices.keys():
            x.append(self.parameters[key])
        return x

    def update(self, x):

        for key, i in self.variable_indices.items():
            self.parameters[key] = x[i]
    
    model = None
    concrete_type = 'c2025'
    expositionclass = 'XD3'
    rho = 25
    load = -100
    calculation_as = 'table'
    younges_modulus = 0
    reinforce_global_opti = False
    nodes = 4
    n_beams = nodes-1

    model                    = None
    concrete_type            = 'c2530'
    expositionclass          = 'XC3'
    rho                      = 25
    load                     = -100
    calculation_as           = 'table'
    younges_modulus          = 0
    l1                       = [4, False]
    l2                       = [4, False]
    h_a                      = [1.0, True]
    h_e                      = [1.0, True]
    b_a                      = [1.0, False]
    b_e                      = [1.0, False]
    beams                    = [2, False]
    elements_beam1           = [20, False] 
    elements_beam2           = [20, False]
    l_c1                     = [0, False]
    l_c2                     = [0, False]

    v = [l1, l2, h_a, h_e, b_a, b_e, beams, elements_beam1, elements_beam2, l_c1, l_c2]

    def constants(self):
        v_constant = dict ()
        for i in range(len(self.v)):
            if self.v[i][1]==False:
                v_constant[i]=self.v[i][0]
        return v_constant

