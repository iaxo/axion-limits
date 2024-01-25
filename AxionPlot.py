import matplotlib.pyplot as plt
import matplotlib as mpl
from XPlotter import BasePlot, ExPltItem
import DataBaseClass as db

def extract_kwargs(arguments_str):
    """Extracts kwargs from a string of arguments. 
    Example: extract_kwargs("a=1, b=2, c=3") returns {'a':1, 'b':2, 'c':3}
             extract_kwargs("a=1, b="red", c=3,") returns {'a':1, 'b':'red', 'c':3}"""
    kwargs = {}
    for arg in arguments_str.split(','):
        if arg.strip() != '':
            key, value = arg.split('=')
            kwargs[key.strip()] = eval(value.strip())
    return kwargs

# ==============================================================================#
# renormalize data, to plot C_ag instead of g_ag
#
def RenormItem(item):
    for i in range(len(item.data)):
        # print(item.name)
        item.data[i, 1] = item.data[i, 1] / item.data[i, 0] * 5.172e9
        # print(item.data[i,0],item.data[i,1])
        # C_ag = g_ag / m_a * 5.172e9

class AxionGagPlot:

    ListOfPlotTypes = {'large_panorama', 'panorama', 'LSWexps', 'haloscopes', 'haloscopes_zoom',
                       'haloscopes_radeszoom', 'helioscopes'}

    def __init__(self,
                     database : db.DataBaseGag, labels : db.DataBaseLabels, plottype="",
                     projections=False, showplot=True, saveplotname=None,
                     figx=None, figy=None, ymin=None, ymax=None, xmin=None, xmax=None,
                     ticksopt_x=None, ticksopt_y=None,
                     labelx='$m_a$ (eV)', labely=r'$|g_{a\gamma}|$ (GeV$^{-1}$)'
                ):

        if plottype not in self.ListOfPlotTypes:
            print('Warning: ' + plottype + ' not a known plot type. Using default values and wildType column in database')

        #default values for the plot (with no specified type)
        if (plottype in ["large_panorama"]) or (plottype not in self.ListOfPlotTypes):
            if figx is None:
                figx = 6.5
            if figy is None:
                figy = 5
            if ymin is None:
                ymin = 1e-18
            if ymax is None:
                ymax = 1e-4
            if xmin is None:
                xmin = 1e-11
            if xmax is None:
                xmax = 1e9
            if ticksopt_x is None:
                ticksopt_x = 'dense'
            if ticksopt_y is None:
                ticksopt_y = 'normal'

        #default values for the plot (with specified type)
        if plottype == "panorama":
            if figx is None:
                figx = 6.5
            if figy is None:
                figy = 6
            if ymin is None:
                ymin = 1e-17
            if ymax is None:
                ymax = 1e-6
            if xmin is None:
                xmin = 1e-9
            if xmax is None:
                xmax = 10
            if ticksopt_x is None:
                ticksopt_x = 'normal'
            if ticksopt_y is None:
                ticksopt_y = 'normal'

        if plottype == "helioscopes":
            if figx is None:
                figx = 8
            if figy is None:
                figy = 6
            if ymin is None:
                ymin = 1e-13
            if ymax is None:
                ymax = 1e-8
            if xmin is None:
                xmin = 1e-11
            if xmax is None:
                xmax = 1
            if ticksopt_x is None:
                ticksopt_x = 'normal'
            if ticksopt_y is None:
                ticksopt_y = 'normal'

        if plottype == "LSWexps":
            if figx is None:
                figx = 6.5
            if figy is None:
                figy = 5
            if ymin is None:
                ymin = 1e-13
            if ymax is None:
                ymax = 1e-6
            if xmin is None:
                xmin = 1e-10
            if xmax is None:
                xmax = 1e-2
            if ticksopt_x is None:
                ticksopt_x = 'normal'
            if ticksopt_y is None:
                ticksopt_y = 'normal'

        if plottype in ["haloscopes", "haloscopes_zoom", "haloscopes_radeszoom"]:
            if figx is None:
                figx = 8
            if figy is None:
                figy = 5
            if ymin is None:
                ymin = 1e-1
            if ymax is None:
                ymax = 1e3
            if xmin is None:
                if plottype in ["haloscopes"]:
                    xmin = 1e-9
                if plottype in ["haloscopes_zoom"]:
                    xmin = 3e-7
                if plottype in ["haloscopes_radeszoom"]:
                    xmin = 3.4e-5
            if xmax is None:
                if plottype in ["haloscopes"]:
                    xmax = 1
                if plottype in ["haloscopes_zoom"]:
                    xmax = 3e-2
                if plottype in ["haloscopes_radeszoom"]:
                    xmax = 4.5e-5
            if ticksopt_x is None:
                ticksopt_x = 'normal'
            if ticksopt_y is None:
                ticksopt_y = 'normal'
            labely = r'$|C_{a\gamma}|\tilde{\rho}_a^{1/2}$'

        #plot the background
        self.axplot = BasePlot(xlab=labelx, ylab=labely,
                               figsizex=figx, figsizey=figy,
                               y_min=ymin, y_max=ymax,
                               x_min=xmin, x_max=xmax,
                               ticksopt_x=ticksopt_x, ticksopt_y=ticksopt_y)

        self.axionDB = database
        self.labelsDB = labels
        #print(self.axionDB.get_rows())

        #Plotting Data & Labels
        self.PlotData(plottype, projections)
        self.PlotLabels(projections)

        if showplot:
            self.axplot.ShowPlot()

        if type(saveplotname)==str:
            if len(saveplotname) > 0:
                print('saving...')
                self.axplot.SavePlot(saveplotname)
                print('done')

    def PlotData(self, plottype, projections = False):
        print("projections = ", projections)    
        if plottype not in self.ListOfPlotTypes:
            plottype = "wildType"
        if "haloscopes" in plottype:
            plottype = "haloscopes" # all haloscopes have the same column assigned ("haloscopes") in the database

        data = self.axionDB.get_rows(f"{plottype}==1")
        if projections:
            data = data + self.axionDB.get_rows(f"projection==1 AND {plottype}==0") # get projections not already included
        for row in data:
            pltItem = ExPltItem(row[0], row[1], row[2], **extract_kwargs(row[3]))
            if "haloscopes" in plottype:
                RenormItem(pltItem) # Its done in Haloscopes exclusively
            pltItem.DrawItem(self.axplot)

    def PlotLabels(self, projections = False):
        labels = self.labelsDB.get_rows(f"onoff==1 AND projection==0")
        if projections:
            labels = labels + self.labelsDB.get_rows(f"onoff==1 AND projection==1")

        for row in labels:
            plt.text(row[1], row[2], row[0], **extract_kwargs(row[3]))


