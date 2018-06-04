import json
from urllib.parse import urlencode
from urllib.request import urlopen
import pandas as pd
import numpy
from src.utils.check_kwargs import is_correct_kwargs
from ..utils.exceptions import OptionNotFound,ValueNotMatchOption
from geopandas import GeoDataFrame

__all__ = ['data_view']

def data_view(file_path, nb_rows_beg=5, nb_rows_end=5,nb_col_max = 5,**kwargs) :
	"""
	Prévisualisation des premières et dernières lignes d'un fichier "tableau" 

    :param file_path: chemin du fichier dont l'on veut obtenir des informations
    :type file_path: ``str``
    :param nb_rows_beg: nombre de lignes du début que l'on souhaite afficher (par défault, 5)
    :type nb_rows_beg: ``int``

    :param nb_rows_end: nombre de lignes de fin que l'on souhaite afficher (par défault, 5)
    :type nb_rows_end: ``int``

    :param nb_col_max: nombre de colonnes que l'on souhaite afficher (par défault, 5)
    :type position_fin: ``int``

    :key worksheet: Précise la feuille que l'on veut extraire dans un fichier tableur

    :key type: Précise le type de fihcier que l'on veut extraire

        * *csv* (``str``) -- Fichier CSV (\*.csv)

        * *excel* (``str``) -- Fichier tableur Excel (\*.xls,\*.xlsx)

        * *geo* (``str``) -- Fichier géographique (\*.shp,\*tab,\*.geojson, ...)

    .. ipython:: python
    
        from src.data_process.data_view import data_view

        di = data_view("../res/geo/subjects/42-loire/42-.shp",nb_rows_beg = 5,nb_rows_end=10,type="geo")

    """
	try:

		set_max_col_width(13)

		print(pd.get_option('display.max_columns'))
		is_correct_kwargs({'type':['excel','csv','geo'],'worksheet':'str'},kwargs)
		type_of_file = kwargs.get("type")


		if type_of_file == "excel" :
			worksheet = kwargs.get("worksheet")
			results = pd.read_excel(file_path,sheet_name=worksheet)

		elif type_of_file == "csv" :
			results = pd.read_csv(file_path)

		elif type_of_file == "geo" :
			results = GeoDataFrame.from_file(file_path)
		else : 
			results = pd.read_csv(file_path)

		cols = list(results.columns.values)
		max_col_name = cols[nb_col_max]
		results = results.loc[:,:max_col_name]

		head = results.head(nb_rows_beg)
		tail = results.tail(nb_rows_end)
		display_dataframe(head,tail)
	
	except OptionNotFound as onf:
		print(onf, "Option non trouvée.")

	except ValueNotMatchOption as vnmo:
		print(vnmo)

	reset_max_col_width()


def set_max_columns(new_max_cols) :
	pd.set_option('display.max_columns', new_max_cols)

def set_max_col_width(new_width) :
	pd.set_option('display.max_colwidth', new_width)

def reset_max_col_width() :
	pd.reset_option("display.max_colwidth")

def reset_max_columns() :
	pd.reset_option("display.max_columns")


def display_dataframe(beg,end) :
	print(beg)
	print(".. | .."+"\n.. | .."+"\n.. | .."+"\n.. v ..")
	print(end)





# Pour la projection
# https://gis.stackexchange.com/questions/7608/shapefile-prj-to-postgis-srid-lookup-table/7633