import axionlimits.databases as db
from axionlimits.axion_plot import AxionGagPlot

import matplotlib.pyplot as plt
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
    "CAPP18T_2022",
    "CAPP12T_2022",
    "CAPP-PACE_2022",
    "HAYSTAC",
    "HAYSTAC2020",
    "ORGAN",
    "ORGAN1a_2022",
    "QUAX",
    "QUAX2021",
    "ADMX_SLIC",
    "CAST-CAPP",
    "RADES2021",
    "TASEH_2022",
    "GraHal_2022",
    "admx",
    "NeutronStars",
    "CAST",
    "TransmonMW_PC",
    "QUAX2024",
    "CAPP2024"

    # projections
#    "ABRA1",
#    "ABRA2",
#    "ABRA3",
#    "ABRA1_l",
#    "KLASH",
#    "TOORAD",  # 'IAXODM','IAXODM_l',
#    "ADMXprosp_2GHz",
#    "ADMXprosp_2GHz_l",
#    "ADMXprosp_10GHz",
#    "ADMXprosp_10GHz_l",
#    "CAPP4_l",
#    "MADMAX_l",
#    "ORGANprosp",
#    "BRASS",

#    "BabyIAXO",
#    "BabyIAXO_l",
#    "IAXO",
#    "IAXO_l",
#    "IAXOplus",
#    "IAXOplus_l",
]

exps = database.get_rows(
    "name", experimentsToPlot
)  # Get the data of the experiments to plot from the database

labels=[
#    (r'{\bf CAST}', 2.5e-3, 110, dict(color="black", size=12, ha='center', rotation=-57)),
#    ('ABRA/DM-Radio', 1e-8, 3, dict(color="black", size=12, ha='center', rotation=-57)),
#    ('KLASH', 3.3e-7, 70, dict(color="black", size=11, ha='center', va='center', rotation=90)),
    ('KSVZ', 1e-4, 2.5, dict(color="green", size=9, va='center', ha='center')),
    ('Axion models', 1e-4, 0.32, dict(color="green", size=9, ha='center')),
    (r'{\bf ADMX}', 2.9e-6, 70, dict(color="black", size=12, ha='center', va='center', rotation=90)),
#    ('ACTION/IAXO-DM', 9.5e-7, 70, dict(color="black", size=10, ha='center', va='center', rotation=90)),
    ('BNL\n+UF', 8.3e-6, 650, dict(color="black", size=8, ha='center', va='center')),
#   ('ADMX', 7e-6, 0.86, dict(color="black", size=10, ha='center', va='center')),
#    ('CAPP', 1.9e-5, 2.24, dict(color="black", size=10, ha='center', va='center')),
#open     ('HAYSTAC', 1.46e-5, 25, dict(color="black", size=8, ha='center', va='center', rotation=90)),
#    ('MADMAX', 1.2e-4, 1.15, dict(color="black", size=8, ha='center', va='center')),
#    ('ORGAN', 1.2e-4, 30, dict(color="black", size=8, ha='center', va='center')),
#    ('RADES', 3e-5, 25, dict(color="black", size=8, ha='center', va='center', rotation=90)),
    ('RADES',34.6e-6,25,dict(color="black",size=8,ha='center',va='center',rotation=90)),
    ('TASEH',15e-6,3.7,dict(color="black",size=8,ha='center',va='center',rotation=90)),
    ('CASTCAPP',15.5e-6,35,dict(color="black",size=7,ha='center',va='center',rotation=90)),
    ('GraHal',28.0e-6,20,dict(color="black",size=8,ha='center',va='center',rotation=90)),
    ('CAPP',8.1e-6,0.33,dict(color="black",size=8,ha='center',va='top',rotation=90)),
    ('HAYSTAC',1.96e-5,1.00,dict(color="black",size=8,ha='center',va='top',rotation=90))
    #projections
#    (r'BabyIAXO', 1.8e-3, 83, dict(color="black", size=10, ha='center', va='center', rotation=-57)),
#    (r'{\bf IAXO}', 1e-3, 36, dict(color="black", size=11, ha='center', va='center', rotation=-57)),
#    ('TOORAD', 0.01, 12, dict(color="black", size=8, ha='center', va='center', rotation=90)),
    # (r'{\bf IAXO+}', 1e-5, 1e-12, dict(color="black",size=9,ha='center',va='center')),
    # (r'{\bf ALPS-II}', 5e-7, 3e-11, dict(color="black",size=10,ha='center',va='center')),
    # (r'{\bf JURA}', 5e-7, 1.5e-12, dict(color="black",size=9,ha='center',va='center')),
]


          
                
# --- BUILD THE PLOT ---
axionplot = AxionGagPlot(
    experiments=exps,
    labels=labels,
    plotCag=True,  # set to true to plot C_ag instead of g_ag
    showplot=False,  # set to false to add the labels later
    saveplotname="haloscopes_zoom_Jun2024.pdf",
    labely=r"$|C_{a\gamma}|\tilde{\rho}_a^{1/2}$",
    figx=8,
    figy=5,
    ymin=1e-1,
    ymax=1e3,
    xmin=6e-7,
    xmax=1.6e-4,
    ticksopt_x="normal",
    ticksopt_y="normal",
)

# --- post-plot customization (need to set showplot to false above)
            
plt.plot([8.3e-6,6.79e-6],[0.4,1.64],color='black',linewidth=0.5)
plt.plot([8.3e-6,1.07e-5],[0.4,1.68],color='black',linewidth=0.5)
plt.plot([8.3e-6,1.33e-5],[0.4,1.64],color='black',linewidth=0.5)
plt.plot([8.3e-6,1.98e-5],[0.4,1.64],color='black',linewidth=0.5)
plt.plot([8.3e-6,0.5e-5],[0.4,0.6],color='black',linewidth=0.5) #capp12t
plt.plot([8.3e-6,0.5e-5],[0.4,0.6],color='black',linewidth=0.5) #capp-pace
plt.plot([15e-6,19.35e-6],[6,9],color='black',linewidth=0.5) #taseh  xdata=1.3252e-05, ydata=6.15306f
plt.plot([2e-5,1.65e-5],[43,30],color='black',linewidth=0.5) #castcapp
plt.plot([2e-5,1.71e-5],[1.12,1.8],color='black',linewidth=0.5)
plt.plot([2e-5,2.38e-5],[1.12,2.24],color='black',linewidth=0.5)
plt.plot([8.3e-5,11e-5],[61,83],color='black',linewidth=0.5)
plt.plot([8.3e-5,6.6e-5],[61,83],color='black',linewidth=0.5)

#one can also add labels here...
plt.text(4.1e-5,3.6,'QUAX',color="black",size=8,ha='center',va='center',rotation=90)
plt.text(0.84e-4,35,'ORGAN',color="black",size=8,ha='center',va='center',rotation=90) #xdata=8.48019e-05, ydata=61.4904f

# we finish by plotting and saving (because we set the flag to false above)
axionplot.ShowPlot()
axionplot.SavePlot()

# ---  end of customization
