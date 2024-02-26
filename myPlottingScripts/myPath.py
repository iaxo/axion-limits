from __future__ import annotations

import sys

# Add the absolute path to the project
PATH_TO_PROJECT = "/home/aezquerro/git/axion-limits_wimps"
try:
    import DataBaseClass as db
    from AxionPlot import *
except ModuleNotFoundError:
    if PATH_TO_PROJECT not in sys.path:
        if PATH_TO_PROJECT == "":
            print(
                "ERROR: Please set the path to the project inside myPlottingScripts/myPath.py"
            )
        else:
            sys.path.append(PATH_TO_PROJECT)
