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
import matplotlib.patheffects as mplpe
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod
from .utils import resolve_relative_path, get_absolute_path
from .utils import is_latex_installed, latex_to_plain_text
from .utils import extract_kwargs, custom_formatter
from .utils import get_polygon_max_shrink_distance, shrink_mpl_polygon, mpl_to_shapely
from .utils import generate_colors_with_alpha, rgba_to_rgb

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

        self.data_to_plot = []

    # ==============================================================================#
    # will draw a new exclusion line to the plot, no to be filled
    #
    def add_plot_item(self, typeitem, data, **kwargs):
        y_top = self.plot.get_ylim()[1]
        y_bottom = self.plot.get_ylim()[0]
        kwargs["zorder"] = self.zorder
        colorseq = kwargs.pop("cseq", None)
        kwargs.pop("cmap", None) # dont need it here as it has been parsed in ExPltItem
        if typeitem not in ["band", "line", "region", "fog"]:
            raise ValueError("item type " + typeitem + " not known")

        # band is a filled region between the line and the top of the plot
        if typeitem == "band":
            self.plot.fill_between(data[:, 0], data[:, 1], y2=y_top, **kwargs)
            if colorseq is not None:
                is_logscale = self.plot.get_yscale() == "log"
                data_visible = data[data[:, 1] < y_top, :]
                if is_logscale:
                    y_steps = np.logspace(np.log10(data_visible[:, 1]), np.log10(y_top), len(colorseq)+1)
                else:
                    y_steps = np.linspace(data_visible[:, 1], y_top, len(colorseq))
                for i in range(len(colorseq)):
                    y_lower = y_steps[i, :]
                    y_upper = y_steps[i+1, :]
                    color = colorseq[i]
                    self.plot.fill_between(data_visible[:, 0], y_lower, y_upper, color=color, zorder=self.zorder)

        # region is an enclosed region defined by the data points
        if typeitem == "region":
            mpl_pol = self.plot.fill(data[:, 0], data[:, 1], **kwargs)[0]
            if colorseq is not None:
                is_logscale = self.plot.get_xscale() == "log" or self.plot.get_yscale() == "log"
                max_d = get_polygon_max_shrink_distance(mpl_to_shapely(mpl_pol, is_logscale))
                for i in range(len(colorseq)):
                    shrunk_factor = i / len(colorseq)
                    shrunken_pol = shrink_mpl_polygon(mpl_pol, shrunk_factor, max_d, is_logscale)
                    x, y = shrunken_pol.exterior.xy
                    self.plot.fill(x, y, color=colorseq[i], zorder=self.zorder)

        # line is a simple line with no surface filling
        if typeitem == "line":
            self.plot.plot(data[:, 0], data[:, 1], **kwargs)

        # fog is a filled region between the line and the bottom of the plot
        if typeitem == "fog":
            self.plot.fill_between(data[:, 0], data[:, 1], y2=y_bottom / 10, **kwargs)
            if colorseq is not None:
                is_logscale = self.plot.get_yscale() == "log"
                data_visible = data[data[:, 1] > y_bottom, :]
                if is_logscale:
                    y_steps = np.logspace(np.log10(y_bottom), np.log10(data_visible[:, 1]), len(colorseq)+1)
                else:
                    y_steps = np.linspace(y_bottom, data_visible[:, 1], len(colorseq))
                for i in range(len(colorseq)):
                    y_lower = y_steps[i, :]
                    y_upper = y_steps[i+1, :]
                    color = colorseq[len(colorseq) - i - 1] # reverse to have the lighter colours with the data curve
                    self.plot.fill_between(data_visible[:, 0], y_lower, y_upper, color=color, zorder=self.zorder)

        self.zorder += 1

    def plot_labels(self, labels: list):
        print("Plotting labels:")
        for label in labels:
            # extract plt.text kwargs from the fourth element of the tuple
            kwargs = {}
            if type(label[3]) == str:
                kwargs = extract_kwargs(label[3])
            elif type(label[3]) == dict:
                kwargs = label[3]
            
            # add functionality for border around text
            border_color = kwargs.pop("bordercolor", None) or kwargs.pop("bc", None)
            border_width = kwargs.pop("borderwidth", None) or kwargs.pop("bw", None)
            # default values if one of them is not provided
            if border_color is not None and border_width is None:
                border_width = 1 # default border width
            elif border_color is None and border_width is not None:
                border_color = "black" # default border color
            if border_color is not None and border_width is not None:
                kwargs["path_effects"] = [mplpe.withStroke(linewidth=border_width, foreground=border_color)]

            # if "picker" not in kwargs:
            #   kwargs["picker"] = True
            text = label[0]
            if not self._uselatex:
                text = latex_to_plain_text(label[0])
            kwargs_to_print = kwargs.copy()
            is_path_effect = kwargs_to_print.pop("path_effects", False)
            if is_path_effect:
                kwargs_to_print["bc"] = border_color
                kwargs_to_print["bw"] = border_width
            print("->", text, label[1], label[2], kwargs_to_print)
            self.plot.text(x=label[1], y=label[2], s=text, **kwargs)
    
    @abstractmethod
    def plot_data(self, data: list):
        pass
    
    def get_plotted_data_dict(self):
        d = {}
        for item in self.data_to_plot:
            properties = {}
            #properties["name"] = item.name
            properties["type"] = item.typeitem
            properties["path"] = item.short_filename
            properties["drawOptions"] = item.drawopt
            d[item.name] = properties.copy()
        return d.copy()
    
    def get_plotted_data_dict_str(self):
        d = self.get_plotted_data_dict()
        s = "{\n"
        for name, properties in d.items():
            s += f'    "{name}": {properties},\n'
        s += "}"
        return s
    
    def get_plotted_data_names(self):
        return [item.name for item in self.data_to_plot]
    
    def get_plot_customization(self):
        return {
            "labelx": self.plot.get_xlabel(),
            "labely": self.plot.get_ylabel(),
            "figx": self.fig.get_figwidth(),
            "figy": self.fig.get_figheight(),
            "ymin": self.plot.get_ylim()[0],
            "ymax": self.plot.get_ylim()[1],
            "xmin": self.plot.get_xlim()[0],
            "xmax": self.plot.get_xlim()[1],
            #"ticksopt_x": "dense" if self.plot.xaxis.get_major_locator().base == 100.0 else "normal",
            #"ticksopt_y": "dense" if self.plot.yaxis.get_major_locator().base == 100.0 else "normal",
            #"labelfontsize": self.plot.get_xlabel().get_fontsize(),
            #"tickformatter_x": self.plot.xaxis.get_major_formatter(),
            #"tickformatter_y": self.plot.yaxis.get_major_formatter(),
        }

    def get_plot_labels(self):
        labels = []
        for text in self.plot.texts:
            kwargs = {
                "color": text.get_color(),
                "fontsize": text.get_fontsize(),
                "ha": text.get_horizontalalignment(),
                "va": text.get_verticalalignment(),
                "rotation": text.get_rotation(),
                "rotation_mode": text.get_rotation_mode(),
            } # text.properties()
            # check if the text has a path effect of type withStroke to extract border color and width
            path_effects = text.get_path_effects()
            if path_effects is not None:
                for pe in path_effects:
                    if isinstance(pe, mplpe.Stroke):
                        kwargs["bordercolor"] = pe._gc.get("foreground", None)
                        kwargs["borderwidth"] = pe._gc.get("linewidth", None)
                        break
            labels.append((text.get_text(), text.get_position()[0], text.get_position()[1], kwargs))
        return labels

    def get_plot_labels_str(self):
        labels = self.get_plot_labels()
        s = "[\n"
        for label in labels:
            kwargs_str = ", ".join(f"{k}={v}" for k, v in label[3].items())
            s += f'    (r\'{label[0]}\', {label[1]}, {label[2]}, {label[3]}),\n'
        s += "]"
        return s

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
                    ", rotation_mode=" + f"'{self.dragged.get_rotation_mode()}'"
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
    def save_plot(self, plot_name="", **kwargs):
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

        if kwargs.get("bbox_inches", None) is None:
            kwargs["bbox_inches"] = "tight" # default value
        self.fig.savefig(filename, **kwargs)
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

        # parse the colormap description
        cmap_description = kwargs.get("cmap", None)
        cseq = None
        if cmap_description:
            params = {
                0 : "", # name of the colormap or color
                1 : 0, # minimum value of the colormap or alpha
                2 : 1, # maximum value of the colormap or alpha
                3 : 100 # number of colors from the colormap
            }
            if type(cmap_description) == str:
                params[0] = cmap_description
            elif type(cmap_description) in [list, tuple]:
                for i in range(len(cmap_description)):
                    params[i] = cmap_description[i]
            else:
                raise ValueError("cmap description must be a string or a list/tuple")

            # generate the sequence of colors
            try:
                cseq = plt.get_cmap(params[0])(np.linspace(params[1], params[2], params[3]))
            except ValueError: # if the colormap is not recognized, try to generate the colors
                cseq = generate_colors_with_alpha(params[0], params[1], params[2], params[3])
                cseq = rgba_to_rgb(cseq)

            self.drawopt["cseq"] = cseq

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

    def draw_item(self, plot):
        drawopt_to_print = self.drawopt.copy()
        drawopt_to_print.pop("cseq", None)
        print("->", self.name, self.short_filename, drawopt_to_print)
        plot.add_plot_item(self.typeitem, self.data, **self.drawopt)


# ==============================================================================#
# ==============================================================================#
# ==============================================================================#
