from __future__ import annotations

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
    "old_haloscopes"
    "ADMX2018",
    "ADMX2019",
    "ADMX2021",
    "ADMX_sidecar",  # 'ADMX2019_2',
    "CAPP-8TB",
    "CAPP_multicell",
    "CAPP2021",
    "HAYSTAC",
    "HAYSTAC2020",
    "ORGAN",
    "QUAX",
    "QUAX2021",
    "ADMX_SLIC",
    "RADES2021",
    "admx",
    "CAST",

    # projections
    "ABRA1",
    "ABRA2",
    "ABRA3",
    "ABRA1_l",
    "KLASH",
    "TOORAD",  # 'IAXODM','IAXODM_l',
    "ADMXprosp_2GHz",
    "ADMXprosp_2GHz_l",
    "ADMXprosp_10GHz",
    "ADMXprosp_10GHz_l",
    "CAPP4_l",
    "MADMAX_l",
    "ORGANprosp",
    "BRASS",

    "BabyIAXO",
    "BabyIAXO_l",
    "IAXO",
    "IAXO_l",
    "IAXOplus",
    "IAXOplus_l",
]

exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    showplot=False,  # set to false to add the labels later
    plotCag=True,  # set to true to plot C_ag instead of g_ag
    labely=r"$|C_{a\gamma}|\tilde{\rho}_a^{1/2}$",
    figx=8,
    figy=5,
    ymin=1e-1,
    ymax=1e3,
    xmin=1e-9,
    xmax=1,
    ticksopt_x="normal",
    ticksopt_y="normal",
)

# --- ADD THE LABELS ---
plt.text(2.5e-3, 110, r'{\bf CAST}', color="black", size=12, ha='center', rotation=-57)
plt.text(1e-8, 3, 'ABRA/DM-Radio', color="black", size=12, ha='center', rotation=-57)
plt.text(3.3e-7, 70, 'KLASH', color="black", size=11, ha='center', va='center', rotation=90)
plt.text(1e-3, 2.5, 'KSVZ', color="green", size=9, va='center', ha='center')
plt.text(1e-3, 0.32, 'Axion models', color="green", size=9, ha='center')
plt.text(2.9e-6, 70, r'{\bf ADMX}', color="black", size=12, ha='center', va='center', rotation=90)
plt.text(9.5e-7, 70, 'ACTION/IAXO-DM', color="black", size=10, ha='center', va='center', rotation=90)
plt.text(8.3e-6, 650, 'BNL\n+UF', color="black", size=8, ha='center', va='center')
plt.text(7e-6, 0.86, 'ADMX', color="black", size=10, ha='center', va='center')
plt.text(1.9e-5, 2.24, 'CAPP', color="black", size=10, ha='center', va='center')
plt.text(1.46e-5, 25, 'HAYSTAC', color="black", size=8, ha='center', va='center', rotation=90)
plt.text(1.2e-4, 1.15, 'MADMAX', color="black", size=8, ha='center', va='center')
plt.text(1.2e-4, 30, 'ORGAN', color="black", size=8, ha='center', va='center')
plt.text(3e-5, 25, 'RADES', color="black", size=8, ha='center', va='center', rotation=90)

#projections
plt.text(1.8e-3, 83, r'BabyIAXO', color="black", size=10, ha='center', va='center', rotation=-57)
plt.text(1e-3, 36, r'{\bf IAXO}', color="black", size=11, ha='center', va='center', rotation=-57)
plt.text(0.01, 12, 'TOORAD', color="black", size=8, ha='center', va='center', rotation=90)
# plt.text(1e-5,1e-12,r'{\bf IAXO+}',color="black",size=9,ha='center',va='center')
# plt.text(5e-7,3e-11,r'{\bf ALPS-II}',color="black",size=10,ha='center',va='center')
# plt.text(5e-7,1.5e-12,r'{\bf JURA}',color="black",size=9,ha='center',va='center')

# --- SHOW AND SAVE THE PLOT ---
axionplot.baseplot.ShowPlot()
axionplot.baseplot.SavePlot("haloscopes.pdf")
