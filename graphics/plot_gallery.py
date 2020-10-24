# -*- coding: utf-8 -*-

"""
* author: kristjan axelsson
* date: 12.09.19
*
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import patches as patches
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


class Plots:
    """ ############################### Plots #################################
            #
            #  this modul enables methods to plot lists and numpy array
            #  in different ways.
            #
            #  for specific informations take a look at
            #  the matplotlib documentation:
            #  https://matplotlib.org/
            #
        ------------------------ Detailed Description -------------------------
            #
            #  in the description below:
            #
            #  "self" stands for the instance of the class.
            #  "o" indicates parameter description
            #  ">>" indicates an example of how to use the dataset.
            #  """

    def _new(self, title):
        self.figure = plt.figure()
        axes = self.figure.add_subplot(111, title=title)
        return axes

    def create_axes(self, title='', xlabel='', ylabel='', xlim=None, ylim=None):
        """ #  create a x-axis, and y-axis to plot on it """
        axes = self._new(title)
        axes.grid(alpha=0.8)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(ylabel)
        if ylim: plt.ylim(ylim)
        if xlim: plt.xlim(xlim)
        self.axes, self.axes2 = axes, None

    def create_axes_pair(self, title='', xlabel='', ylabel='', y2label='', xlim=None, ylim=None):
        """ #  create a x-axis, y-axis and y2-axis to plot on it """
        axes = self._new(title)
        axes2 = axes.twinx()
        axes.grid(alpha=0.8)
        axes.set_xlabel(xlabel)
        axes.set_ylabel(y2label, color='tab:blue')
        axes2.set_ylabel(ylabel, color='tab:green')
        if ylim: plt.ylim(ylim)
        if xlim: plt.xlim(xlim)
        self.axes, self.axes2 = axes, axes2

    def save(self, path):
        """ o  path (str): complete filepath """
        self.figure.tight_layout()
        self.figure.savefig(path)

    def show(self):
        plt.show()

    def set_cmap(self, cmap, ncolor):
        """ #  create a colormap for values between 0 and 1
            o  cmap (str): name of colormap
            o  ncolor (int): number of different colors """
        self.cmap = cm.get_cmap(cmap, ncolor)

    def get_color(self, value):
        """ #  read colorvalue of colormap for values between 0 and 1
            o  value (int): value between 0 and 1 """
        return self.cmap(value)

    def single(self, x, y, linestyle='', marker='o', markersize=3, **kwargs):
        """ #  call self.create_axes() before you call this function
            o  x (list): data of x-axis
            o  y (list): data of y-axis """
        self.axes.plot(list(x), list(y), marker=marker, markersize=markersize, linestyle=linestyle, **kwargs)

    def pair(self, x, y1, y2, label1=None, label2=None, marker='o', markersize=3, linestyle='-'):
        """ #  call self.create_axes_pair() before you call this function
            o  x (list): data of x-axis
            o  y1 (list): data of left y-axis
            o  y2 (list): data of right y-axis """
        self.axes.plot(x, y1, label=label1, marker=marker, markersize=markersize, color='tab:blue', linestyle=linestyle,
                       zorder=1)
        self.axes2.plot(x, y2, label=label2, marker=marker, markersize=markersize, color='tab:green',
                        linestyle=linestyle)

    def multiple(self, x, y, legend, line='', marker='o', color=None, markersize=3, **kwargs):
        """ #  call self.create_axes() before you call this function
            o  x (list): data of x-axis
            o  y (list_of_lists): each list is column of data on y-axis
            o  legend (list): labels of each column of data on y-axis """
        if type(line) == str:
            line = [line for _ in legend]
        for yi, li, ls in zip(y, legend, line):
            self.axes.plot(x, yi, marker=marker, markersize=markersize, color=color, linestyle=ls, label=li, **kwargs)
        self.legend_show()

    def legend_reverse(self):
        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend(reversed(handles), reversed(labels))

    def legend_show(self):
        plt.legend()
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)

    def histogram(self, x, title='', xlabel='', classes=None):
        """ o  x (list): data for the histogram """
        if not classes: classes = len(list(set(x))) - 1
        plt.figure()
        plt.xlabel(xlabel)
        plt.ylabel('Counts')
        n, class_border, patches = plt.hist(x, bins=classes)
        plt.title(title)

    def boxplot(self, x):
        """ #  call self.create_axes() before you call this function
            o  x (list): data for the boxplot """
        self.axes.boxplot(x, sym='.')

    def matrixplot(self, z, cmap='seismic', vmin=None, vmax=None):
        """ #  call self.create_axes() before you call this function
            #  create a matrixplot
            #  cmaps = [
                    'binary', 'gist_yarg', 'gist_gray', 'gray',
                    'bone', 'pink', 'spring', 'summer',
                    'autumn', 'winter', 'cool', 'Wistia',
                    'hot', 'afmhot', 'gist_heat', 'copper']
            o  z (numpy.array): 2D-data for the matrixplot """
        m, n = z.shape
        # z = z.transpose()
        x, y = self._make_grid(xMin=0, xMax=n, xStep=n + 1, yMin=0, yMax=m, yStep=m + 1)
        cmap = plt.cm.get_cmap(cmap)
        cmap.set_under('white')
        if vmin is None:
            vmin = np.min(z[np.nonzero(z)])
        if vmax is None:
            vmax = np.abs(z).max()
        im = self.axes.pcolormesh(x, y, z, cmap=cmap, vmin=vmin, vmax=vmax)
        self.figure.colorbar(im)

    def cubicplot(self, z, title='', xlabel='x', ylabel='y', zlabel='z'):
        """ #  create a cubicplot
            o  z (numpy.array): 2D-data for the cubicplot """
        n, m = z.shape
        x, y = self._makeMGrid(xStep=n, yStep=m)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        ax.plot_surface(x, y, z)

    def _make_grid(self, **kwargs):
        return np.meshgrid(np.linspace(kwargs['xMin'], kwargs['xMax'], kwargs['xStep']),
                           np.linspace(kwargs['yMin'], kwargs['yMax'], kwargs['yStep']))

    def _makeMGrid(self, **kwargs):
        return np.mgrid[:kwargs['xStep'], :kwargs['yStep']]


class Drawer:
    """ fill: bool
        hatch: '/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'
        linestyle: '-', '--', '-.', ':', '' """

    def __init__(self, ax=None, xlabel='x [mm]', ylabel='y [mm]'):

        if ax:
            self.ax = ax
        else:

            fig = plt.figure()
            self.ax = fig.add_subplot(111)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

    def line(self, p0, p1, **kwargs):
        obj = patches.ConnectionPatch(p0, p1, coordsA="data", **kwargs)
        self.ax.add_patch(obj)
        self.ax.axis('equal')

    def circle(self, center, radius, **kwargs):
        obj = patches.Circle(xy=center, radius=radius, fill=False, **kwargs)
        self.ax.add_patch(obj)
        self.ax.axis('equal')

    def rect(self, x0, y0, dx, dy, fill=False, **kwargs):
        obj = patches.Rectangle((x0, y0), dx, dy, fill=fill, **kwargs)
        self.ax.add_patch(obj)
        self.ax.axis('equal')

    def ellipse(self, center, width, height, rotation):
        obj = patches.Ellipse(xy=center, width=width, height=height, angle=rotation, fill=False)
        self.ax.add_patch(obj)
        self.ax.axis('equal')


if __name__ is '__main__':
    pass






