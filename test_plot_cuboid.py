# def plot_cuboid(center, size):
#     """
#        Create a data array for cuboid plotting.


#        ============= ================================================
#        Argument      Description
#        ============= ================================================
#        center        center of the cuboid, triple
#        size          size of the cuboid, triple, (x_length,y_width,z_height)
#        :type size: tuple, numpy.array, list
#        :param size: size of the cuboid, triple, (x_length,y_width,z_height)
#        :type center: tuple, numpy.array, list
#        :param center: center of the cuboid, triple, (x,y,z)
#    """
#     # suppose axis direction: x: to left; y: to inside; z: to upper
#     # get the (left, outside, bottom) point
#     import numpy as np
#     ox, oy, oz = center
#     l, w, h = size

#     x = np.linspace(ox-l/2,ox+l/2,num=10)
#     y = np.linspace(oy-w/2,oy+w/2,num=10)
#     z = np.linspace(oz-h/2,oz+h/2,num=10)
#     x1, z1 = np.meshgrid(x, z)
#     y11 = np.ones_like(x1)*(oy-w/2)
#     y12 = np.ones_like(x1)*(oy+w/2)
#     x2, y2 = np.meshgrid(x, y)
#     z21 = np.ones_like(x2)*(oz-h/2)
#     z22 = np.ones_like(x2)*(oz+h/2)
#     y3, z3 = np.meshgrid(y, z)
#     x31 = np.ones_like(y3)*(ox-l/2)
#     x32 = np.ones_like(y3)*(ox+l/2)

#     from mpl_toolkits.mplot3d import Axes3D
#     import matplotlib.pyplot as plt
#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#     # outside surface
#     ax.plot_wireframe(x1, y11, z1, color='b', rstride=1, cstride=1, alpha=0.6)
#     # inside surface
#     ax.plot_wireframe(x1, y12, z1, color='b', rstride=1, cstride=1, alpha=0.6)
#     # bottom surface
#     ax.plot_wireframe(x2, y2, z21, color='b', rstride=1, cstride=1, alpha=0.6)
#     # upper surface
#     ax.plot_wireframe(x2, y2, z22, color='b', rstride=1, cstride=1, alpha=0.6)
#     # left surface
#     ax.plot_wireframe(x31, y3, z3, color='b', rstride=1, cstride=1, alpha=0.6)
#     # right surface
#     ax.plot_wireframe(x32, y3, z3, color='b', rstride=1, cstride=1, alpha=0.6)
    
#     ax.set_xlabel('X')
#     ax.set_xlim(-100, 100)
#     ax.set_ylabel('Y')
#     ax.set_ylim(-100, 100)
#     ax.set_zlabel('Z')
#     ax.set_zlim(-100, 100)
#     plt.show()



# def test():
#     center = [0, 0, 0]
#     length = 32 * 2
#     width = 50 * 2
#     height = 100 * 2
#     plot_cuboid(center, (length, width, height))


# if __name__ == '__main__':
#     test()



from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

file_path = "./3D_surface_and_contour.jpg"
p = 0.05
f = -0.01

def get_data(p):
    x, y, z = axes3d.get_test_data(p)
    z = f * z
    return x, y, z

def plot_3d_contour(p, f):
    nrows = 4
    ncols = 5

    x, y, z = get_data(p)

    x_min, x_max = np.min(x), np.max(x)
    y_min, y_max = np.min(y), np.max(y)
    z_min, z_max = np.min(z), np.max(z)

    fig = plt.figure(figsize=(15, 10))
    for n in range(nrows * ncols):
        i = n % ncols
        j = n / ncols
        k = n + 1
        if j == 0:
            azim = -60 + (i - 2) * 15
            elev = 30
        elif j == 1:
            azim = -60
            elev = 30 + (i - 2) * 5
        elif j == 2:
            azim = 60 + (i - 2) * 10
            elev = 30
        elif j == 3:
            azim = 60
            elev = 30 + (i - 2) * 5
        ax = fig.add_subplot(nrows, ncols, k, projection='3d')
        ax.set_title("azim=" + str(azim) + " elev=" + str(elev))
        ax.tick_params(labelsize=8)
        ax.view_init(azim=azim, elev=elev)
        ax.plot_surface(x, y, z, rstride=10, cstride=10, alpha=0.3)
        ax.contourf(x, y, z, zdir='z', offset=z_min, cmap=cm.coolwarm)
        ax.contourf(x, y, z, zdir='x', offset=x_min, cmap=cm.coolwarm)
        if j == 0 or j == 1:
            ax.contourf(x, y, z, zdir='y', offset=y_max, cmap=cm.coolwarm)
        elif j == 2 or j == 3:
            ax.contourf(x, y, z, zdir='y', offset=y_min, cmap=cm.coolwarm)

        ax.set_xlabel('X')
        ax.set_xlim(x_min, x_max)
        ax.set_ylabel('Y')
        ax.set_ylim(y_min, y_max)
        ax.set_zlabel('Z')
        ax.set_zlim(z_min, z_max)

    plt.savefig(file_path, dpi=80)
    plt.show()

plot_3d_contour(p, f)