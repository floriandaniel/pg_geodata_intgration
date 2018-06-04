#!/usr/bin/python3
from hurry.filesize import size, alternative

import os
import magic
import mimetypes
import pandas as pd
from os.path import isdir

# IMPORTS

from ..utils.folder import get_files_directory

# -------INFO FILE-------

"""
    Implémentation de la proclamation de la bonne parole.
    Usage
    >>> from sm_lib import proclamer
    >>> proclamer()
"""


__all__ = ['file_info']


def file_info(file_path):

    """
    Affiche les informations d'un document (nom, taille, extension, ...)

    :param file_path: chemin du fichier ou du dossier
    :type file_path: ``str``


    .. ipython:: python

        from src.pre_processing.fileInfo import file_info
       
        infos = file_info("../res/archives/81-tarn.zip")
        infos_excel = file_info("../res/excels/commune.xls")
        error_infos = file_info("../.e//xcels/commune.xls")

    """

    # check if it's an excel file
    # make a config file with spreadsheets formats
    # là ils sont codés en dur

    try:
        if isdir(file_path):
            files = get_files_directory(file_path, path="yes")

            for file in files:
                display_info(file)
        else:
            if real_file(file_path):
                display_info(file_path)

    except FileNotFoundError as error:
        print('FileNotFoundError : File not found. Check your path.')

    except Exception as e:
        print(e, 'Unknown error.')


def real_file(file_path):
    """
    Indique si le fichier existe dans l'arborescence indiquée en paramètre.

    :param file_path: chemin du fichier cible
    :type file_path: str
    :return: vrai si le file_path est un fichier,
        une exception dnas les autres cas
    :rtype: ``bool``

    :raises FileNotFoundError: le fichier n'a pas été trouvé
    """

    if os.path.isfile(file_path):
        return True
    else:
        raise FileNotFoundError


def file_name(file_path):
    """
    Retourne le nom du fichier, sans l'extension

    :param file_path: chemin du fichier cible
    :type file_path: str

    :return: le nom du fichier indiqué en paramètre
    :rtype: ``str``

    """
    name = os.path.basename(file_path)

    return name


def file_extension(file_path):
    """
    Indique l'extension d'un fichier. Dans notre cas, on considère le suffixe comme tel.

    :param file_path: chemin du fichier cible
    :type file_path: str
    :return: l'enxtension du fihcier
    :rtype: ``str``
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension


def file_size(file_path):
    """
    La taille du fichier en bits, et en unité conventionnelle plus lisible pour l'utilisateur.

    :param file_path: chemin du fichier cible
    :type file_path: str
    :return: la taille du fichier en bits et dans une unité à l'échelle (Mio,Gio,Tio)
    :rtype: ``float``

    """
    sizeBytes = os.path.getsize(file_path)
    readingSize = size(sizeBytes, system=alternative)

    return sizeBytes, readingSize


def file_count_sheets(file_path):
    """
    Indique le nombre de feuilles si le fichier est un tableau

    :param file_path: chemin du fichier cible
    :type file_path: str
    :return: nombre de feuilles pour les fichiers Excel et autres(.xls, ...)
    :rtype: ``int``

    """
    xl = pd.ExcelFile(file_path)
    countSheets = len(xl.sheet_names)

    return countSheets


def path_folder(file_path):
    """
    Indique le chemin absolu d'un fihcier passé en paramètre

    :param file_path: chemin du fichier cible
    :type file_path: str
    :return: une chaîne de caractères étant le chémin absolu
    :rtype: ``str``

    """
    path_folder = dirname(abspath(file_path))

    return path_folder


def display_info(file_path):
    """
    Affiche les les informations dans la sortie standard

    :param file_path: chemin du fichier cible
    :type file_path: str
    :return: une chaîne de caractères regroupant les prinicpales informations du fichier
    :rtype: ``str``

    """
    name = file_name(file_path)
    extension = file_extension(file_path)
    size_bytes, size_unit = file_size(file_path)

    print("------"+file_path+"------")
    print("name : {}".format(name))
    print("type : {}".format(extension))
    print("size : {} ({} bytes)".format(size_unit, size_bytes))

    if file_path.endswith((".xls", ".xlsx")):
        sheets_count = file_count_sheets(file_path)
        print("number of sheets : {}".format(sheets_count))


# Exemples d'utilisation de la méthode file_info

# file_info("memory.png")
# file_info("file1.csv")
# file_info("fileInfo.py")
# file_info("fileOut.csv")
# file_info("memory.png")
# file_info("memorydq.png")
