import os
from importlib.resources import files

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