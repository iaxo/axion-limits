import sys

# Add the absolute path to the project
PATH_TO_PROJECT = ""

try:
    from AxionPlot import *
    import DataBaseClass as db
except ModuleNotFoundError:
    if PATH_TO_PROJECT not in sys.path:
        if PATH_TO_PROJECT == "":
            print("ERROR: Please set the path to the project inside myPlottingScripts/myPath.py")
        else:
            sys.path.append(PATH_TO_PROJECT)