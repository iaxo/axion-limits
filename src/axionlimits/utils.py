import shutil
import os
import ast
import re
import numpy as np
from importlib.resources import files
from pylatexenc.latex2text import LatexNodes2Text

def latex_to_plain_text(latex_string):
    converter = LatexNodes2Text()
    return converter.latex_to_text(latex_string)

def is_latex_installed():
    """Verify if LaTeX is installed in the system."""
    return shutil.which("latex") is not None

def resolve_relative_path(relative_path, package_route='axionlimits.data'):
    """
    Resuelve un path relativo ('files.db') al path absoluto dentro del paquete.

    :param relative_path: Ruta relativa al archivo en el paquete.
    :return: Ruta absoluta al archivo.
    """
    # Usa importlib.resources para encontrar la carpeta base
    resource_folder = files(package_route)
    absolute_path = resource_folder / relative_path

    # Comprueba si el archivo existe
    if not absolute_path.exists():
        raise FileNotFoundError(f"The file '{relative_path}' does not exist in the package.")

    return absolute_path

def get_absolute_path(path, package_route='axionlimits.data'):
    """
    Devuelve la ruta absoluta de un archivo en el sistema de archivos.

    :param path: Ruta relativa o absoluta al archivo.
    :return: Ruta absoluta al archivo.
    """
    if os.path.isfile(path):
        absolute_path = os.path.abspath(path)
    else:
        absolute_path = resolve_relative_path(path, package_route)

    return absolute_path

def extract_kwargs(arguments_str):
    """Extracts kwargs from a string of arguments, including lists or tuples.
    Example: 
        extract_kwargs("a=1, b=2, c=(3, 4)") returns {'a': 1, 'b': 2, 'c': (3, 4)}
        extract_kwargs("a=1, b='red', c=[1,2,3], d=(4,5,6)") returns {'a': 1, 'b': 'red', 'c': [1, 2, 3], 'd': (4, 5, 6)}
    """
    kwargs = {}
    # Regex to match key=value pairs, allowing nested structures like lists/tuples
    pattern = r'\s*(\w+)\s*=\s*(.+?)\s*(?=,\s*\w+\s*=|$)'
    
    matches = re.findall(pattern, arguments_str)
    for key, value in matches:
        try:
            kwargs[key.strip()] = ast.literal_eval(value.strip())
        except (ValueError, SyntaxError):
            kwargs[key.strip()] = value.strip()
    return kwargs

def custom_formatter(x, pos):
    """Custom formatter for the x and y axis
    It will format the axis in scientific notation,
    except for the values 0.1, 1 and 10.
    """
    # Check if x is one of the values you want to format differently
    if x in [0.1, 1, 10]:
        return f"{x:g}"
    else:
        # For other values, use scientific notation
        return rf"$10^{{{np.log10(x):.0f}}}$"