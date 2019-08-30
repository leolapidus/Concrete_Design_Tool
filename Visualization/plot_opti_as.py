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

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement


def plot_opti_as(x, f, args):

    x_sys=list()
    y_sys=list()
    x_b = list()
    y_b = list()
    x_h = list()
    y_h = list()
    x_reinf = list()
    y_reinf = list()
    for node in args[1].model.nodes:
            x_sys.append(node._x)
            y_sys.append(node._y)
    
    for i, ele in enumerate(args[1].model.elements):
        if type(ele)==BeamColumnElement:
            _current_vector = ele.get_vector()
        
            a = _current_vector[1]*-1
            b = _current_vector[0]
            _normal_vector = (a,b)
        
            normalized_vector = _normal_vector/np.linalg.norm(_normal_vector)

            v_1 = normalized_vector*(x[i][0]/1)
            v_2 = normalized_vector*(x[i][1]/1)
            if ele.local_internal_forces[2] > -1e-6:
                v_3 = -1*normalized_vector*(f[i]/10)
            else:
                v_3 = normalized_vector*(f[i]/10)
            

            x_b.append(ele.nodes[0]._x+v_1[0])
            x_b.append(ele.nodes[1]._x+v_1[0])
            y_b.append(ele.nodes[0]._y+v_1[1])
            y_b.append(ele.nodes[1]._y+v_1[1])

            x_h.append(ele.nodes[0]._x+v_2[0])
            x_h.append(ele.nodes[1]._x+v_2[0])
            y_h.append(ele.nodes[0]._y+v_2[1])
            y_h.append(ele.nodes[1]._y+v_2[1])

            x_reinf.append(ele.nodes[0]._x+v_3[0])
            x_reinf.append(ele.nodes[1]._x+v_3[0])
            y_reinf.append(ele.nodes[0]._y+v_3[1])
            y_reinf.append(ele.nodes[1]._y+v_3[1])


    fig, ax = plt.subplots(1,3)
    for l in range(3):
        ax[l].plot(x_sys, y_sys, 'k')
    
    
    x_i = []
    for i in range(len(x_sys)):
        x_i.append(x_sys[i])
        x_i.append(x_sys[i])
    del x_i[0]
    del x_i[-1]

    y_i = []
    for i in range(len(y_sys)):
        y_i.append(y_sys[i])
        y_i.append(y_sys[i])
    del y_i[0]
    del y_i[-1]
    
    #Change of width

    segments_b = list()
    
    for i in range(len(x_i)):
            segments_b.append(
                [(x_i[i], y_i[i]),
                (x_b[i].f, y_b[i].f)]
            )
    line_segments_b = LineCollection(segments_b, linewidths=0.5, colors='darkgrey')
    ax[0].add_collection(line_segments_b)

    verts_b = list()
    l = int((len(x_i))/2)
    for i in range(l):
            verts_b.append(
                [(x_i[i+i], y_i[i+i]),
                (x_b[i+i].f, y_b[i+i].f),
                (x_b[i+i+1].f, y_b[i+i+1].f),
                (x_i[i+i+1], y_i[i+i+1])]
            )
    poly_verts_b = PolyCollection(verts_b, linewidths=0.5, facecolors= 'lightblue', edgecolors='darkgrey')
    ax[0].add_collection(poly_verts_b)
    ax[0].axis('off')
    # b = "%.3f" % max(b)
    # ax[0].annotate(f'Maximale Längsbewehrung \n{b} cm²', xy=(0,1), xycoords='axes fraction',
    #                 fontsize=9, xytext=(3,-5), textcoords='offset points', ha='left', va='top')
    
    ax[0].autoscale()
    ax[0].axis('equal')
    ax[0].set_title('Änderung der Breite')

    # for i, value in enumerate(self.As):
    #     ax[0].annotate("%.3f" % value, (self.x_As[i+1], self.y_As[i+1]))


#Change of height

    segments_h = list()
    
    for i in range(len(x_i)):
            segments_h.append(
                [(x_i[i], y_i[i]),
                (x_h[i].f, y_h[i].f)]
            )
    line_segments_h = LineCollection(segments_h, linewidths=0.5, colors='darkgrey')
    ax[1].add_collection(line_segments_h)

    verts_h = list()
    l = int((len(x_i))/2)
    for i in range(l):
            verts_h.append(
                [(x_i[i+i], y_i[i+i]),
                (x_h[i+i].f, y_h[i+i].f),
                (x_h[i+i+1].f, y_h[i+i+1].f),
                (x_i[i+i+1], y_i[i+i+1])]
            )
    poly_verts_h = PolyCollection(verts_h, linewidths=0.5, facecolors= 'lightblue', edgecolors='darkgrey')
    ax[1].add_collection(poly_verts_h)
    ax[1].axis('off')
    # b = "%.3f" % max(b)
    # ax[0].annotate(f'Maximale Längsbewehrung \n{b} cm²', xy=(0,1), xycoords='axes fraction',
    #                 fontsize=9, xytext=(3,-5), textcoords='offset points', ha='left', va='top')
    
    ax[1].autoscale()
    ax[1].axis('equal')
    ax[1].set_title('Änderung der Höhe')

    # for i, value in enumerate(self.As):
    #     ax[0].annotate("%.3f" % value, (self.x_As[i+1], self.y_As[i+1]))

#Change of reinforcement

    segments_reinf = list()
    
    for i in range(len(x_i)):
            segments_reinf.append(
                [(x_i[i], y_i[i]),
                (x_reinf[i], y_reinf[i])]
            )
    line_segments_reinf = LineCollection(segments_reinf, linewidths=0.5, colors='darkgrey')
    ax[2].add_collection(line_segments_reinf)

    verts_reinf = list()
    l = int((len(x_i))/2)
    for i in range(l):
            verts_reinf.append(
                [(x_i[i+i], y_i[i+i]),
                (x_reinf[i+i], y_reinf[i+i]),
                (x_reinf[i+i+1], y_reinf[i+i+1]),
                (x_i[i+i+1], y_i[i+i+1])]
            )
    poly_verts_reinf = PolyCollection(verts_reinf, linewidths=0.5, facecolors= 'lightblue', edgecolors='darkgrey')
    ax[2].add_collection(poly_verts_reinf)
    ax[2].axis('off')
    # b = "%.3f" % max(b)
    # ax[0].annotate(f'Maximale Längsbewehrung \n{b} cm²', xy=(0,1), xycoords='axes fraction',
    #                 fontsize=9, xytext=(3,-5), textcoords='offset points', ha='left', va='top')
    
    ax[2].autoscale()
    ax[2].axis('equal')
    ax[2].set_title('Längsbewehrung')

    # for i, value in enumerate(self.As):
    #     ax[0].annotate("%.3f" % value, (self.x_As[i+1], self.y_As[i+1]))

    
    
    # ax.set_title('Designraum der Biegebewehrung')
    # ax.set_ylabel('Höhe [m]')
    # ax.set_xlabel('Breite [m]')
    plt.get_current_fig_manager().window.state('zoomed')
    plt.show()

