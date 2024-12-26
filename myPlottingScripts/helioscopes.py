import axionlimits.databases as db
from axionlimits.axion_plot import AxionGagPlot

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
    "admx_hf_2016",
    "ADMX2018",
    "ADMX2019",
    "ADMX2021",
    "ADMX_sidecar",
    "CAPP-8TB",
    "HAYSTAC",
    "HAYSTAC2020",
    "ORGAN",
    "QUAX",
    "QUAX2021",
    "RADES2021",
    "ADMX_SLIC",
    "old_haloscopes",
    "admx",
    "THintMayer",
    "THintCIBER",
    "HBhint",
    "hess",
    "mrk421",
    "sn1987a_photon",
    "FERMI_NG1275",
    "endlist2_gamma_projimprov",
    "telescopes",
    "telescopes_new",
    "HBalpbound_l",
    "solar_nu",
    "CAST",

    "SHAFT", "ABRA_2021", "BASE_2021",
    "OSCAR2015", "PVLAS2015", "ALPSI",

    # projections
     "ALPSII_l",
    "BabyIAXO",
    "IAXO",
    "IAXOplus",
    "BabyIAXO_l",
    "IAXO_l",
    "IAXOplus_l",
    "AMELIE",
]

exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

labels=[
    (r"{\bf CAST}", 3e-6, 8.5e-11, dict(color="blue", size=13)),
    # (r'{\bf Laboratory}', 1e-7, 2e-7, dict(color="white",size=12)),
    (r"T-hints", 1e-8, 6e-12, dict(color="red", size=11)),
    # (r"HE $\gamma \textrm{-rays}$", 2e-9, 6e-12, dict(color="black",size=10)),
    (r"{\bf Haloscopes}", 1e-6, 1e-12, dict(color="black", size=13)),
    ("KSVZ", 1.15e-3, 0.75e-12, dict(color="black", size=10, rotation=57)),
    ("Axion models", 4.7e-3, 5e-13, dict(color="black", size=10, rotation=57)),
    # ('Telescopes', 5, 3e-13, dict(color="black",size=8,rotation=90)),
    ("HB", 8e-2, 7e-11, dict(color="black", size=10)),
    ("HB hint", 1e-1, 1.3e-11, dict(color="red", size=10)),
    ("WD \ncooling\n hint ", 3.5e-3, 6.0e-12, dict(color="red", size=10, ha="center",)),
    # ('Sun', 3, 1.3e-9, dict(color="black",size=9,ha='center')),
    # (r'{\bf Sun}', 1e2, 2e-9, dict(color="white",size=10)),
    ("ABRA\n-10cm", 7e-10, 2e-9, dict(color="black", size=10)),
    ("SHAFT", 2e-11, 4e-10, dict(color="black", size=10)),
    ("HESS", 3e-8, 2e-11, dict(color="black", size=9, ha="center")),
    ("Mrk421", 1e-8, 4e-11, dict(color="black", size=9, ha="center")),
    ("SN1987A", 1.5e-11, 7e-12, dict(color="black", size=9)),
    ("Fermi\nNG1275", 6e-10, 7e-12, dict(color="black", size=9)),

    #projections
    (r"{\bf AMELIE}", 1e-3, 8.5e-11, dict(color="gray", size=11)),
    (r"BabyIAXO", 3e-4, 2e-11, dict(color="black", size=12)),
    (r"{\bf IAXO}", 1.75e-4, 5e-12, dict(color="black", size=13)),
    (r"{\bf IAXO+}", 1.4e-4, 3.2e-12, dict(color="black", size=9, ha="center", va="center")),
    (r"{ ALPS-II}", 5e-7, 2.7e-11, dict(color="black", size=12)),
    # (r'{\bf JURA}', 5e-7, 1.5e-12, dict(color="black",size=9,ha='center',va='center')),
]

# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=False,  # set to true to plot C_ag instead of g_ag
    showplot=True,  # set to false to add the labels later
    saveplotname="helioscopes.pdf",
    figx = 8,
    figy = 6,
    ymin = 1e-13,
    ymax = 1e-8,
    xmin = 1e-11,
    xmax = 1,
    ticksopt_x = "normal",
    ticksopt_y = "normal",
)
