"""This module contains the steepest descent algorithm
"""
import numpy as np 
import hyperjet as hj
import matplotlib.pyplot as pt
from numpy.testing import assert_almost_equal
from Visualization.plot_opti_as import plot_opti_as
from Visualization.plot_opti_asw import plot_opti_asw
from Visualization.plot_opti_3d import plot_opti_3d


def steepest_descent(f, x, solvertype, args, g, h):
   
    if solvertype == 'linear':
        
        # coord = []
        # fcoord = []
        # miter = 1
        # step = 0.01/miter
        # max_int = 10
        # fcoord.append(f(x,args))
        # coord.append((x[0].f, x[1].f))
        # print(x, f(x,args), g(x,args), h(x,args), 0)
        
        # while miter <= max_int:
        #     temp = x-step*g(x,args)
            
        #     if np.abs(f(x,args)-f(temp,args))>0.0000001:
        #         x=temp         
        #     else:
        #         break
        #     coord.append((x[0].f, x[1].f))
        #     fcoord.append(f(x,args))
        #     print(x, f(x,args), g(x,args), miter)
        #     miter += 1
        
        # fig, ax = pt.subplots()
        # pt.axis("equal")
        # ax.set_title('Steepest Descent \n linearer line search')
        # ax.set_ylabel('Höhe [m]')
        # ax.set_xlabel('Breite [m]')
        # coord_array = np.array(coord)
        # t=coord_array.T[0]
        # pt.plot(coord_array.T[0], coord_array.T[1], "x-")
        # for i, value in enumerate(fcoord):
        #     if not i % 5 or i == len(fcoord):
        #         ax.annotate(f'f(x) = {"%.5f" % value}, i = {i}', (coord[i][0], coord[i][1]))
            
        # pt.show() 




#test
        coord = []
        fcoord = []
        miter = 1
        step = 0.02/miter
        max_int = 1
        fcoord.append(f(x,args))
        i_coord = len(x)
        for i in range(int(len(x)/2)):
            coord.append((x[i*2].f, x[i*2+1].f))
        #print(x, 0)
        
        while miter <= max_int:
            p=[step*d for d in g(x,args)]
            temp=[x-p for x, p in zip(x,p)]
            
            
            if np.abs(np.array(f(x,args))-np.array(f(temp,args))).all()>0.0000001:
                x=temp         
            else:
                break
            fcoord.append(f(x,args))
            for i in range(int(len(x)/2)):
                coord.append((x[i*2].f, x[i*2+1].f))
            print(x, miter)
            miter += 1

        #plot_opti_as(x,f(x,args),args)
        #plot_opti_asw(x,f(x,args),args)
        plot_opti_3d(x,f(x,args),args)
        
        fig, ax = pt.subplots()
        pt.axis("equal")
        ax.set_title('Steepest Descent \n linearer line search')
        ax.set_ylabel('Höhe [m]')
        ax.set_xlabel('Breite [m]')
        coord_array = np.array(coord)
        plot_list = []
        for k in range(i_coord):
            plot_list.append([])
        for i in range(len(plot_list)):
            for j in range(int(len(coord)/i_coord)):
                plot_list[i].append(coord[j*i_coord+i])
        plot_list = np.array(plot_list)
        
        
        for s in range(len(plot_list)):
            pt.plot(plot_list[s].T[0], plot_list[s].T[1], "x-")
        
        # for i, value in enumerate(fcoord):
        #     if not i % 5 or i == len(fcoord[1]):
        #         ax.annotate(f'f(x) = {"%.5f" % value[2]}, i = {i}', (coord[i][0], coord[i][1]))
            
        pt.show() 

    elif solvertype == 'hessian':    
        
        coord = []
        fcoord = []   # for plotting
        fcoord.append(f(x,args))
        coord.append((x[0].f, x[1].f))
        print(x, f(x,args), g(x,args), h(x,args),0)

        for k in range(10):
           
            for j in range(len(h(x,args))):
                if h(x,args)[j,j] < 10e-15:
                    h(x,args)[j,j]=0
                else:
                    pass 
            w=np.linalg.inv(h(x,args))
            r=np.dot(w,g(x,args))
            c = np.linalg.solve(h(x,args), g(x,args))
            print(c)
            x_new = [0]*len(x)
            if np.linalg.norm(c) > 1.0:
                #c *= 0.01
                c /= np.linalg.norm(c) * 0.01

            for n in range(len(x)):
                if c[n] is not None:
                    x_new[n] = x[n]-c[n]
                else:
                    x_new[n] = x[n]

            for p in range(len(x_new)):
                
                if x_new[p].f > -10e-8 and x_new[p].f < 10e-8:
                    x_new[p].f = 0.0
                       
            if abs(f(x, args)-f(x_new, args)) > 0.000001:
                x = x_new
            else:
                print('Lösung mue_eds =', f(x,args))
                break
            fcoord.append(f(x,args))
            coord.append((x[0].f, x[1].f))
            print(x, f(x, args), h(x,args), k)
            
            
        fig, ax = pt.subplots()
        pt.axis("equal")
        ax.set_title('Steepest Descent \n linearer line search')
        ax.set_ylabel('Höhe [m]')
        ax.set_xlabel('Breite [m]')
        coord_array = np.array(coord)
        t=coord_array.T[0]
        pt.plot(coord_array.T[0], coord_array.T[1], "x-")
        for i, value in enumerate(fcoord):
            if not i % 5 or i == len(fcoord):
                ax.annotate(f'f(x) = {"%.5f" % value}, i = {i}', (coord[i][0], coord[i][1]))
            
        pt.show()    