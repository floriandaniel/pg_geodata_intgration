import json
from urllib.parse import urlencode
from urllib.request import urlopen
import pandas as pd
import numpy
from simpledbf import Dbf5
from src.utils.check_kwargs import is_correct_kwargs
from ..utils.exceptions import OptionNotFound,ValueNotMatchOption
from geopandas import GeoDataFrame
from dbfread import DBF


def data_view(file_path, nb_rows_beg=5, nb_rows_end=5,nb_col_max = 5,**kwargs) :
	try:
		set_max_columns(nb_col_max+1)
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

		head = results.head(nb_rows_beg)
		tail = results.tail(nb_rows_end)
		display_dataframe(head,tail)
	
	except OptionNotFound as onf:
		print(onf, "v'là")

	except ValueNotMatchOption as vnmo:
		print(vnmo)

	reset_max_columns()
	reset_max_col_width()
	print(pd.get_option('display.max_colwidth'))


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