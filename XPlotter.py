# ================================XPlotter.py==================================#
# ================================XPlotter.py==================================#
# Igor G. Irastorza 2020
#
# Description:
# Translation to python of core plotter routines to be used to generate nice
# figures of sensitivity plots, etc`
# ==============================================================================#
# ==============================================================================#
from __future__ import annotations

import pickle

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

PATH_FIGURE_FOLDER = "./plots/"


def custom_formatter(x, pos):
    """Custom formatter for the x and y axis
    It will format the axis in scientific notation,
    except for the values 0.1, 1 and 10.
    """
    # Check if x is one of the values you want to format differently
    if x in [0.1, 1, 10]:
        return f"{x:g}"
    else:
        # For other values, use scientific notation
        return rf"$10^{{{np.log10(x):.0f}}}$"


# ==============================================================================#
# == class representing a generic sensitivity plot
# ==============================================================================#
# ==============================================================================#
class BasePlot:
    """Base class to host a generic sensitivity plot"""

    # ==============================================================================#
    # the class is initialized with info on the limits, axis, etc
    def __init__(
        self,
        xlab="x axis",
        ylab="y axis",
        figsizex=6.5,
        figsizey=5,
        y_min=1.0e-18,
        y_max=1.0e-4,
        x_min=1.0e-11,
        x_max=1.0e9,
        ticksopt_x="normal",
        ticksopt_y="normal",
        labelfontsize=14,
        tickformatter_x=custom_formatter,
        tickformatter_y=custom_formatter,
    ):
        plt.rc("text", usetex=True)
        #plt.rc("font", family="times", size=labelfontsize)
        plt.rc("font", family="serif", serif="cm", size=labelfontsize)
        self.fig = plt.figure(figsize=(figsizex, figsizey))
        self.plot = self.fig.add_subplot(111)

        # axis and labels
        self.plot.set_xlabel(
            xlab, fontsize=labelfontsize, horizontalalignment="right", x=1,
        )
        self.plot.set_ylabel(
            ylab, fontsize=labelfontsize, horizontalalignment="right", y=1,
        )
        self.plot.tick_params(
            which="major", direction="in", right=True, top=True, width=0.8, length=5, pad=6
        )
        self.plot.tick_params(
            which="minor", direction="in", right=True, top=True, width=0.4, length=3, pad=6
        )
        # ,right=TrueopAndRightTicks,top=TopAndRightTicks,pad=7)
        # self.plot.tick_params(which='minor',direction='in',width=1,length=10)
        # ,right=TopAndRightTicks,top=TopAndRightTicks)
        self.plot.set_yscale("log")
        self.plot.set_xscale("log")
        self.plot.set_xlim([x_min, x_max])
        self.plot.set_ylim([y_min, y_max])
        locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        locmin = mpl.ticker.LogLocator(
            base=10.0, subs=np.arange(2, 10) * 0.1, numticks=100
        )
        if ticksopt_x == "dense":
            locmaj = mpl.ticker.LogLocator(base=100.0, subs=(1.0,), numticks=100)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        self.plot.xaxis.set_major_locator(locmaj)
        self.plot.xaxis.set_minor_locator(locmin)

        locmaj = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        locmin = mpl.ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=100)
        if ticksopt_y == "dense":
            locmaj = mpl.ticker.LogLocator(base=100.0, subs=(1.0,), numticks=100)
            locmin = mpl.ticker.LogLocator(base=10.0, subs=(1.0,), numticks=100)
        self.plot.yaxis.set_major_locator(locmaj)
        self.plot.yaxis.set_minor_locator(locmin)

        if tickformatter_x is not None:
            self.plot.xaxis.set_major_formatter(tickformatter_x)
        if tickformatter_y is not None:
            self.plot.yaxis.set_major_formatter(tickformatter_y)
        self.plot.xaxis.set_minor_formatter(mpl.ticker.NullFormatter())
        self.plot.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())

        self.zorder = -100

        self.dragged = None  # store the dragged text object

    # ==============================================================================#
    # will draw a new exclusion line to the plot, no to be filled
    #
    def AddPlotItem(self, typeitem, linename, data, **kwargs):
        y_top = self.plot.get_ylim()[1]
        y_bottom = self.plot.get_ylim()[0]
        kwargs["zorder"] = self.zorder
        if typeitem not in ["band", "line", "region", "fog"]:
            print("ERROR: item type" + typeitem + "not known")
            exit()
        if typeitem == "band":
            self.plot.fill_between(data[:, 0], data[:, 1], y2=y_top, **kwargs)
        if typeitem == "region":
            plt.fill(data[:, 0], data[:, 1], **kwargs)
        if typeitem == "line":
            self.plot.plot(data[:, 0], data[:, 1], **kwargs)
        if typeitem == "fog":
            self.plot.fill_between(data[:, 0], data[:, 1], y2=y_bottom / 10, **kwargs)
        self.zorder += 1

    def on_click(self, event):
        if event.button == 3: # right click
            print(
                "Right click: x=%d, y=%d, xdata=%.3g, ydata=%.3g"
                % (
                    event.x if event.x is not None else -1,
                    event.y if event.y is not None else -1,
                    event.xdata if event.xdata is not None else -1,
                    event.ydata if event.ydata is not None else -1,
                )
            )

    def on_pick(self, event):
        "Store which text object was picked and were the pick event occurs."

        if isinstance(event.artist, mpl.text.Text):
            self.dragged = event.artist
        return True

    def on_release(self, event):
        "Update text position and redraw"

        if self.dragged is not None:
            old_pos = self.dragged.get_position()
            new_pos = (event.xdata, event.ydata)
            if new_pos[0] is None or new_pos[1] is None:
                print("WARNING: new position is out of limits, not moving text.")
                self.dragged = None
                return False

            self.dragged.set_position(new_pos)
            print(
                "%s, %.3g, %.3g, size=%d, rotation=%d"
                % (
                    self.dragged.get_text().replace("\n", "\\n"),
                    self.dragged.get_position()[0],
                    self.dragged.get_position()[1],
                    self.dragged.get_fontsize(),
                    self.dragged.get_rotation(),
                )
            )
            self.dragged = None
            plt.draw()
        return True

    def on_scroll(self, event):
        "Increase or decrease text size"

        if self.dragged is not None:
            old_size = self.dragged.get_fontsize()
            new_size = old_size + event.step
            if new_size < 1:
                new_size = 1
            if new_size == old_size:
                return False
            self.dragged.set_fontsize(new_size)
            # print("Changed text %s size to %.3g" % (self.dragged.get_text(), new_size))
            plt.draw()

    def on_key(self, event):
        "Rotate text"

        if self.dragged is not None:
            old_rotation = self.dragged.get_rotation()
            rot = 0
            if event.key == "+":
                rot = 1
            elif event.key == "*":
                rot = 10
            elif event.key == "-":
                rot = -1
            elif event.key == "/":
                rot = -10
            new_rotation = old_rotation + rot
            self.dragged.set_rotation(new_rotation)
            # print("Rotated text %s to %.3g" % (self.dragged.get_text(), new_rotation))
            plt.draw()

    # ==============================================================================#
    # switch to interactive mode and shows the plot on screen
    #
    def ShowPlot(self):
        cid_rclick = self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        cid_pick = self.fig.canvas.mpl_connect("pick_event", self.on_pick)
        cid_release = self.fig.canvas.mpl_connect(
            "button_release_event", self.on_release
        )
        cid_scroll = self.fig.canvas.mpl_connect("scroll_event", self.on_scroll)
        cid_key = self.fig.canvas.mpl_connect("key_press_event", self.on_key)
        plt.ioff()
        print("Showing plot... Close the figure window to continue.")
        plt.show()
        self.fig.canvas.mpl_disconnect(cid_rclick)
        self.fig.canvas.mpl_disconnect(cid_pick)
        self.fig.canvas.mpl_disconnect(cid_release)
        self.fig.canvas.mpl_disconnect(cid_scroll)
        self.fig.canvas.mpl_disconnect(cid_key)

    # ==============================================================================#
    # saves the plot on a file
    #
    def SavePlot(self, plotname):
        filename = PATH_FIGURE_FOLDER + plotname

        extensions = [".pdf", ".png", ".svg", ".pickle"]
        # if it does not end with any of this extensions add .pdf as default extension
        if not any(plotname.endswith(ext) for ext in extensions):
            filename = filename + ".pdf"

        if filename.endswith(".pickle"):
            fil = open(filename, "wb")
            pickle.dump(self.fig, fil)
            print("Saving figure as " + filename)
            return

        try:
            self.fig.savefig(filename, bbox_inches="tight")
        except FileNotFoundError:
            # if PATH_FIGURE_FOLDER was already added to plotname
            # or plotname included the path to another folder
            filename = filename.replace(PATH_FIGURE_FOLDER, "")
            self.fig.savefig(filename, bbox_inches="tight")
        print("Saving figure as " + filename)


# ==============================================================================#
# class representing a physics item (i.e. excluded region)
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
        if typeitem not in ["band", "region", "line", "fog"]:
            print("ERROR: unknown plot item " + typeitem)
        self.data = []
        try:
            self.data = np.loadtxt(filename)
        except ValueError:
            delimiters = [" ", ",", ";"]
            for dlmt in delimiters:
                try:
                    self.data = np.loadtxt(filename, delimiter=dlmt)
                    break
                except ValueError:
                    pass
            if len(self.data) == 0:
                print(
                    "ERROR: could not load data from file "
                    + filename
                    + ". Check the delimiter is within:",
                    delimiters,
                )
                exit()
        # self.data = loadtxt(filename)

    def DrawItem(self, plot):
        print("->", self.name, self.filename, self.drawopt)
        plot.AddPlotItem(self.typeitem, self.name, self.data, **self.drawopt)


# ==============================================================================#
# ==============================================================================#
# ==============================================================================#
