"""This module contains visualization of the sensitivity of As.
"""

import numpy as np 
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from matplotlib import colors

import matplotlib
import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.collections import PolyCollection
from matplotlib import colors as mcolors
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import cm

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement

fig = plt.figure()
ax = fig.gca(projection='3d')
# ax.set_aspect("equal") 

#bottom and top surface
def x_y_edge(x_range, y_range, z_range):
    xx, yy = np.meshgrid(x_range, y_range)
    z1 = np.ones_like(xx)*(z_range[0])
    z2 = np.ones_like(xx)*(z_range[1])
   
 

    for i in [0, 1]:
        if i == 0:
            ax.plot_wireframe(xx, yy, z1, color="darkgrey")
            ax.plot_surface(xx, yy, z1, color="blue", alpha=0.5)
        else:
            ax.plot_wireframe(xx, yy, z2, color="darkgrey")
            ax.plot_surface(xx, yy, z2, color="blue", alpha=0.5)


def y_z_edge(x_range, y_range, z_range):
    yy, zz = np.meshgrid(y_range, z_range)
    x1 = np.ones_like(yy)*(x_range[0])
    x2 = np.ones_like(yy)*(x_range[1])

    for i in [0, 1]:
        if i == 0:
            ax.plot_wireframe(x1, yy, zz, color="darkgrey")
            ax.plot_surface(x1, yy, zz, color="blue", alpha=0.5)
        else:
            ax.plot_wireframe(x2, yy, zz, color="darkgrey")
            ax.plot_surface(x2, yy, zz, color="blue", alpha=0.5)



def x_z_edge(x_range, y_range, z_range):
    xx, zz = np.meshgrid(x_range, z_range)
    y1 = np.ones_like(xx)*(y_range[0])
    y2 = np.ones_like(xx)*(y_range[1])

    for i in [0, 1]:
        if i == 0:
            ax.plot_wireframe(xx, y1, zz, color="darkgrey")
            ax.plot_surface(xx, y1, zz, color="blue", alpha=0.5)
        else:
            ax.plot_wireframe(xx, y2, zz, color="darkgrey")
            ax.plot_surface(xx, y2, zz, color="blue", alpha=0.5)



def plot_opti_3d(x, f, args):

    x_nodes = list()
    x_sys = list()
    b_sys = list()
    h_sys = list()
    
    for node in args[1].model.nodes:
        x_nodes.append(node._x)

    for i in range(len(x)):
        if i % 2 == 0:
            b_sys.append(x[i].f)
        else:
            h_sys.append(x[i].f)
    
    for i, ele in enumerate(args[1].model.elements):
        if type(ele)==BeamColumnElement:
            _current_vector = ele.get_vector()
        
            a = _current_vector[1]*-1
            b = _current_vector[0]
            _normal_vector = (a,b)
        
            normalized_vector = _normal_vector/np.linalg.norm(_normal_vector)

            v_b = normalized_vector*(x[i*2].f)
            v_h = normalized_vector*(x[i*2+1].f)
           
            x_range = np.array([x_nodes[i], x_nodes[i+1]])
            y_range = np.array([-v_b[1]/2, v_b[1]/2])
            #z_range = np.array([-v_h[1]/2, v_h[1]/2])
            z_range = np.array([-v_h[1], 0])
            
            x_y_edge(x_range, y_range, z_range)
            y_z_edge(x_range, y_range, z_range)
            x_z_edge(x_range, y_range, z_range)


    ax.set_xlim([min(x_nodes), max(x_nodes)])
    ax.set_ylim([-max(x_nodes), max(x_nodes)])
    ax.set_zlim([-max(x_nodes), max(x_nodes)])

    
    _l =np.array(x_nodes)
    _l = np.delete(_l,[0])
    _h = np.array(h_sys)
    l, h = np.meshgrid(_l, _h)
    _b = np.ones_like(l)*(b_sys)
    # Get rid of the panes
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # # Get rid of the ticks
    # ax.set_xticks([]) 
    # ax.set_yticks([]) 
    # ax.set_zticks([])
        
    ax.set_title('Optimiertes Tragwerk')

    ax.set_zlabel('Höhe [m]')
    ax.set_ylabel('Breite [m]')
    ax.set_xlabel('Länge [m]')
    
    plt.contourf(l, _b, h, zdir='z', offset = -2, cmap=cm.coolwarm)
    
   
    
        
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()

