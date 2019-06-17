
from Concrete_Design.values import Values
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.bending_without_n import bending
from Concrete_Design.shear import shear_reinforcement

class Design:


    def __init__(self, model, concrete_type, exp):


        self.model = model
        self.values = Values()
        if self.values.concrete(concrete_type):
            self.concrete_type = concrete_type
        if self.values.check_exposition_class(exp):
            self.exp = exp
   

    #==== designing

    
    def bending_design(self):

        #bending without normal force
        As = bending(self.model, self.values, self.concrete_type, self.exp)

        #add reinforcement to element information 

        for i, ele in enumerate(self.model.elements):
            if type(ele)==BeamColumnElement:
                ele.bending_reinforcement.append(As[i])
        
        return As

    def shear_design(self):

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