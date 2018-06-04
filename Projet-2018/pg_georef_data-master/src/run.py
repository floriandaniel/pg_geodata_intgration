#!/usr/bin/python3

"""
from geopandas import GeoDataFrame
from src.pre_processing import download,fileInfo,extract
from src.data_process import data_info, data_view
from src.utils import folder,check_kwargs
import sys
import json
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import fiona
import urllib, geojson, gdal, subprocess
from fiona.crs import to_string
from osgeo import ogr,gdal,osr
from sqlalchemy_utils import create_database,drop_database,database_exists
import matplotlib.pyplot as plt
from src.database import import_export
"""
from src import file_info


file_info("res/archives/81-tarn.zip")
# EXEMPLES D'UTILISATION DES METHODES
# data_view.data_view("res/excels/commune.xls",5,5,5,type="excel",worksheet="Donnees")
# data_view.data_view("data.geojson",5,5,10,type="geo")
# data_view.data_view("res/geo/subjects/42-loire/42-.shp",5,5,10,type="geo")
# data_view.data_view("res/csv/menus_de_cantines.csv",5,5,10,type="csv")



# data_view.data_view("res/excels/commune.xls",5,5,5,type="excel",worksheet="Donnees")
# data_info.data_info("destination_data.shp","A,1","B,3",type="geo")
# data_info.data_info("res/csv/agenda_nantes.csv","A,1","G,3",type="csv")
# data_view.data_view("res/geo/subjects/42-loire/42-.shp",5,5,10,type="geo")
# data_view.data_view("res/csv/menus_de_cantines.csv",5,5,10,type="csv")





# lis = download("https://www.insee.fr/fr/statistiques/fichier/2388572/filo-revenu-pauvrete-menage-2013.zip","grfcv")
# print(lis)
# extract("/srv/geodata/download/42-loire.zip","grfcv/",name_folder="auto")





# #
# #   GEOGRAPHIE
# ######################################################

# print("GEO-GEO-GEO-GEO-GEO-GEO-GEO-GEO")
# data_view.data_view("res/geo/subjects/42-loire/42-.dbf",type="geo")

# ##
# ##   CSV
# ######################################################
# print("CSV-CSV-CSV-CSV-CSV-CSV-CSV-CSV")
# data_view.data_view("res/csv/agenda_nantes.csv",type="csv")


# ##
# ##   EXCEL
# ######################################################
# print("XCEL-XCEL-XCEL-XCEL-XCEL-XCEL-XCEL-")
# data_view.data_view("res/excels/commune.xls",type="excel",worksheet="Donnees")

# Si on se trompe de feuilles, il faut en proposer d'autres ;)





# #
# #   GEOGRAPHIE
# ######################################################

# print("GEO-GEO-GEO-GEO-GEO-GEO-GEO-GEO")
# dt1 = data_info.data_info("res/geo/subjects/42-loire/42-.dbf","A,1","C,1",type="geo")

# ##
# ##   CSV
# ######################################################
# print("CSV-CSV-CSV-CSV-CSV-CSV-CSV-CSV")
# dt2 = data_info.data_info("res/csv/agenda_nantes.csv","A,1","C,1",type="csv")


# ##
# ##   EXCEL
# ######################################################
# print("XCEL-XCEL-XCEL-XCEL-XCEL-XCEL-XCEL-")
# dt3 = data_info.data_info("res/excels/commune.xls","A,1","C,1",type="excel",worksheet="Donnees")


# print(dt1)
# print(dt2)
# print(dt3)

# print(type(dt1))
# print(type(dt2))
# print(type(dt3))

# from sqlalchemy import create_engine
# from geoalchemy2 import Geometry, WKTElement

# engine = create_engine('postgresql://postgres:ifsttar@137.121.74.24:5432/maps',echo=True,client_encoding='utf8')
# # # # dt1.to_sql('first-geo', engine)
# # dt1['geom'] = dt1['geometry'].apply(lambda x: WKTElement(x.wkt, srid=2154))

# # print(dt1.head())
# # #drop the geometry column as it is now duplicative
# # dt1.drop('geometry', 1, inplace=True)
# # print(dt1.head())

# # dt1.to_sql('gnnnnn', engine, if_exists='append', index=False, dtype={'geom': Geometry('GEOMETRY',srid=2154)})

# # sql= "select geom, x,y,z from your_table"
# # query = ("select \"X_CHF_LIEU\", geom from gnnnnn where \"X_CHF_LIEU\"={a}").format(a=8253)
# # dt45 = dt1.from_postgis(query,engine, geom_col='geom',crs={'init': 'epsg:2154'})


# # print("dt1.crs = "+str(dt1.crs))
# # print(data_info.get_projection("res/geo/subjects/42-loire/42-.dbf"))
# # print(dt45.head())
# # print("dt45.crs = "+str(dt45.crs))

# # d = dt45.to_crs(epsg=4326) 
# # print(type(d))
# # print(d.head())
# # print("dt45.crs = "+str(d.crs))

# import_export.ImportFromDataframe(engine, dt1,'aloha',srid=2154)
# dfr = import_export.ExportToDataframe(engine,"gnnnnn")
# print(dfr)

# d = dfr.to_crs(epsg=4326)
# print(d.crs) 
# print(d)
# # d.plot()
# # dt45.plot()

# # plt.show()

# print(fiona.supported_drivers)

# # import_export.ExportToGeojson(dfr,"a")
# # import_export.ExportToGeojson(dt2,"b")

