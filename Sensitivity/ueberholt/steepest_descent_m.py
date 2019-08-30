"""This module contains the steepest descent algorithm
"""
import numpy as np 
import scipy.optimize as sopt
from FE_code.beam_column_element import BeamColumnElement
from Concrete_Design.designing import Design
import hyperjet as hj
import matplotlib.pyplot as pt


def steepest_descent_m(model, b0, h0, younges_modulus):
    
    
    b = b0
    h = h0
    x = (b,h)
    rho = 25
    load = -100
    
    
    def f(x):
        m = []
        model.reset_neumann_conditions()
        model.set_material_parameters(younges_modulus, x[0], x[1])
        for a in range(4):
            model.add_distributed_load(id=a+100, structural_element_id=a+1, load=load, rho=rho, b=x[0], h=x[1])

        model.remove_solution()
        print(x)
        model.solve()   
        model.calculate_internal_forces()

        for ele in model.elements:
            if type(ele)==BeamColumnElement:
                m.append(ele.local_internal_forces[2])
                m.append(ele.local_internal_forces[5]*-1)

        f = max([abs(x) for x in m]) 

        #f = model._elements[2].local_internal_forces[5]*-1 #m_ed
        #f = model.get_node(2).results["v"]
        return f


    variante_1 = True
    
    if variante_1:
        # Variante 1
        #-----------------
        sc = []
        miter = 1
        step = 0.01/miter
        vals = []
        objectfs = []
        max_int = 300
        # you can customize your own condition of convergence, here we limit the number of iterations
        while miter <= max_int:
            func = f(x)
            vals.append(x)
            objectfs.append(func)
            temp = x-step*func.g
            
            if np.abs(f(temp)-f(x))>0.000000001:
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

        for i in range(100):
            
            func = f(x)
            print('func', func)
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
            
            for n in range(len(x)):
                if type(x[n])==hj.HyperJet:
                    if len(c)==1:
                        a[n]=c
                    else:
                        a[n]=c[n]
                else:
                    a[n]=a[n]

            x_new = [0]*len(x)
        
            for o in range(len(x)):
                if a[o] is not None:
                    x_new[o] = x[o]+a[o]
                else:
                    x_new[o] = x[o]

            for p in range(len(x_new)):
                if x_new[p].f > -10e-8 and x_new[p].f < 10e-8:
                    x_new[p].f = 0.0

            func_new = f(x_new)

            if func_new.f != func_new.f:
                raise RuntimeError("Function evaluation returned nan", func_new)

            if abs(func_new-func) > 0.0000001:
                x = x_new
            else:
                print('Lösung', func)
                break
            print(x, func_new, func_new.g)
            sc.append(x)
            
        fig, ax = pt.subplots()
        pt.axis("equal")
        #pt.contour(xmesh, ymesh, fmesh, 50)
        it_array = np.array(sc)
        pt.plot(it_array.T[0], it_array.T[1], "x-")
        pt.show()    
        
    # Variante 3
    #------------
    
    #alpha_opt = sopt.golden(grad_meth)


            
            # h = h+alpha*sd
            # b = b+alpha*sd

            



        #----------
    #Iteraion 1
    #----------

    # search direction is the neg. gradient sd=-deltaf with inital design x0
    #s = -df
    # line search f(x0 + alpha*sd) and df/dalpha(x0+alpha*sd)=0

    # calculate alpha

    # x1 = x0 + alpha*sd

    # claculate new f(x1)

        
        # As = []
        # model.reset_neumann_conditions()

    



