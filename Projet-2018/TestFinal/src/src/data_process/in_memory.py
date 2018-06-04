import json
from urllib.parse import urlencode
from urllib.request import urlopen
import pandas as pd
import numpy
import fiona
import ast, re
import json
from geopandas import GeoDataFrame
from shapely.geometry import shape
import re
from fiona.crs import to_string
# from osgeo import ogr,gdal,osr

from ..pre_processing.fileInfo import real_file,file_name,file_size,file_extension,file_count_sheets
from .data_info import coord_accepted

__all__ = ['in_memory']

def in_memory(file_path,position_depart,position_fin,**kwargs):
    """
    Renvoie un tableau sous forme de Dataframe, sélectionné grâce à des positions début et fin.

    :param file_path: chemin du fichier dont l'on veut obtenir des informations
    :type file_path: ``str``

    :param position_depart: représente les coordonnées en haut à gauche du tableau que l'on veut sélectionné
    :type position_depart: ``str``

    :param position_fin: représente les coordonnées en bas à droite du tableau que l'on veut sélectionné
    :type position_fin: ``str``

    :key worksheet: Précise la feuille que l'on veut extraire dans un fichier tableur

    :key type: Précise le type de fihcier que l'on veut extraire

        * *csv* (``str``) -- Fichier CSV (\*.csv)

        * *excel* (``str``) -- Fichier tableur Excel (\*.xls,\*.xlsx)

        * *geo* (``str``) -- Fichier géographique (\*.shp,\*tab,\*.geojson, ...)

    .. ipython:: python
    
        from src.data_process.in_memory import in_memory

        im = in_memory("../res/geo/subjects/42-loire/42-.shp","A,2","C,4",type="geo")
        im

    """

    type_of_file = kwargs.get("type")
    sheet = ""
    is_geo = False


    if type_of_file == "csv":
        dtframe = pd.read_csv(file_path)
    elif type_of_file == "excel":
        if "worksheet" in kwargs:
            sheet = kwargs.get("worksheet")
            dtframe = pd.read_excel(file_path,sheet_name=sheet)
    elif type_of_file == "geo":
        dtframe = GeoDataFrame.from_file(file_path)
        is_geo = True
    else: 
        print("Maybe error")
    
    # on prend les 5 premières lignes
    # dtframe2 = dtframe.head()

    # on récupère le nom des colonnes
    cols = list(dtframe.columns.values)

    # on transforme les paramètres en indices de lignes et de colonnes
    col_d,row_d = coord_accepted(position_depart)
    col_f,row_f = coord_accepted(position_fin)
    

    col_d_name = cols[col_d] 
    col_f_name = cols[col_f]
       
    # on sélectionne un sous-tableau, qui devient un dataframe
    dtframe = dtframe.loc[row_d-2:row_f, col_d_name:col_f_name]

    return dtframe
    
