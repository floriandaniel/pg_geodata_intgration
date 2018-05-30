import json
from urllib.parse import urlencode
from urllib.request import urlopen
import pandas as pd
import numpy
from simpledbf import Dbf5
from check_kwargs import is_correct_kwargs
from dbfread import DBF

xlfilePath = "commune.xls"
dbf_file = "42-.dbf"
# xl_file = pd.ExcelFile((xlfilePath)
# dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}

# dfs.loc[2].values
# dfs.loc[2]

# df = pd.read_csv(xlfilePath)

# df2 = pd.DataFrame(df, index = ['a1', 'a2', 'a3'], columns = ['A', 'B', 'C', 'D'])

# ar = numpy.array([[1.1, 2, 3.3, 4], [2.7, 10, 5.4, 7], [5.3, 9, 1.5, 15]])
# df1 = pd.DataFrame(ar, index = ['a1', 'a2', 'a3'], columns = ['A', 'B', 'C', 'D'])

# print(df.loc[2])
# print("\n")
# print(df)
# print("\n")
# print(df2)

# print("\n")
# print(df1)


def data_view(file_path, worksheet, nb_rows_beg=5, nb_rows_end=5,nb_col_max = 10,**kwargs) :
	
	# pd.set_option('display.height', 1000)
	# pd.set_option('display.max_rows', 2500)
	# pd.set_option('display.max_columns', 1500)
	# pd.set_option('display.width', 2000)

	if is_correct_kwargs({'type':['excel','csv','geo']},kwargs) == True :
		print(True)
	else :
		print(False)

	
	# set_max_columns(nb_col_max)
	type_of_file = kwargs.get("type")

	if type_of_file == "excel" :
		results = pd.read_excel(file_path,sheet_name=worksheet)
	elif type_of_file == "csv" :
		results = pd.read_csv(file_path)
	elif type_of_file == "geo" :
		dbf = DBF(file_path)
		results = pd.DataFrame(iter(dbf))
	else : 
		results = pd.read_csv(file_path)


	head = results.head(nb_rows_beg)
	tail = results.tail(nb_rows_end)
	display_dataframe(head,tail)
	


# def build_array(nb_col_max,nb_rows_beg,nb_rows_end) :
# 	return 


def set_max_columns(new_max_cols) :
	pd.set_option('display.max_columns', new_max_cols)


def display_dataframe(beg,end) :
	print(beg)
	print(".. | .."+"\n.. | .."+"\n.. | .."+"\n.. v ..")
	print(end)



data_view(dbf_file,"Donnees",5,6,10,type="geo")

# Pour la projection
# https://gis.stackexchange.com/questions/7608/shapefile-prj-to-postgis-srid-lookup-table/7633




