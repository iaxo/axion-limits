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
from abc import ABC, abstractmethod
from .utils import resolve_relative_path, get_absolute_path
from .utils import is_latex_installed, latex_to_plain_text
from .utils import extract_kwargs, custom_formatter


# ==============================================================================#
# == class representing a generic sensitivity plot
# ==============================================================================#
# ==============================================================================#
class BasePlot(ABC):
    """Base class to host a generic sensitivity plot"""

    # ==============================================================================#
    # the class is initialized with info on the limits, axis, etc
    def __init__(
        self,
        saveplotname=None,
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
        self._uselatex = is_latex_installed()
        if self._uselatex:
            plt.rc("text", usetex=True)
            plt.rc("font", family="serif", size=labelfontsize)
            plt.rc("font", family="serif", serif="cm", size=labelfontsize)
            
        self.fig = plt.figure(figsize=(figsizex, figsizey))
        self.plot = self.fig.add_subplot(111)

        # axis and labels
        self.plot.set_xlabel(
            xlab,
            fontsize=labelfontsize,
            horizontalalignment="right",
            x=1,
        )
        self.plot.set_ylabel(
            ylab,
            fontsize=labelfontsize,
            horizontalalignment="right",
            y=1,
        )
        self.plot.tick_params(
            which="major",
            direction="in",
            right=True,
            top=True,
            width=0.8,
            length=5,
            pad=6,
        )
        self.plot.tick_params(
            which="minor",
            direction="in",
            right=True,
            top=True,
            width=0.4,
            length=3,
            pad=6,
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
        locmin = mpl.ticker.LogLocator(
            base=10.0, subs=np.arange(2, 10) * 0.1, numticks=100
        )
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
        self.anchor_point = None  # store the anchor point of the dragged text object
        self.saveplotname = saveplotname

    # ==============================================================================#
    # will draw a new exclusion line to the plot, no to be filled
    #
    def add_plot_item(self, typeitem, linename, data, **kwargs):
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

    def plot_labels(self, labels: list):
        print("Plotting labels:")
        for label in labels:
            kwargs = {}
            if type(label[3]) == str:
                kwargs = extract_kwargs(label[3])
            elif type(label[3]) == dict:
                kwargs = label[3]
            # if "picker" not in kwargs:
            #   kwargs["picker"] = True
            text = label[0]
            if not self._uselatex:
                text = latex_to_plain_text(label[0])
            print("->", text, label[1], label[2], kwargs)
            self.plot.text(x=label[1], y=label[2], s=text, **kwargs)
    
    @abstractmethod
    def plot_data(self, data: list):
        pass

    def on_click(self, event):
        if event.button == 3:  # right click
            print(
                "Right click: x=%d, y=%d, xdata=%.3g, ydata=%.3g"
                % (
                    event.x if event.x is not None else -1,
                    event.y if event.y is not None else -1,
                    event.xdata if event.xdata is not None else -1,
                    event.ydata if event.ydata is not None else -1,
                )
            )
            # remove anchor point if it exists
            if self.anchor_point is not None:
                self.anchor_point.remove()
                self.anchor_point = None
                plt.draw()

    def on_pick(self, event):
        "Store which text object was picked and were the pick event occurs."
        if event.mouseevent.button != 1:
            return False
        if isinstance(event.artist, mpl.text.Text):
            self.dragged = event.artist
            # self.dragged.set_bbox(dict(facecolor="None", edgecolor="black", alpha=0.5, boxstyle="square,pad=0.01"))
            self.dragged.set_rotation_mode("anchor")
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
            if self.anchor_point is not None:
                self.anchor_point.remove()
            self.anchor_point = self.plot.scatter(
                self.dragged.get_position()[0],
                self.dragged.get_position()[1],
                s=5,
                color="red",
                alpha=0.5,
            )
            print(
                "%s, %.3g, %.3g, size=%d, rotation=%d"
                % (
                    self.dragged.get_text().replace("\n", "\\n"),
                    self.dragged.get_position()[0],
                    self.dragged.get_position()[1],
                    self.dragged.get_fontsize(),
                    self.dragged.get_rotation(),
                ),
                (
                    ", rotation_mode=" + self.dragged.get_rotation_mode()
                    if self.dragged.get_rotation() != 0
                    else ""
                ),
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
    def show_plot(self):
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
    def save_plot(self, plot_name=""):
        if plot_name != "":
            self.saveplotname = plot_name
        if self.saveplotname is None or self.saveplotname == "":
            raise ValueError("No filename specified for saving the plot.")

        if self.anchor_point is not None:
            self.anchor_point.remove()
            self.anchor_point = None

        filename = self.saveplotname
        extensions = [".pdf", ".png", ".svg", ".pickle"]
        # if it does not end with any of this extensions add .pdf as default extension
        if not any(filename.endswith(ext) for ext in extensions):
            filename = filename + ".pdf"

        if filename.endswith(".pickle"):
            fil = open(filename, "wb")
            pickle.dump(self.fig, fil)
            print("Saving figure as " + filename)
            return

        self.fig.savefig(filename, bbox_inches="tight")
        print("Saving figure as " + filename)
        self.saveplotname = filename


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
        self.short_filename = filename
        self.filename = get_absolute_path(self.short_filename, 'axionlimits.data')
        self.drawopt = kwargs
        if typeitem not in ["band", "region", "line", "fog"]:
            raise ValueError("item type " + typeitem + " not known")
        self.data = []
        try:
            self.data = np.loadtxt(self.filename)
        except ValueError:
            delimiters = [" ", ",", ";"]
            for dlmt in delimiters:
                try:
                    self.data = np.loadtxt(self.filename, delimiter=dlmt)
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
                raise ValueError("Could not load data from file " + filename)

        # self.data = loadtxt(filename)

    def draw_item(self, plot):
        print("->", self.name, self.short_filename, self.drawopt)
        plot.add_plot_item(self.typeitem, self.name, self.data, **self.drawopt)


# ==============================================================================#
# ==============================================================================#
# ==============================================================================#
