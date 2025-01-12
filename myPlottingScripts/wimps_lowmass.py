import axionlimits.databases as db
from axionlimits.wimp_plot import WimpPlot

# --- LOAD THE DATABASE ---

database = db.DataBaseWimps()  # the second parameter is the table name inside the database, see DataBaseClass.py for more info

"""
# Here you can edit the database if you want.
# For example, change the drawOptions of a row:
database.update_row("exp_name", "drawOptions", "color='blue', linewidth=1")
# Or delete a row:
database.delete_rows("name='exp_name'", confirm=True)
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
exps = database.get_rows("name", experimentsToPlot)  # Get the data of the experiments to plot from the database
# Edit the drawOptions if you want
exps["NuFloorXe"]["drawOptions"] += ", cmap=('Greys', 0.1, 0.7, 50), edgecolor=None"

# Get the labels of the experiments to plot from the database
db_labels = database.get_rows("name", experimentsToPlot)
# Edit the labels if you want
db_labels["PandaX-4T_2022"]["labelPosX"] = 3.7
db_labels["PandaX-4T_2022"]["labelPosY"] = 2.67e-44
db_labels["PandaX-4T_2022"]["labelDrawOptions"] += ", rotation=313, rotation_mode='anchor', picker=True"

# Extract the labels in the format (label, labelPosX, labelPosY, labelDrawOptions)
# as required by the WimpPlot class
labels = []
for label in db_labels.values():
    labels.append(
        (
            label.get("label",None),
            label.get("labelPosX",None),
            label.get("labelPosY",None),
            label.get("labelDrawOptions",""),
        )
    )

# --- BUILD THE PLOT ---
axionplot = WimpPlot(
    experiments=exps,
    labels=labels,
    showplot=True,  # set to false to add the labels later
    saveplotname="WIMPs_SI.pdf",
    figx=9,
    figy=7,
)

axionplot.save_plot(__file__+".png")