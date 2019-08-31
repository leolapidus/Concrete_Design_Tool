"""Design
=========
This tool contains designing tools for a concrete beam under 
bending and shear loads"""

from Concrete_Design.values import Values
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.bending_without_n_table import bending_without_n_table
from Concrete_Design.bending_without_n_iteration import bending_without_n_iteration
from Concrete_Design.bending_with_n import bending_with_n
from Concrete_Design.shear import shear_reinforcement
from Concrete_Design.debug_print import debug


class Design:
    """
    This tool recives the results from a Finite Element Analysis
    After that it is able to design a cnocrete beam element

    Parametrs
    ---------
    model : class
        class method that contains the Finite Element Analysis
    
    concrete_type : str
        String that holds the type of concrete.
        Use: 'c1215', 'c1620', 'c2025', 'c2530', 'c3037', 'c3545', 'c4050', 'c4555', 'c5060'

    exp : str
        String that holds the Expositionsklasse.
        Use only the authoritative: 'XC1', 'XC2', 'XC3', 'XC4', 'XD1', 'XD2', 'XD3','XS1', 'XS2', 'XS3'
    """

    def __init__(self, model, concrete_type, exp):
        """
        Import the model and the resuts of the finite element anlaysis with 'model'.
        Import the class 'Values' that contains all necessary values for a concrete design.
        """

        self.model = model
        self.values = Values()
        if self.values.concrete(concrete_type):
            self.concrete_type = concrete_type
        if self.values.check_exposition_class(exp):
            self.exp = exp
   

    #==== designing

    
    def bending_design_without_n(self, value):
        """Concrte design of a beam element under bending load.

        Returns
        -------
        As = float
            Area of necessary reinforcement
        """
        #bending without normal force
        if value == 'table':
            As = bending_without_n_table(self.model, self.values, self.concrete_type, self.exp)
        elif value == 'iteration':
            As = bending_without_n_iteration(self.model, self.values, self.concrete_type, self.exp)
        
        #add reinforcement to element information 

        for i, ele in enumerate(self.model.elements):
            if type(ele)==BeamColumnElement:
                ele.bending_reinforcement.append(As[i])
               
        
        return As

    def bending_design_with_n(self):
        """Concrte design of a beam element under bending load and normal force.

        Returns
        -------
        As = float
            Area of necessary reinforcement
        """
        #bending without normal force
        As = bending_with_n(self.model, self.values, self.concrete_type, self.exp)

        #add reinforcement to element information 

        for i, ele in enumerate(self.model.elements):
            if type(ele)==BeamColumnElement:
                ele.bending_reinforcement.append(As[i])
        
        return As

    def shear_design(self):
        """Concrte design of a beam element under shear load.

        Returns
        -------
        asw = float
            Area of necessary reinforcement per meter
        """

        asw = shear_reinforcement(self.values, self.model, self.concrete_type, self.exp)

        #add reinforcement to element information

        for i, ele in enumerate(self.model.elements):
            if type(ele)==BeamColumnElement:
                ele.shear_reinforcement.append(asw[i])
        
        return asw

    def remove_designing(self):
        if self.model.elements:
            for ele in self.model.elements:
                if type(ele)==BeamColumnElement:
                    ele.reset_design()
        
        if self.values:
            self.values.reset_values()