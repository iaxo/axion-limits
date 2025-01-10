
# Project contents
## Source files
The main files where the code is written are in the [src](src/axionlimits) folder. The code contains the following modules

1. x_plotter.py : the matplotlib.pyplot objects creation and configuration are
   handled within the two classes (BasePlot and ExPltItem) defined in this file
2. axion_plot.py : the creation of the BasePlot for the two cases (AxionGagPlot
   and AxionGaePlot), the plotting of the data and labels are handled within
   this classes.
3. wimp_plot.py : the creation of the BasePlot, the plotting of the data and labels are handled within this class.
4. databases.py : Here the DataBase classes are defined to interface with
   the SQLite .db files. It has the following classes:
   - DataBase is the generic database class that can be used to load an already existing database.
   - DataBaseGag to create the database table of AxionGag experiments.
   - DataBaseGae to create the  database table of AxionGae experiments.
   - DataBaseWimps to create the database table of WIMps experiments.

All these files are not intended to be modified by the user.

## Data files

Inside the data folder you can find the default databases which organize the different exclusion lines. 

### Databases
The different dark matter detection experiment are organize in SQL databases. For now, we have one database for [axion](data/Axions.db) experiments (which contains one table named AxionsGag for photon coupling and another one called AxionGae for electron coupling) and for [WIMPs](data/Wimps.db) experiments (which contains one table named WIMPs_SI for spin independent interaction). Any of this table databases contain at least these first columns:
1. **_name_** : string used to identify the experiment. It should be unique (although it is not forbidden) to the data that would load, so is recommended to add some other identificative tag to the experiment name itself. For example, instead of just _ADMX_ you may use _ADMX2021_ .
2. **_type_** : string used to specify the type of exclusion data it is. It can hold this valid values:
   - _line_ : it will be plotted as a line. In WimpPlot, it will be included by default to get the exclusion region.
   - _region_ : it will be plotted as an enclosed surface on the plot.
   - _band_ : it will be plotted as an open surfarce from the line defined in the data up to the top of the figure.
   - _fog_ : it will be plotted as an open surfarce from the line defined in the data down to the bottom of the figure. For example, it is used for neutrino fog (or floor) representation on WimpPlot.

   Each of this will use a different matplotlib.pyplot method (see [XPlotter](src/axionlimits/x_plotter.py)).
3. **_path_** : string containing the relative path (from the database file directory) to the data file (.txt or .dat) where the data of that experiment is contained. This file should be inside the data/axion/ or data/wimp/ directory. For example: _axion/ADMX2018.txt_
4. **_drawOptions_** : string containing the customization options for the plotting method of matplotlib.pyplot used (dependent on the _type_). For example: _facecolor='limegreen', edgecolor='darkgreen', lw=0.2_
5. **_projection_** : integer (_0_ or _1_) that indicates if the data is just a prospect/projection for future results (_1_) or if it is a reported result (_0_).
6. **_source_** : string containing the origin of the data. It can be the DOI of the publication, the arXiV identifier or any other way of tracing the origin of the data. This information should also be included inside the data file as a header (starting with the comment character # ). For example: _2110.06096_
7. **_year_** : string containing the year of release of the data. For example: _2019_


Furthermore, the different DM candidates databases have more specific additional columns. In order to create the desired database you may use the correspondent database class defined in [databases.py](src/axionlimits/databases.py).

The python script [build_database.py](src/axionlimits/data/build_databases.py) serves as backup for generating the databases in case they are unintentionally changed or deleted.