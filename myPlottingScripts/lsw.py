from __future__ import annotations

import myPath # add the path to the project
import DataBaseClass as db
from AxionPlot import *

# --- LOAD THE DATABASE ---

database = db.DataBaseGag(
    "databases/Axions.db", "AxionsGag"
)  # the second parameter is the table name inside the database, see DataBaseClass.py for more info

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
    "qcdband",
    "ksvz",
    "THintMayer",
    "THintCIBER",
    "hess",
    "mrk421",
    "sn1987a_photon",
    "FERMI_NG1275",
    "CAST",
    "HBhint",
    "OSCAR2015",
    "PVLAS2015",
    "ALPSI",
    "CROWS",
    # projections
    "ALPSII",
    "STAX1",
    "STAX2",
    "ALPSII",
]

exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

labels=[
    (r'CAST', 1e-3, 1e-10, dict(color="black", size=10)),
    (r'{ ALPS-I}', 1e-4, 1.4e-7, dict(color="white", size=10, ha='center', va='center')),
    (r'{ CROWS}', 1e-7, 1.5e-7, dict(color="white", size=10, ha='center', va='center')),
    (r'{ PVLAS}', 3e-3, 1e-7, dict(color="black", size=10, ha='center', va='center', rotation=45)),
    (r'{ OSQAR}', 1e-4, 2e-8, dict(color="black", size=10, ha='center', va='center')),
    (r"T-hints", 2e-9, 6e-12, dict(color="black", size=10)),

    #projections
    ('STAX1', 3e-6, 1e-10, dict(color="black", size=10, ha='center', va='center')),
    ('STAX2', 2e-6, 5e-12, dict(color="black", size=10, ha='center', va='center')),
    # (r'{\bf IAXO+}', 1e-5, 1e-12, dict(color="black",size=9,ha='center',va='center')),
    (r'{\bf ALPS-II}', 1e-6, 3e-11, dict(color="black", size=10, ha='center', va='center')),
    # (r'{\bf JURA}', 2e-5, 1.3e-12, dict(color="black", size=9, ha='center', va='center')),
]

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    showplot=True,  # set to false to add the labels later
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    saveplotname="lsw_exps.pdf",
    figx=6.5,
    figy=5,
    ymin=1e-13,
    ymax=1e-6,
    xmin=1e-10,
    xmax=1e-2,
    ticksopt_x="normal",
    ticksopt_y="normal",
)

