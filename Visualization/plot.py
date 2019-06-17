import matplotlib.pyplot as plt 
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib import colors as mcolors
from matplotlib.gridspec import GridSpec

from FE_code.model import Model
from FE_code.beam_column_element import BeamColumnElement

class Plot2D:

    def __init__(self):
        #self.ax, self.fig =plt.subplots()
        self.x = list()
        self.y = list()
        self.x_d = list()
        self.y_d = list()
        self.N = list()
        self.V = list()
        self.M = list()
        self.x_n = list()
        self.y_n = list()
        self.x_v = list()
        self.y_v = list()
        self.x_m = list()
        self.y_m = list()
        self.x_As = list()
        self.y_As = list()
        self.x_asw = list()
        self.y_asw = list()
        self.As = list()
        self.asw = list()


    def geometry(self, model):
        #initial geometry
        for node in model.nodes:
            self.x.append(node._x)
            self.y.append(node._y)

        #deformed geometrie
        for node in model.nodes:
            self.x_d.append(node._x + node.results['u'])
            self.y_d.append(node._y + node.results['v'])


    def internal_forces(self, model):

        for i, ele in enumerate(model.elements):
            if type(ele)==BeamColumnElement:
                self.N.append(ele.local_internal_forces[0])
                self.V.append(ele.local_internal_forces[1])
                self.M.append(ele.local_internal_forces[2])
                self.N.append(ele.local_internal_forces[3]*-1)
                self.V.append(ele.local_internal_forces[4]*-1)
                self.M.append(ele.local_internal_forces[5]*-1)

            
                _current_vector = ele.get_vector()
            
                a = _current_vector[1]*-1
                b = _current_vector[0]
                _normal_vector = (a,b)
            
                normalized_vector = _normal_vector/np.linalg.norm(_normal_vector)

                v_N1 = normalized_vector*(self.N[i+i]/100)
                v_N2 = normalized_vector*(self.N[i+i+1]/100)
                v_V1 = normalized_vector*(self.V[i+i]/100)
                v_V2 = normalized_vector*(self.V[i+i+1]/100)
                v_M1 = normalized_vector*(self.M[i+i]/100)
                v_M2 = normalized_vector*(self.M[i+i+1]/100)

                self.x_n.append(ele.nodes[0]._x+v_N1[0])
                self.x_n.append(ele.nodes[1]._x+v_N2[0])
                self.y_n.append(ele.nodes[0]._y+v_N1[1])
                self.y_n.append(ele.nodes[1]._y+v_N2[1])

                self.x_v.append(ele.nodes[0]._x+v_V1[0])
                self.x_v.append(ele.nodes[1]._x+v_V2[0])
                self.y_v.append(ele.nodes[0]._y+v_V1[1])
                self.y_v.append(ele.nodes[1]._y+v_V2[1])

                self.x_m.append(ele.nodes[0]._x+v_M1[0])
                self.x_m.append(ele.nodes[1]._x+v_M2[0])
                self.y_m.append(ele.nodes[0]._y+v_M1[1])
                self.y_m.append(ele.nodes[1]._y+v_M2[1])

    

    def plot_geometry(self):

        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        ax.plot(self.x_d, self.y_d)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
        plt.axis([0, 5, 0, -1]) #plt.axis([xmin, xmax, ymin, ymax])
    
    def plot_internal_forces(self):
        fig = plt.figure(constrained_layout=True)
        gs = GridSpec(2, 3, figure=fig)
        ax1 = fig.add_subplot(gs[0, :])
        ax2 = fig.add_subplot(gs[1,0])
        ax3 = fig.add_subplot(gs[1,1])
        ax4 = fig.add_subplot(gs[1,2])
        fig.suptitle("FE Berechnung")
        
        x = []
        for i in range(len(self.x)):
            x.append(self.x[i])
            x.append(self.x[i])
        del x[0]
        del x[-1]

        y = []
        for i in range(len(self.x)):
            y.append(self.y[i])
            y.append(self.y[i])
        del y[0]
        del y[-1]

        #Axes 1: show deformed system
        
        ax1.plot(self.x, self.y)
        ax1.plot(self.x_d, self.y_d)
        ax1.set_title('verformter Zustand')

        for i, value in enumerate(self.y_d):
            ax1.annotate(round(value, 3), (self.x_d[i], self.y_d[i]))

        #Axes 2: show normal forces

        ax2.plot(self.x, self.y)
        ax2.plot(self.x_n, self.y_n)
        segments_n = list()
        
        for i in range(len(x)):
                segments_n.append(
                    [(x[i], y[i]),
                    (self.x_n[i], self.y_n[i])]
                )
        line_segments_n = LineCollection(segments_n, linewidths=0.5, colors='lightblue')
        ax2.add_collection(line_segments_n)
        ax2.set_title('Normalkraftverlauf')

        for i, value in enumerate(self.N):
            ax2.annotate(round(value, 3), (self.x_n[i], self.y_n[i]))

        #Axes3: show shear force

        ax3.plot(self.x, self.y)
        ax3.plot(self.x_v, self.y_v)
        segments_v = list()
        
        for i in range(len(x)):
                segments_v.append(
                    [(x[i], y[i]),
                    (self.x_v[i], self.y_v[i])]
                )
        line_segments_v = LineCollection(segments_v, linewidths=0.5, colors='lightblue')
        ax3.add_collection(line_segments_v)
        ax3.set_title('Querkraftverlauf')

        ax3.fill_between(x, self.y_v, y, alpha=0.5)
        
        for i, value in enumerate(self.V):
            ax3.annotate(round(value, 3), (self.x_v[i], self.y_v[i]))

        
        #Axes 4: show bending moment
        #TODO: change direction of plot

        ax4.plot(self.x, self.y)        
        ax4.plot(self.x_m, self.y_m)
        segments_m = list()
        
        for i in range(len(x)):
                segments_m.append(
                    [(x[i], y[i]),
                    (self.x_m[i], self.y_m[i])]
                )
        line_segments_m = LineCollection(segments_m, linewidths=0.5, colors='lightblue')
        ax4.add_collection(line_segments_m)
        ax4.set_title('Momentenverlauf')

        
        ax4.fill_between(x, self.y_m, y, alpha=0.5)

        for i, value in enumerate(self.M):
            ax4.annotate(round(value, 3), (self.x_m[i], self.y_m[i]))
        
        

        plt.show()

    def reinforcement(self, model):

        for i, ele in enumerate(model.elements):
            if type(ele)==BeamColumnElement:
                self.As.append(ele.bending_reinforcement[0])
                self.asw.append(ele.shear_reinforcement[0])

            
                _current_vector = ele.get_vector()
            
                a = _current_vector[1]*-1
                b = _current_vector[0]
                _normal_vector = (a,b)
            
                normalized_vector = _normal_vector/np.linalg.norm(_normal_vector)

                v_1 = normalized_vector*(self.As[i])
                v_2 = normalized_vector*(self.asw[i])
                

                self.x_As.append(ele.nodes[0]._x+v_1[0])
                self.x_As.append(ele.nodes[1]._x+v_1[0])
                self.y_As.append(ele.nodes[0]._y+v_1[1])
                self.y_As.append(ele.nodes[1]._y+v_1[1])

                self.x_asw.append(ele.nodes[0]._x+v_2[0])
                self.x_asw.append(ele.nodes[1]._x+v_2[0])
                self.y_asw.append(ele.nodes[0]._y+v_2[1])
                self.y_asw.append(ele.nodes[1]._y+v_2[1])

    def plot_reinforcement(self):
        

        fig, ax = plt.subplots(1,2)
        ax[0].plot(self.x, self.y)
        ax[1].plot(self.x, self.y)
        
        x = []
        for i in range(len(self.x)):
            x.append(self.x[i])
            x.append(self.x[i])
        del x[0]
        del x[-1]

        y = []
        for i in range(len(self.x)):
            y.append(self.y[i])
            y.append(self.y[i])
        del y[0]
        del y[-1]
        
        ax[0].plot(self.x_As, self.y_As)

        segments_As = list()
        
        for i in range(len(x)):
                segments_As.append(
                    [(x[i], y[i]),
                    (self.x_As[i], self.y_As[i])]
                )
        line_segments_As = LineCollection(segments_As, linewidths=0.5, colors='lightblue')
        ax[0].add_collection(line_segments_As)
        ax[0].set_title('Biegebewehrung')

        ax[0].fill_between(x, self.y_As, y, alpha=0.5)
        
        # for i, value in enumerate(self.As):
        #     ax[0].annotate(round(value, 3), (self.x_As[i+1], self.y_As[i+1]))


        ax[1].plot(self.x_asw, self.y_asw)

        segments_asw = list()
        
        for i in range(len(x)):
                segments_asw.append(
                    [(x[i], y[i]),
                    (self.x_asw[i], self.y_asw[i])]
                )
        line_segments_asw = LineCollection(segments_asw, linewidths=0.5, colors='lightblue')
        ax[1].add_collection(line_segments_asw)
        ax[1].set_title('Querkraftbewehrung')

        ax[1].fill_between(x, self.y_asw, y, alpha=0.5)

        plt.show()


 