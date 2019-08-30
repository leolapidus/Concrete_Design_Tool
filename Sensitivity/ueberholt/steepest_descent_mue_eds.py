"""This module contains the steepest descent algorithm
"""
import numpy as np 
import scipy.optimize as sopt
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design
import hyperjet as hj
import matplotlib.pyplot as pt



def steepest_descent_mue_eds(model, b0, h0, younges_modulus, concrete_type, val, expositionclass):
    
    x = (b0,h0)
    rho =25
       
    def f(x):
        m = []
        mue_eds = []
        model.reset_neumann_conditions()
        model.set_material_parameters(younges_modulus, x[0], x[1])
        for a in range(3):
            model.add_distributed_load(id=a+100, structural_element_id=a+1, load=-100, rho=rho, b=x[0], h=x[1])

        model.remove_solution()
        model.solve()   
        model.calculate_internal_forces()
        fcd = val.concrete(concrete_type)['fcd']
        for i, ele in enumerate(model.elements):
            if type(ele)==BeamColumnElement:
                m.append(ele.local_internal_forces[2])
                m.append(ele.local_internal_forces[5]*(-1))
                m_ed = max(abs(m[0]), abs(m[1]))
                m_ed = m_ed*0.001

                #TODO: if abfrage für hyperjet
                #diff_m_ed = m_ed.g

                #debug('m_ed')

                
                mue_eds.append(m_ed/(ele.b*(val.static_usable_height(ele.h, expositionclass)**2)*fcd))
                
                del m[0]
                del m[0]
        
        f = max(mue_eds)
        
        return f

    


    variante_1 = True

    if variante_1:
        # Variante 1
        #-----------------
        sc = []
        miter = 1
        step = 90/miter
        vals = []
        objectfs = []
        max_int = 20
        # you can customize your own condition of convergence, here we limit the number of iterations
        while miter <= max_int:
            func = f(x)
            vals.append(x)
            objectfs.append(func)
            temp = x-step*func.g
            
            if np.abs(f(temp)-f(x))>0.0000001:
                x = temp
            else:
                break
            sc.append(x)
            print(x, func, func.g, miter)
            miter += 1
        

        fig, ax = pt.subplots()
        pt.axis("equal")
        #pt.contour(xmesh, ymesh, fmesh, 50)
        it_array = np.array(sc)
        pt.plot(it_array.T[0], it_array.T[1], "x-")
        pt.show() 
    else:    
        # Variante 2
        #------------

        sc=[]   # for plotting

        for k in range(100):
            
            func = f(x)
            sd = -func.g
            q = func.h
            for j in range(len(q)):
                if q[j,j] < 10e-15:
                    q[j,j]=0
                else:
                    pass     
            alpha_1 = np.linalg.inv(q)
            c = np.dot(alpha_1,sd)
            a = [None]*len(x)
            
            for o in range(len(x)):
                if type(x[o])==hj.HyperJet:
                    if len(c)==1:
                        a[o]=c
                    else:
                        a[o]=c[o]
                else:
                    a[o]=a[o]

            x_new = [0]*len(x)
        
            for n in range(len(x)):
                if a[n] is not None:
                    x_new[n] = x[n]+a[n]
                else:
                    x_new[n] = x[n]

            for p in range(len(x_new)):
                
                if x_new[p].f > -10e-8 and x_new[p].f < 10e-8:
                    x_new[p].f = 0.0
            
           
            if abs(f(x_new)-f(x)) > 0.00001:
                x = x_new
            else:
                print('Lösung mue_eds =', f(x))
                break
            print(x, f(x), f(x).g, k)
            sc.append(x)
            
        fig, ax = pt.subplots()
        pt.axis("equal")
        #pt.contour(xmesh, ymesh, fmesh, 50)
        it_array = np.array(sc)
        pt.plot(it_array.T[0], it_array.T[1], "x-")
        pt.show()    
        
    
    



