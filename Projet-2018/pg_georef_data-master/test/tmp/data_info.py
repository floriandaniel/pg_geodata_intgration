import json
from urllib.parse import urlencode
from urllib.request import urlopen
import pandas as pd
import numpy
from simpledbf import Dbf5
from dbfread import DBF
import ast, re
from dbfread import DBF
import dbfread
from ..pre_processing.fileInfo import real_file,file_name,file_size,file_extension,file_count_sheets


def data_info(file_path) :
	if get_extension(file_path) == "dbf" :
		print("allo")
	
	# results = pd.read_excel("commune.xls",sheet_name="Donnees")
	# head = results.head(5)
	# tail = results.tail(5)

	# print(head)
	# print(".. | .."+"\n.. | .."+"\n.. | .."+"\n.. v ..")
	# print(tail)

	# result1 = results.loc[0][0]
	# result2 = results.loc[0][1]

	# print(type(result2))
	# print("[{}][{}] --> {}".format(0,0,result1))
	# print("[{}][{}] --> {}".format(0,1,result2))

	print(type('00.1'))

	dbf = DBF("81-.dbf")
	# print("{}".format(dbf.fields))
	# print(dbf.records[0])

	print("type"+str(ast.literal_eval('1')))
	print("{}".format(type(ast.literal_eval('200.0'))))
	print(type(df.dtypes))

	# Number of rows in .dbf file
	print(len(dbf))

	# Number of columns in .dbf file
	print(len(dbf.fields))



	# ast to determine the type of an object from a string

def get_projection(prj_file) :

	with open(prj_file, 'r') as fp:
	    prj_txt = fp.read()

	query = urlencode({
	    'exact': True,
	    'error': True,
	    'mode': 'wkt',
	    'terms': prj_txt})

	webres = urlopen('http://prj2epsg.org/search.json', query.encode())
	jres = json.loads(webres.read().decode())

	results = jres['codes'][0]

	return results['name'],results['code']

# def get_attributes(dbf_file) :
# 	return 

def get_extension(file_path) :
	return file_extension(file_path)


data_info("tmp/81-.dbf")