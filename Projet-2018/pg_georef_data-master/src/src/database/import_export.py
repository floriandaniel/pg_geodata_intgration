#!/usr/bin/python3

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine.url import URL
import geopandas as gpd
import pandas as pd
from geoalchemy2 import Geometry, WKTElement

from ..data_process.data_info import get_projection

def ImportFromDataframe(engine, dataframe, table_name, schema=None,if_exists='append', srid=-1):
	"""
	3 choices for "if_existe" arg : fail, replace, append, 
	"""
	if is_geodataframe(dataframe):
		geometry_col = find_geometry_column(dataframe)
		print("si")
		print(geometry_col)

		dataframe['geom'] = dataframe[geometry_col].apply(lambda x: WKTElement(x.wkt, srid=srid))
		dataframe.drop(geometry_col, 1, inplace=True)
		dtype={'geom': Geometry('GEOMETRY', srid=srid)}
	else:
		print("else")
		dtype = None

	#drop the geometry column as it is now duplicative
	dataframe.to_sql(table_name, engine, schema=schema,if_exists=if_exists, index=False, dtype=dtype)


def ExportToDataframe(engine, table_name, crs=None):
	query = ("select \"X_CHF_LIEU\", geom from gnnnnn where \"X_CHF_LIEU\"={a}").format(a=8253)
	dataframe = gpd.GeoDataFrame.from_postgis(query,engine, geom_col='geom',crs={'init':'epsg:2154'})
	print(dataframe.crs)
	return dataframe

def FastExportToDataframe(engine, table_name, crs=None):
	query = ("select * from \"{table}\"").format(table=table_name)
	dataframe = gpd.GeoDataFrame.from_postgis(query,engine, geom_col='geom',crs={'init':'epsg:2154'})
	print(dataframe.crs)
	
	return dataframe
	

def ExportToShapefile(dataframe, path_name):
	return dataframe.to_file(path_name, driver="ESRI Shapefile")


def ExportToGeojson(dataframe, path_name):
	return dataframe.to_file(path_name, driver="GeoJSON")


def ExportToMapinfo(dataframe, path_name):
	return dataframe.to_file(path_name, driver="MapInfo File")


def reproject(geodataframe, crs=None, epsg=None):
	if crs is None:
		result = geodataframe.to_crs(epsg=epsg)
	else:
		result = geodataframe.to_crs(crs=crs)

	return result


def find_geometry_column(dataframe):
	return dataframe.geometry.name

def is_geodataframe(dataframe):
	if isinstance(dataframe, gpd.GeoDataFrame):
		return True
	else:
		return False




# INSERTION, UPDATE, DELETE
# CREATE SCHEMA, DELETE SCHEMA
# CREATE TABLE, DELETE SCHEMA
# INSERT, UPDATE, DELETE ROWS