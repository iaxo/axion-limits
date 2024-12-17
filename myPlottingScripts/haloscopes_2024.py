import axionlimits.Database as db
from axionlimits.AxionPlot import AxionGagPlot

# --- LOAD THE DATABASE ---

database = db.DataBaseGag()
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
    "old_haloscopes",
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
    "CAST2021",

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

labels=[
    (r'{\bf CAST}', 2.5e-3, 110, dict(color="black", size=12, ha='center', rotation=-57)),
    ('ABRA/DM-Radio', 1e-8, 3, dict(color="black", size=12, ha='center', rotation=-57)),
    ('KLASH', 3.3e-7, 70, dict(color="black", size=11, ha='center', va='center', rotation=90)),
    ('KSVZ', 1e-3, 2.5, dict(color="green", size=9, va='center', ha='center')),
    ('Axion models', 1e-3, 0.32, dict(color="green", size=9, ha='center')),
    (r'{\bf ADMX}', 2.9e-6, 70, dict(color="black", size=12, ha='center', va='center', rotation=90)),
    ('ACTION/IAXO-DM', 9.5e-7, 70, dict(color="black", size=10, ha='center', va='center', rotation=90)),
    ('BNL\n+UF', 8.3e-6, 650, dict(color="black", size=8, ha='center', va='center')),
    ('ADMX', 7e-6, 0.86, dict(color="black", size=10, ha='center', va='center')),
    ('CAPP', 1.9e-5, 2.24, dict(color="black", size=10, ha='center', va='center')),
    ('HAYSTAC', 1.46e-5, 25, dict(color="black", size=8, ha='center', va='center', rotation=90)),
    ('MADMAX', 1.2e-4, 1.15, dict(color="black", size=8, ha='center', va='center')),
    ('ORGAN', 1.2e-4, 30, dict(color="black", size=8, ha='center', va='center')),
    ('RADES', 3e-5, 25, dict(color="black", size=8, ha='center', va='center', rotation=90)),

    #projections
    (r'BabyIAXO', 1.8e-3, 83, dict(color="black", size=10, ha='center', va='center', rotation=-57)),
    (r'{\bf IAXO}', 1e-3, 36, dict(color="black", size=11, ha='center', va='center', rotation=-57)),
    ('TOORAD', 0.01, 12, dict(color="black", size=8, ha='center', va='center', rotation=90)),
    # (r'{\bf IAXO+}', 1e-5, 1e-12, dict(color="black",size=9,ha='center',va='center')),
    # (r'{\bf ALPS-II}', 5e-7, 3e-11, dict(color="black",size=10,ha='center',va='center')),
    # (r'{\bf JURA}', 5e-7, 1.5e-12, dict(color="black",size=9,ha='center',va='center')),
]

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=True,  # set to true to plot C_ag instead of g_ag
    showplot=True,  # set to false to add the labels later
    saveplotname="haloscopes_2024.pdf",
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