# # wkt_element_1 = WKTElement('POINT(5 45)')
# # wkt_element_2 = WKTElement('POINT(5 45)', srid=4326)
# # print(wkt_element_1)
# # print(wkt_element_2)
# # el = WKTElement("SRID=4326; POINT(4.1,52.0)")
# # print(el)

# dictionnaire = {
#     'shape':'ESRI Shapefile',
#     'geojson':'GeoJSON',
#     'mapinfo':'MapInfo File'
# }

# # d.to_file('1e.map', driver="MapInfo File")


# file_path = "res/archives/81-tarn.zip"
# fileInfo.file_info("res/geo/subjects/42-loire/42-.shp")
# extract("res/archives/file.gz", target_folder="./")

# data_view.data_view("res/excels/commune.xls",nb_rows_beg=5,nb_rows_end=5,nb_col_max = 3,type="excel",worksheet="Donnees")
# data_info.data_info("res/geo/subjects/42-loire/42-.dbf","A,2","C,4",type="geo")















































# driver = gdal.IdentifyDriver('destination_data.shp')
# shape = ogr.Open('EXTRACT_POLYGON.mid')
# shape = ogr.Open('res/geo/subjects/42-loire/42-.shp')
# ogrinfo -so -al destination_data.shp


# ds=gdal.Open('EXTRACT_POLYGON.mid')
# prj=ds.GetProjection()
# print(prj)

# with open('EXTRACT_POLYGON.tab') as f:
#     table = pd.read_table(f)
# print(str(table))

# print('\n\n')
# shops = GeoDataFrame.from_file("res/geo/subjects/42-loire/42-.dbf")
# print(shops.head())
# dtframe = shops.head()

# cols = list(dtframe.columns.values)
# cols = cols[1:3]
# dtframe = dtframe.loc[1:5, 'SUPERFICIE':'CODE_CANT']
# print(dtframe)
# print(cols)


# d = shops.to_json()

# dat = json.loads(d)
# print(len(dat['features']))

# charts = {}
# for feature in dat['features']:
#     one_type = feature['geometry']['type']
#     if one_type not in charts.keys():
#         charts[one_type] = 1
#     else:
#         charts[one_type] += 1

# print(charts)



# data_info.data_info("res/geo/subjects/42-loire/42-.dbf","A,1","F,15",type="geo")



# data_info.data_info("res/excels/commune.xls","A,0","D,2",type="excel", sheet="Donnees")
# dtframe = pd.read_excel("res/excels/commune.xls",sheet_name='Donnees')

# data_info.coord_accepted("aaaa,22")



###############################################################################################


from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.engine.url import URL
import numpy as np

# engine1 = create_engine('postgresql://postgres:ifsttar@137.121.74.24:5432/maps',echo=True,client_encoding='utf8')

# # db_name = "test"
# # engine.execute("CREATE DATABASE {}".format("db")).execution_options(isolation_level="AUTOCOMMIT")
# # # conn.execute("CREATE DATABASE %s  ;" % db_name)
# Session = sessionmaker(bind=engine1)

# # create a database connection
# engine1.connect()

# session = Session()
# # res = engine.execute("select 1 as is_alive;")
# metadata = MetaData(engine1)
# print(str(res))
# print(metadata.tables.keys())    
# village_table = Table('village',metadata,schema="dpt",autoload=True)


# # create an Insert object
# ins = village_table.insert()
# # add values to the Insert object
# new_village = ins.values(abc="Joe")
 
# conn = engine1.connect()
# # add user to database by executing SQL
# # conn.execute(new_village)


# metadata=MetaData(bind=engine1)
# main_table=Table('sample',metadata,            
#             Column('LIN',String(10),primary_key=True),
#             Column('material_type',String(20),nullable=False),
#             Column('source',String(20),nullable=False),
#             Column('material_description',String(100)),
#             Column('quantity',Integer),
#             Column('location',String(2)),
#             Column('received_by',String(20)),
#             Column('received_date',DateTime,nullable=False),
#             schema='dpt')

# metadata.create_all()

# # from sqlalchemy.schema import CreateSchema
# # engine.execute(CreateSchema('my_schema'))
# df = pd.DataFrame(np.random.randn(6,4),columns=list('ABCD'))
# print(df)
# df.to_sql('vilage', engine1,schema="dpt")

# session.commit()

# if not engine.dialect.has_table(engine, 'village', schema = 'dbo')

# page_table = schema.Table('page', metadata,
#     schema.Column('id', types.Integer, primary_key=True),
#     schema.Column('name', types.Unicode(255), default=u''),
#     schema.Column('title', types.Unicode(255), default=u'Untitled Page'),
#     schema.Column('content', types.Text(), default=u''),
# )

# ins = page_table.insert(
#     values=dict(name=u'test', title=u'Test Page', content=u'Some content!')
# )

# print(ins)
# result = conn.execute(ins)
# print(result)




























# connection = Connexion()
# conn, session, engine, metadata = connection.connect('postgresql')

# main_table = Table('sample',metadata,            
#             Column('LIN',String(10),primary_key=True),
#             Column('material_type',String(20),nullable=False),
#             Column('source',String(20),nullable=False),
#             Column('material_description',String(100)),
#             Column('quantity',Integer),
#             Column('location',String(2)),
#             Column('received_by',String(20)),
#             Column('received_date',DateTime,nullable=False),
#             schema='dpt')

# metadata.create_all()
# session.commit()
# session.rollback()

# connection.disconnect(conn, session, engine)

# url = {'driver':'postgresql',
#        'username':'postgres',
#        'password':'ifsttar',
#        'host':'137.121.74.24',
#        'port':'5432'
# }

# db = Database()
# db.createDatabase(url,"florian2")

# OperationalError, 