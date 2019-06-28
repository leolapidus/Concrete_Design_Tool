"""This module contains visualization of the sensitivity of As.
"""

import numpy as np 
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
from matplotlib import colors

import matplotlib
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator


def visualization_sensitivity_as(b, h, As, b_min, b_max, h_min, h_max):

    #fig, ax = plt.subplots()
    As_max = np.amax(As)
    As_min = np.amin(As)

    intervall_As = np.linspace(As_max, As_min, 5)
    intervall_b = b[1]-b[0]
    db = intervall_b/2
    intervall_h = h[1]-h[0]
    dh = intervall_h/2


    y, x = np.mgrid[slice(h_min, h_max + intervall_h, intervall_h),
                    slice(b_min, b_max + intervall_b, intervall_b)]

    # levels = MaxNLocator(nbis='auto').tick_values(As_min, As_max)
    levels = np.linspace(As_min, As_max, 10)
    cmap = plt.get_cmap('plasma')
    
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    fig, ax = plt.subplots()

    im = ax.pcolormesh(x, y, As, cmap=cmap, norm=norm)
    fig.colorbar(im, ax=ax).set_label('Biegebewehrung As [cm²]')
    
    ax.set_title('Designraum der Biegebewehrung')
    ax.set_ylabel('Höhe [m]')
    ax.set_xlabel('Breite [m]')

    plt.show()


def visualization_sensitivity_asw(b, h, asw, b_min, b_max, h_min, h_max):

    asw_max = np.amax(asw)
    asw_min = np.amin(asw)

    intervall_b = b[1]-b[0]
    db = intervall_b/2
    intervall_h = h[1]-h[0]
    dh = intervall_h/2

    y, x = np.mgrid[slice(h_min, h_max + intervall_h, intervall_h),
                    slice(b_min, b_max + intervall_b, intervall_b)]

    # levels = MaxNLocator(nbis='auto').tick_values(As_min, As_max)
    levels = np.linspace(asw_min, asw_max)
    cmap = plt.get_cmap('plasma')
    
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    fig, ax = plt.subplots()

    im = ax.pcolormesh(x, y, asw, cmap=cmap, norm=norm)
    fig.colorbar(im, ax=ax).set_label('Querkraftbewehrung [cm²/m]')
    
    ax.set_title('Designraum der Querkraftbewehrung')
    ax.set_ylabel('Höhe [m]')
    ax.set_xlabel('Breite [m]')

    plt.show()

