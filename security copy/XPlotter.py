# ================================XPlotter.py==================================#
# ================================XPlotter.py==================================#
# Igor G. Irastorza 2020
#
# Description:
# Translation to python of core plotter routines to be used to generate nice
# figures of sensitivity plots, etc`
# ==============================================================================#
# ==============================================================================#

import os
from numpy import *
from numpy.random import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from matplotlib import colors
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cm
import pickle

plotpdfdir = './plots_test/'
plotpngdir = plotpdfdir + 'pngs/'


# ==============================================================================#
# == class representing a generic sensitivity plot
# ==============================================================================#
# ==============================================================================#

class BasePlot():
    """Base class to host a generic sensitivity plot"""

    # ==============================================================================#
    # the class is initialized with info on the limits, axis, etc
    def __init__(self, xlab='x axis', ylab='y axis', \
                 figsizex=6.5, figsizey=5, \
                 y_min=1.0e-18, y_max=1.0e-4, \
                 x_min=1.0e-11, x_max=1.0e9, \
                 ticksopt_x="normal", ticksopt_y="normal",
                 labelfontsize=14):

        plt.rc('text', usetex=True)
        plt.rc('font', family='times', size=labelfontsize)
        self.fig = plt.figure(figsize=(figsizex, figsizey))
        self.plot = self.fig.add_subplot(111)

        # axis and labels
        self.plot.set_xlabel(xlab, fontsize=labelfontsize, horizontalalignment='right', x=1)
        self.plot.set_ylabel(ylab, fontsize=labelfontsize, horizontalalignment='right', y=1)
        self.plot.tick_params(which='major', direction='in', right=True, top=True, width=0.8, length=5)
        self.plot.tick_params(which='minor', direction='in', right=True, top=True, width=0.4, length=3)
        # ,right=TrueopAndRightTicks,top=TopAndRightTicks,pad=7)
        # self.plot.tick_params(which='minor',direction='in',width=1,length=10)
        # ,right=TopAndRightTicks,top=TopAndRightTicks)
        self.plot.set_yscale('log')
        self.plot.set_xscale('log')
        self.plot.set_xlim([x_min, x_max])
        self.plot.set_ylim([y_min, y_max])
        locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10) * .1, numticks=100)
        if (ticksopt_x == 'dense'):
            locmaj = mpl.ticker.LogLocator(base=100.0, subs=(1.0,), numticks=100)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        self.plot.xaxis.set_major_locator(locmaj)
        self.plot.xaxis.set_minor_locator(locmin)
        self.plot.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
        locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        locmin = mpl.ticker.LogLocator(base=10.0, subs=arange(2, 10) * .1, numticks=100)
        if (ticksopt_x == 'dense'):
            locmin = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        self.plot.yaxis.set_major_locator(locmaj)
        self.plot.yaxis.set_minor_locator(locmin)
        self.plot.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())

        self.zorder = -100

    # ==============================================================================#
    # will draw a new exclusion line to the plot, no to be filled
    #
    def AddPlotItem(self, typeitem, linename, data, **kwargs):
        y2 = self.plot.get_ylim()[1]
        kwargs['zorder'] = self.zorder
        if (typeitem not in ['band', 'line', 'region']):
            print('ERROR: item type' + typeitem + 'not known')
            exit()
        if (typeitem == "band"):
            self.plot.fill_between(data[:, 0], data[:, 1], y2=y2, **kwargs)
        if (typeitem == "region"):
            plt.fill(data[:, 0], data[:, 1], **kwargs)
        if (typeitem == "line"):
            self.plot.plot(data[:, 0], data[:, 1], **kwargs)
        self.zorder += 1

    # #==============================================================================#
    # # will draw a new exclusion line to the plot, no to be filled
    # #
    # def AddPlotLine(self,linename,data,**kwargs):
    #     y2 = self.plot.get_ylim()[1]
    #     kwargs['zorder']=self.zorder
    #     self.plot.plot(data[:,0], data[:,1],**kwargs)
    #     self.zorder+=1

    # #==============================================================================#
    # # will draw a new exclusion line to the plot (defined as a line and everything
    # # above it is excluded (i.e. potentially filled)
    # #
    # def AddPlotBand(self,linename,data,**kwargs):
    #     y2 = self.plot.get_ylim()[1]
    #     kwargs['zorder']=self.zorder
    #     self.plot.fill_between(data[:,0], data[:,1], y2=y2, **kwargs)
    #     self.zorder+=1

    # #==============================================================================#
    # # will draw a new (exclusion) region to the plot (defined as a closed contour
    # # that is potentially filled
    # #
    # def AddPlotRegion(self,linename,data,**kwargs):
    #     y2 = self.plot.get_ylim()[1]
    #     kwargs['zorder']=self.zorder
    #     plt.fill(data[:,0], data[:,1],**kwargs)
    #     self.zorder+=1

    def onclick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%g, ydata=%gf' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

    # ==============================================================================#
    # switch to interactive mode and shows the plot on screen
    #
    def ShowPlot(self):
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.ioff()
        plt.show()
        self.fig.canvas.mpl_disconnect(cid)

    # ==============================================================================#
    # saves the plot on a file
    #
    def SavePlot(self, plotname, pngsave=False, openpdf=False, picklesave=False):
        filename = plotpdfdir + plotname + '.pdf'
        self.fig.savefig(filename, bbox_inches='tight')
        print(filename + " saved.")

        if pngsave:
            self.fig.savefig(plotpngdir + plotname + '.png', bbox_inches='tight')
            print(filename + ".png saved.")

        if openpdf:
            os.startfile(filename)
            print(filename)

        if picklesave:
            fil = open(plotpdfdir + plotname + ".pickle", "wb")
            pickle.dump(self.fig, fil)
            print(plotpdfdir + plotname + ".pickle saved.")


# ==============================================================================#
# class representing an physics item (i.e. excluded region)
# to be drawn on plot
# useful to create the object but decide later if to be plotted or not
# ==============================================================================#
# ==============================================================================#
class ExPltItem:

    # ==============================================================================#
    # the object just contains the same info that I would pass when plotting...
    #
    def __init__(self, name, typeitem, filename, **kwargs):
        self.name = name
        self.typeitem = typeitem
        self.filename = filename
        self.drawopt = kwargs
        if typeitem not in ["band", "region", "line"]:
            print("ERROR: unknown plot item " + typeitem)
        self.data = loadtxt(filename)

    def DrawItem(self, plot):
        print(self.name, self.filename, self.drawopt)
        plot.AddPlotItem(self.typeitem, self.name, self.data, **self.drawopt)
        # if (self.typeitem == "band"):
        #     plot.AddPlotBand(self.name,data,**self.drawopt)
        # if (self.typeitem == "region"):
        #     plot.AddPlotRegion(self.name,data,**self.drawopt)
        # if (self.typeitem == "line"):
        #     plot.AddPlotLine(self.name,data,**self.drawopt)

# ==============================================================================#
# ==============================================================================#
# ==============================================================================#
