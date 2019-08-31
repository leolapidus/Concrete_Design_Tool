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

class ParametrizationTwoSpanBeam:
    
    def __init__(self, mp):
        """
        Create a new model.
        """
        self.mp = mp

    

    def create_model(self,v_parameters):
        mp = self.mp
        mp['model'].reset_model()
        n_nodes = []
        #number of nodes
        if mp['beams'] == 1:
            for i in range(mp['elements_beam1']+1):
                n_nodes.append(i+1)
        else:
            for i in range(mp['elements_beam1'] + mp['elements_beam2'] + 1):
                n_nodes.append(i+1)

        #supports/dirichlet conditions
        supports = []
        supports.append(n_nodes[0])
        if mp['beams'] == 1:
            supports.append(n_nodes[-1])
        else:
            supports.append(n_nodes[mp['elements_beam1']])
            supports.append(n_nodes[-1])
        
        #add nodes to model
        for i in range(len(n_nodes)):
            if i <= mp['elements_beam1']:
                mp['model'].add_node(id=i+1, x=i*mp['l1']/mp['elements_beam1'], y=0.0)
            else:
                mp['model'].add_node(id=i+1, x=i*mp['l2']/mp['elements_beam2'], y=0.0)

        #add Dirichlet conditions to model
        for i in range(len(supports)):
            mp['model'].add_dirichlet_condition(dof=(supports[i], 'v'), value=0)
        mp['model'].add_dirichlet_condition(dof=(1, 'u'), value=0)

        #add beams to model (every optimization step overwrite the beam elments with new parameters)
        for i in range(len(n_nodes)-1):      
            mp['model'].add_beam(id=i+1, node_ids=[i+1, i+2], element_type='beam', E=mp['younges_modulus'], b=v_parameters[i*2], h=v_parameters[i*2+1])

        #reset and add new neumann conditions to model
        mp['model'].reset_neumann_conditions()
        for a in range(len(n_nodes)-1):
            mp['model'].add_distributed_load(id=a+100, structural_element_id=a+1, load=mp['load'], rho=mp['rho'])
        
        return mp['model']

    def tsb_free(self, x):
        return x
 
    def define_shape(self, x):
        if self.mp['shape']=='linear':
            return self.create_linear_tsb(x)
        if self.mp['shape']=='cove':
            return self.create_cove_tsb(x)

    def create_linear_tsb(self, x):
        """
        x: array of parameters
        tsb = two spann beam
                         ___
                     ___|   |
                 ___|   |   | h_e  
             ___|   |   |   |
        h_a |___|___|___|___|
    	"""
        mp = self.mp
        mp.update(x)

        v_parameters = np.zeros(2*(mp['elements_beam1']+mp['elements_beam2']), dtype=object)
        if mp['beams'] == 1:
            delta_h = (mp['h_e'] - mp['h_a'])/mp['l1']
            delta_b = (mp['b_e'] - mp['b_a'])/mp['l1']
            l_element = mp['l1']/mp['elements_beam1']

            for i in range(mp['elements_beam1']):
                v_parameters[i*2]=delta_b*(i+1)*l_element+mp['b_a']
                v_parameters[i*2+1]=delta_h*(i+1)*l_element+mp['h_a']

        else:
            delta_h_beam1 = (mp['h_e'] - mp['h_a'])/mp['l1']
            delta_h_beam2 = -1*(mp['h_e'] - mp['h_a'])/mp['l2']
            delta_b_beam1 = (mp['b_e'] - mp['b_a'])/mp['l1']
            delta_b_beam2 = -1*(mp['b_e'] - mp['b_a'])/mp['l2']
            l_element1 = mp['l1']/mp['elements_beam1']
            l_element2 = mp['l2']/mp['elements_beam2']

            for i in range(mp['elements_beam1']+mp['elements_beam2']):
                if i < mp['elements_beam1']:
                    v_parameters[i*2]=delta_b_beam1*((i+1)*l_element1)+mp['b_a']
                    v_parameters[i*2+1]=delta_h_beam1*((i+1)*l_element1)+mp['h_a']
                else:
                    v_parameters[i*2]=delta_b_beam2*((i-mp['elements_beam1'])*l_element2)+mp['b_e']
                    v_parameters[i*2+1]=delta_h_beam2*((i-mp['elements_beam1'])*l_element2)+mp['h_e']
            mp.v_parameters = v_parameters
            
            self.create_model(v_parameters)

        return v_parameters

        
    def create_cove_tsb(self, x):
        """
        tsb = two spann bar
                         
                            / \h_e 
                 l_c      /     \      
             ___ ___ ___/         \___ ___ ___
        h_a |___|___|___|_________|___|___|___|
        """
        #TODO: l_c abfragen ob es ein Vielfaches von der elementlänge ist oder nicht
        # if l_c % l_element:

        mp = self.mp
        mp.update(x)
        v_parameters = np.zeros(2*(mp['elements_beam1']+mp['elements_beam2']), dtype=object)
        delta_h_beam1 = (mp['h_e'] - mp['h_a'])/mp['lc1']
        delta_h_beam2 = -1*(mp['h_e'] - mp['h_a'])/mp['lc2']
        delta_b_beam1 = (mp['b_e'] - mp['b_a'])/mp['lc1']
        delta_b_beam2 = -1*(mp['b_e'] - mp['b_a'])/mp['lc2']
        l_element1 = mp['l1']/mp['elements_beam1']
        l_element2 = mp['l2']/mp['elements_beam2']
        
        for i in range(mp['elements_beam1']+mp['elements_beam2']):
            if i <= mp['elements_beam1']:
                if i*l_element1 <= (mp['l1']-mp['lc1']):
                    v_parameters[i*2]=mp['b_a'] 
                    v_parameters[i*2+1]=mp['h_a'] 
                else:
                    v_parameters[i*2]=delta_b_beam1*((i+1)*l_element1)+mp['b_a']
                    v_parameters[i*2+1]=delta_h_beam1*(i*l_element1-(mp['l1']-mp['lc1']))+mp['h_a']
            else:
                if (i-mp['elements_beam1'])*l_element2 < mp['lc2']:
                    v_parameters[i*2]=delta_b_beam2*((i-mp['elements_beam1'])*l_element2)+mp['b_e']
                    v_parameters[i*2+1]=delta_h_beam2*((i-mp['elements_beam1'])*l_element2)+mp['h_e']
                else:
                    v_parameters[i*2]=mp['b_a'] 
                    v_parameters[i*2+1]=mp['h_a']       
        mp.v_parameters = v_parameters
        
        self.create_model(v_parameters)
        return v_parameters