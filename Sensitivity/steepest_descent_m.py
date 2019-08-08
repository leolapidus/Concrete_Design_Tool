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
    rho = 1
    load = -100
    
    
    def f(x):
        m = []
        model.reset_neumann_conditions()
        model.set_material_parameters(younges_modulus, x[0], x[1])
        for a in range(3):
            model.add_distributed_load(id=a+100, structural_element_id=a+1, load=load, rho=rho, b=x[0], h=x[1])

        model.remove_solution()
        model.solve()   
        model.calculate_internal_forces()

        for ele in model.elements:
            if type(ele)==BeamColumnElement:
                m.append(ele.local_internal_forces[2])
                m.append(ele.local_internal_forces[5]*-1)

        #m_ed = max([abs(x) for x in m]) 

        f = model._elements[2].local_internal_forces[5]*-1 #m_ed
        #f = model.get_node(2).results["v"]
        return f

    def df(x):
        return f(x).g

    def hessian(x):
        return f(x).h


    # Variante 1
    #-----------------
    # sc = []
    # miter = 1
    # step = 0.0001/miter
    # vals = []
    # objectfs = []
    # max_int = 300
    # # you can customize your own condition of convergence, here we limit the number of iterations
    # while miter <= max_int:
    #     vals.append(x)
    #     objectfs.append(f(x))
    #     temp = x-step*df(x)
        
    #     if np.abs(f(temp)-f(x))>0.000000000001:
    #         x = temp
    #     else:
    #         break
    #     sc.append(x)
    #     print(x, f(x), miter)
    #     print(df(x))
    #     miter += 1
    

    # fig, ax = pt.subplots()
    # pt.axis("equal")
    # #pt.contour(xmesh, ymesh, fmesh, 50)
    # it_array = np.array(sc)
    # pt.plot(it_array.T[0], it_array.T[1], "x-")
    # pt.show() 
     
    # Variante 2
    #------------

    sc=[]   # for plotting

    for i in range(100):
        
        func = f(x)
        sd = -func.g
        q = func.h
        for i in range(len(q)):
            if q[i,i] < 1e-10:
                q[i,i]=0
            else:
                pass     
        alpha_1 = np.linalg.inv(q)
        c = np.dot(alpha_1,sd)
        a = [None]*len(x)
        
        for i in range(len(x)):
            if type(x[i])==hj.HyperJet:
                if len(c)==1:
                    a[i]=c
                else:
                    a[i]=c[i]
            else:
                a[i]=a[i]



        x_new = [0]*len(x)
      
        for i in range(len(x)):
            if a[i] is not None:
                x_new[i] = x[i]+a[i]
            else:
                x_new[i] = x[i]


        # print(f(x_new))
        # print(f(x))
        if abs(f(x_new)-f(x)) > 0.0000001:
            x = x_new
        else:
            print('Lösung', f(x))
            break
        print(x, f(x), df(x))
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

    



