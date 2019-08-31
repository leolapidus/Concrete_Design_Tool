"""This module contains the steepest descent algorithm
"""
import numpy as np 
import hyperjet as hj
import matplotlib.pyplot as pt
from Sensitivity.objective_as import objective_as
from Sensitivity.objective_m import objective_m
from Sensitivity.objective_mue_eds import objective_mue_eds
from Sensitivity.objective_asw import objective_asw
from matplotlib import colors as mcolors
from matplotlib.gridspec import GridSpec

def steepest_descent_copy(func, x, solvertype, mp):

    if func == 'as':
        def f(x):
            return objective_as(x, mp)
    elif func == 'm':
        def f(x):
            return objective_m(x, mp)
    elif func == 'mue_eds':
        def f(x):
            return objective_mue_eds(x, mp)
    elif func == 'asw':
        def f(x):
            return objective_asw(x, mp)

    
    
    if solvertype == 'linear':
        
        coord = []
        fcoord = []
        miter = 1
        step = 0.01/miter
        vals = []
        objectfs = []
        max_int = 20
        
        while miter <= max_int:
            func = f(x)
            vals.append(x)
            objectfs.append(func)
            temp = x-step*func.g
            coord.append(x)
            fcoord.append(func.f)            
            if np.abs(f(temp)-f(x))>0.0000001:
                x = temp
            else:
                break
            print(x, f(x), f(x).g, miter)
            miter += 1
        
        fig, ax = pt.subplots()
        pt.axis("equal")
        ax.set_title('Steepest Descent \n linearer line search')
        ax.set_ylabel('Höhe [m]')
        ax.set_xlabel('Breite [m]')
        coord_array = np.array(coord)
        pt.plot(coord_array.T[0], coord_array.T[1], "x-")
        for i, value in enumerate(fcoord):
            ax.annotate(f'f(x) = {"%.5f" % value}, i = {i}', (coord[i][0], coord[i][1]))
            
        pt.show() 

    elif solvertype == 'hessian':    
        
        coord = []
        fcoord = []   # for plotting

        for k in range(100):
            
            func = f(x)
            sd = -func.g
            q = func.h
            coord.append(x)
            fcoord.append(func.f) 
            for j in range(len(q)):
                if q[j,j] < 10e-15:
                    q[j,j]=0
                else:
                    pass     
            c = np.linalg.solve(q, sd)
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
        
            if np.linalg.norm(a) > 0.1:
                a /= np.linalg.norm(a) * 0.1

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
            
            
        fig, ax = pt.subplots()
        pt.axis("equal")
        ax.set_title('Steepest Descent \n line search mit Hesse-Matrix')
        ax.set_ylabel('Höhe [m]')
        ax.set_xlabel('Breite [m]')
        coord_array = np.array(coord)
        pt.plot(coord_array.T[0], coord_array.T[1], "x-")
        for i, value in enumerate(fcoord):
            ax.annotate(f'f(x) = {"%.5f" % value}, i = {i}', (coord[i][0], coord[i][1]))
        pt.show()    