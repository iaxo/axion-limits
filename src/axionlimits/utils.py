import shutil
import os
import ast
import re
import numpy as np
from importlib.resources import files
from pylatexenc.latex2text import LatexNodes2Text
from shapely.geometry import Polygon
import matplotlib.colors as mcolors

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

def get_polygon_max_shrink_distance(polygon, precision=1e-4):
    """
    Get the maximum distance that can be applied to a polygon without causing self-intersections.

    Parameters
    ----------
    polygon : shapely.geometry.Polygon
        The polygon to shrink.
    precision : float, optional
        The precision of the calculation.
    """

    # Gross approximation of the maximum buffer distance
    d = polygon.area**0.5 * 1e-5 # use sqrt(area) as estimate of the characteristic length of the polygon
    multiplier = 1.5
    while True:
        d *= multiplier
        polygon_mod = polygon.buffer(-d)
        if polygon_mod.is_empty:
            break

    # Fine tune the buffer distance
    min_d = d/multiplier
    max_d = d
    while (max_d - min_d) / min_d > precision:
        d = (max_d + min_d) / 2
        polygon_mod = polygon.buffer(-d)
        if polygon_mod.is_empty:
            max_d = d
        else:
            min_d = d

    return min_d

def shrink_mpl_polygon(polygon, shrunk_factor, max_distance=None, logscale=False):
    """
    Shrink a matplotlib Polygon object by a given factor.

    Parameters
    ----------
    polygon : matplotlib.patches.Polygon
        The polygon to shrink.
    shrunk_factor : float
        The factor by which to shrink the polygon.
    max_distance : float, optional
        The maximum distance to shrink the polygon. If None, it will be calculated.
    logscale : bool, optional
        If True, the polygon is in logscale, so the polygon will be built on the transformed coordinates,
        shrunk and then transformed back to the original coordinates.
    """
    # Get the vertices of the polygon
    path = polygon.get_path()
    vertices = path.vertices
    # Apply the transform if it is in logscale
    if logscale:
        transformation = polygon.get_transform()
        vertices = transformation.transform(vertices)
    polygon_coords = vertices.tolist()

    # Create a shapely Polygon from the coordinates
    shapely_polygon = Polygon(polygon_coords)

    # Shrink the polygon
    if max_distance is None:
        max_distance = get_polygon_max_shrink_distance(shapely_polygon)
    distance = shrunk_factor * max_distance
    shrunken_polygon = shapely_polygon.buffer(-distance)

    # transform back to original coordinates
    if logscale:
        x, y = shrunken_polygon.exterior.xy
        xy = list(zip(x, y))
        xy = transformation.inverted().transform(xy)
        shrunken_polygon = Polygon(xy)

    return shrunken_polygon

def mpl_to_shapely(polygon, logscale=False):
    """
    Convert a matplotlib Polygon object to a shapely Polygon object.
    """
    # Get the vertices of the polygon
    path = polygon.get_path()

    # Apply the transform if it is in logscale
    if logscale:
        transformation = polygon.get_transform()
        path = path.transformed(transformation)
    
    # Get the vertices of the polygon
    vertices = path.vertices
    # Convert the vertices to a list of tuples
    polygon_coords = vertices.tolist()

    # Create a shapely Polygon from the coordinates
    shapely_polygon = Polygon(polygon_coords)
    return shapely_polygon

def generate_colors_with_alpha(color_name, alpha_min=0.0, alpha_max=1.0, n=10):
    """
    Genera un vector de N colores con valores alpha equiespaciados entre alpha_min y alpha_max.

    Args:
        color_name (str or tuple): Nombre del color o tupla RGB.
        N (int): Número de colores a generar.
        alpha_min (float): Valor mínimo de alpha (entre 0 y 1).
        alpha_max (float): Valor máximo de alpha (entre 0 y 1).

    Returns:
        list of tuples: Lista de colores en formato RGBA.
    """
    
    rgb = mcolors.to_rgb(color_name)
    alphas = np.linspace(alpha_min, alpha_max, n)
    rgba_colors = [[rgb[0], rgb[1], rgb[2], alpha] for alpha in alphas]
    
    return rgba_colors


def rgba_to_rgb(rgba, background_rgba=(1, 1, 1, 1)):
    """
    Convert an RGBA color to RGB with a given background color.

    Parameters
    ----------
    rgba : array-like
        The RGBA color to convert.
    background_rgba : array-like, optional
        The background color in RGBA format.
        Default is white.
    
    Returns
    -------
    array-like
        The RGB color.
    """

    rgba = np.array(rgba, ndmin=2) # ensure input is 2D for generalization
    background_rgba = np.array(background_rgba)
    
    # Perform RGBA to RGB conversion
    rgb = (1 - rgba[:, 3, None]) * background_rgba[:3] + rgba[:, 3, None] * rgba[:, :3]
    
    return np.squeeze(rgb) # squeeze to recover input dimensionality