class AxionGaePlot:

    ListOfPlotTypes = {} # No plottypes for Gae yet

    def __init__(self, 
                    database : db.DataBaseGae, labels : db.DataBaseLabels, plottype="", 
                    projections=False, showplot=True, saveplotname=None,
                    figx=6, figy=5, xmin=1.0e-4, xmax=1., ymin=1.0e-13, ymax=1.0e-10, labelfontsize=13, 
                    labelx='$m_a$ (eV)', labely=r'$|g_{ae}g_{a\gamma}|^{1/2}$ (GeV$^{-1/2}$)'
                ):

        self.axplot = BasePlot(xlab=labelx, ylab=labely,
                               figsizex=figx, figsizey=figy,
                               y_min=ymin, y_max=ymax,
                               x_min=xmin, x_max=xmax,
                               labelfontsize=labelfontsize)

        self.axionDB = database
        self.labelsDB = labels
        #print(self.axionDB.get_rows())

        self.PlotData(plottype, projections)
        self.PlotLabels(projections)
        if showplot:
            self.axplot.ShowPlot()

        if type(saveplotname)==str:
            if len(saveplotname) > 0:
                print('saving...')
                self.axplot.SavePlot(saveplotname)
                print('done')

    def PlotData(self, plottype, projections=False):
        print("projections = ", projections)    
        if plottype not in self.ListOfPlotTypes:
            plottype = "wildType"

        data = self.axionDB.get_rows(f"{plottype}==1")
        if projections:
            data = data + self.axionDB.get_rows(f"projection==1 AND {plottype}==0") # get projections not already included
        for row in data:
            pltItem = ExPltItem(row[0], row[1], row[2], **extract_kwargs(row[3]))
            pltItem.DrawItem(self.axplot)

    def PlotLabels(self, projections = False):
        labels = self.labelsDB.get_rows(f"onoff==1 AND projection==0")
        if projections:
            labels = labels + self.labelsDB.get_rows(f"onoff==1 AND projection==1")
       
        for row in labels:
            plt.text(row[1], row[2], row[0], **extract_kwargs(row[3]))
