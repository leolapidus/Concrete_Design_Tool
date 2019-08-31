"""
Parametrization
=====

Parametrization of the FE-Model to optimize the structur for forced 
parameters
"""

import numpy as np
import numpy.linalg as la

from Sensitivity.model_parameters import ModelParameters

import hyperjet as hj

class Parametrization:
    
    def __init__(self, mp):
        """
        Create a new model.
        """
        self.mp = mp

    def vector_of_parameters(self, b0, h0):
        a = []
        b = [b0 for s in range(self.mp.elements_beam1+self.mp.elements_beam2)]
        h = [h0 for d in range(self.mp.elements_beam1+self.mp.elements_beam2)]
        for i in range(2*(self.mp.elements_beam1+self.mp.elements_beam2)):
            if i %2 ==0:
                a.append(hj.HyperJet.variable(value=b[int(i/2)], size=2*(self.mp.elements_beam1+self.mp.elements_beam2), index=i))
            else:
                a.append(hj.HyperJet.variable(value=h[int(i/2-0.5)], size=2*(self.mp.elements_beam1+self.mp.elements_beam2), index=i))
            # a.append(h0)
        return a

    def create_model(self,a):
        self.mp.model.reset_model()
        n_nodes = []
        #number of nodes
        if self.mp.beams == 1:
            for i in range(self.mp.elements_beam1+1):
                n_nodes.append(i+1)
        else:
            for i in range(self.mp.elements_beam1 + self.mp.elements_beam2 + 1):
                n_nodes.append(i+1)

        #supports/dirichlet conditions
        supports = []
        supports.append(n_nodes[0])
        if self.mp.beams == 1:
            supports.append(n_nodes[-1])
        else:
            supports.append(n_nodes[self.mp.elements_beam1])
            supports.append(n_nodes[-1])
        
        #add nodes to model
        for i in range(len(n_nodes)):
            if i <= self.mp.elements_beam1:
                self.mp.model.add_node(id=i+1, x=i*self.mp.l1/self.mp.elements_beam1, y=0.0)
            else:
                self.mp.model.add_node(id=i+1, x=i*self.mp.l2/self.mp.elements_beam2, y=0.0)

        #add Dirichlet conditions to model
        for i in range(len(supports)):
            self.mp.model.add_dirichlet_condition(dof=(supports[i], 'v'), value=0)
        self.mp.model.add_dirichlet_condition(dof=(1, 'u'), value=0)

        #add beams to model (every optimization step overwrite the beam elments with new parameters)
        for i in range(len(n_nodes)-1):      
            self.mp.model.add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam', E=self.mp.younges_modulus, b=a[i*2], h=a[i*2+1])

        #reset and add new neumann conditions to model
        self.mp.model.reset_neumann_conditions()
        for a in range(len(n_nodes)-1):
            self.mp.model.add_distributed_load(id=a+100, structural_element_id=a+1, load=self.mp.load, rho=self.mp.rho)
        
        return self.mp.model

    def solve_model(self):
        self.mp.model.remove_solution()
        self.mp.model.solve()   
        self.mp.model.calculate_internal_forces()
        


    def tsb_free(self, x):
        return x
    

    def tsb_linear(self, x):
        """
        tsb = two spann beam
                         ___
                     ___|   |
                 ___|   |   | h_e  
             ___|   |   |   |
        h_a |___|___|___|___|
    	"""
        if self.mp.beams == 1:
            delta_h = (self.mp.h_e - self.mp.h_a)/self.mp.l1
            delta_b = (self.mp.b_e - self.mp.b_a)/self.mp.l1
            l_element = self.mp.l1/self.mp.elements_beam1

            for i in range(self.mp.elements_beam1):
                x[i*2]=delta_b*i*1.5*l_element
                x[i*2+1]=delta_h*i*1.5*l_element

        else:
            delta_h_beam1 = (self.mp.h_e - self.mp.h_a)/self.mp.l1
            delta_h_beam2 = -1*(self.mp.h_e - self.mp.h_a)/self.mp.l2
            delta_b_beam1 = (self.mp.b_e - self.mp.b_a)/self.mp.l1
            delta_b_beam2 = -1*(self.mp.b_e - self.mp.b_a)/self.mp.l2
            l_element1 = self.mp.l1/self.mp.elements_beam1
            l_element2 = self.mp.l2/self.mp.elements_beam2

            for i in range(self.mp.elements_beam1+self.mp.elements_beam2):
                if i <= self.mp.elements_beam1:
                    x[i*2].f=delta_b_beam1*((i+0.5)*l_element1)+self.mp.b_a
                    x[i*2+1].f=delta_h_beam1*((i+0.5)*l_element1)+self.mp.h_a
                else:
                    x[i*2].f=delta_b_beam2*((i-self.mp.elements_beam1-0.5)*l_element2)+self.mp.b_e
                    x[i*2+1].f=delta_h_beam2*((i-self.mp.elements_beam1-0.5)*l_element2)+self.mp.h_e+delta_b_beam1

        return x

        
    def tsb_cove(self, x):
        """
        tsb = two spann bar
                         
                            / \h_e 
                 l_c      /     \      
             ___ ___ ___/         \___ ___ ___
        h_a |___|___|___|_________|___|___|___|
        """
        #TODO: l_c abfragen ob es ein Vielfaches von der elementlänge ist oder nicht
        # if l_c % l_element:

        delta_h_beam1 = (self.mp.h_e - self.mp.h_a)/(self.mp.l1-self.mp.l_c1)
        delta_h_beam2 = -1*(self.mp.h_e - self.mp.h_a)/(self.mp.l2-self.mp.l_c2)
        delta_b_beam1 = (self.mp.b_e - self.mp.b_a)/(self.mp.l1-self.mp.l_c1)
        delta_b_beam2 = -1*(self.mp.b_e - self.mp.b_a)/(self.mp.l2-self.mp.l_c2)
        l_element1 = self.mp.l1/self.mp.elements_beam1
        l_element2 = self.mp.l2/self.mp.elements_beam2

        for i in range(self.mp.elements_beam1+self.mp.elements_beam2):
            if i <= self.mp.elements_beam1:
                if i*l_element1 < self.mp.l_c1:
                    x[i*2]=self.mp.b_a 
                    x[i*2+1]=self.mp.h_a 
                else:
                    x[i*2]=delta_b_beam1*i*1.5*l_element1
                    x[i*2+1]=delta_h_beam1*i*1.5*l_element1
            else:
                if i*l_element2 < (self.mp.l2-self.mp.l_c2):
                    x[i*2]=delta_b_beam2*i*1.5*l_element2
                    x[i*2+1]=delta_h_beam2*i*1.5*l_element2
                else:
                    x[i*2]=self.mp.b_a 
                    x[i*2+1]=self.mp.h_a       
            
            return x