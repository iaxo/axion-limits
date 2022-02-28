from axionPlot import AxionGagPlot, AxionGaePlot
from wimpPlot import WimpPlot

for plot_type in AxionGagPlot.ListOfPlotTypes:
    AxionGagPlot(plot_type,
                 projections=True,
                 showplot=False,
                 saveplot=True)

    AxionGaePlot(plot_type,
                 projections=True,
                 showplot=False,
                 saveplot=True)

# There seems to be some bugs in WIMP plots, we are not saving them by default until this is fixed
#for plot_type in WimpPlot.ListOfPlotTypes:
#    WimpPlot(plot_type,
#             projections=True,
#             showplot=True,
#             saveplot=False)
