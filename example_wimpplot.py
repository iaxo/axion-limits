import axionlimits.databases as db
from axionlimits.wimp_plot import WimpPlot

# --- LOAD THE DATABASE ---

database = db.DataBaseWimps()  # the second parameter is the table name inside the database, see DataBaseClass.py for more info

"""
# Here you can edit the database if you want.
# For example, change the drawOptions of a row:
database.update_row("exp_name", "drawOptions", "color='blue', linewidth=1")
"""

# List of the names of the experiments to plot. The names must match the name column in the database
# To see the names of the experiments in the database, you can use the following command:
# print([row[0] for row in database.get_rows_where("1 ORDER BY name")])
experimentsToPlot = [
    "CDMSLite_2016",
    "CRESSTII_2015",
    "CRESSTIII_2019",
    "DAMIC_2020",
    "DarkSide50_2022",
    "NEWS_G_2018",
    "PandaX-4T_2022",
    "PICO_C3F8_2017",
    "XENON1T_2018",
    "XENON1T_2021",
    "DAMA_I",
    # Neutrino fog
    "NuFloorXe",
    # projections
]
exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database
exps = [list(exp) for exp in exps]  # Convert the tuples to lists

exps[-1][3] += ", cmap=('Greys', 0, 0.5, 50)"
exps.append(
    ["TREX-DM_projection", "line", "data/wimp/Ar_iso1/C_2y.dat", dict(projection=True, color="red"), True]
)

# --- ADD THE LABELS ---
labels = database.get_rows("name", experimentsToPlot)
# get the 7th (label text), 8th (x), 9th (y) and 10th (draw opts) columns
labels = [row[7:11] for row in labels]

extralabels = [
    ("TREX-DM", 0.21, 1.4e-37, dict(size=10, color="red")),
]
labels.extend(
    extralabels
)  # use extend instead of append to add the elements of the list, not the list itself

# --- BUILD THE PLOT ---
axionplot = WimpPlot(
    experiments=exps,
    labels=labels,
    showplot=True,  # set to false to add the labels later
    saveplotname="WIMPs_SI.pdf",
    figx=9,
    figy=7,
)

