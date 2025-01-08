import axionlimits.databases as db
from axionlimits.wimp_plot import WimpPlot

# --- LOAD THE DATABASE ---

database = db.DataBaseWimps()

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

# --- EDIT THE ITEMS PROPERTIES ---
# If you want to edit the properties of an item you have selected from the database,
# you can do it here. For example, change the drawOptions of the element "NuFloorXe":
exps["NuFloorXe"]["drawOptions"] += ", cmap=('Greys', 0, 0.8, 100), edgecolor=None"

# Or add a new element which is not present in the database. For example, a projection
# you have calculated and want to compare with the existing exclusion lines from the
# database:
exps["TREX-DM_projection"] = {
    "type": "line",
    "path": "wimp/Ar_iso1/C_2y.dat",
    "drawOptions": "color='red'",
    "projection": True,
}


# --- ADD THE LABELS ---
# Get the default label properties from the database
default_labels = database.get_rows("name", experimentsToPlot)
labels = []
for label in default_labels.values():
    labels.append(
        (
            label.get("label",None),
            label.get("labelPosX",None),
            label.get("labelPosY",None),
            label.get("labelDrawOptions",""),
        )
    )
# add extra label
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

