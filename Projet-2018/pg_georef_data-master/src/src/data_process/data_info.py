import json
from urllib.parse import urlencode
from urllib.request import urlopen
import pandas as pd
import numpy
import fiona
from dbfread import DBF
import ast, re
import dbfread
from messytables import type_guess
import json
from geopandas import GeoDataFrame
import geojson
from shapely.geometry import shape
import re
from fiona.crs import to_string
from osgeo import ogr,gdal,osr

from ..pre_processing.fileInfo import real_file,file_name,file_size,file_extension,file_count_sheets

__all__ = ['data_info']

def data_info(file_path,position_depart,position_fin,**kwargs):
    """
    Afficher les informations relatives à un sous-tableau dans un fichier, sélectionné grâce à des positions.

    :param file_path: chemin du fichier dont l'on veut obtenir des informations
    :type file_path: ``str``
    :param position_depart: représente les coordonnées en haut à gauche du tableau que l'on veut sélectionné
    :type position_depart: ``str``

    :param position_fin: représente les coordonnées en bas à droite du tableau que l'on veut sélectionné
    :type position_fin: ``str``

    :key worksheet: Précise la feuille que l'on veut extraire dans un fichier tableur

        * *manual* (``str``) -- Place l'archive dans un dossier comportant le nom de l'

        * *auto* (``str``) -- Additional content

    :key type: Précise le type de fihcier que l'on veut extraire

        * *csv* (``str``) -- Fichier CSV (\*.csv)

        * *excel* (``str``) -- Fichier tableur Excel (\*.xls,\*.xlsx)

        * *geo* (``str``) -- Fichier géographique (\*.shp,\*tab,\*.geojson, ...)

    .. ipython:: python
    
        from src.data_process.data_info import data_info

        di = data_info("../res/geo/subjects/42-loire/42-.shp","A,1","C,4",type="geo")

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
    col_f_name = cols[col_f+1]
        
    # on sélectionne un sous-tableau, qui devient un dataframe
    dtframe = dtframe.loc[row_d:row_f, col_d_name:col_f_name]
    
    
    # on détecte les types de chaque colonne
    types = detect_types(dtframe)


    cols = cols[col_d:col_f+1]
    


    print("\n")
    print("----- Nombre de lignes -----")
    number_of_rows = row_f-row_d+1
    number_of_cols = len(cols)

    print("Rows : {}".format(number_of_rows))
    print("Columns : {}".format(number_of_cols))

    print("\n")
    print("----- Attributs/types -----")

    # on affiche les types de chaque colonne
    for i in range(0,len(cols)):
        print("{} ({})".format(cols[i],types[i]))

    print("\n")
    print("----- Géographie -----")

    if is_geo:
        print("Fichier géographique : oui")
        name, epsg, url_epsg, area, scope, n = get_projection(file_path)
        print("\n")
        print("----- Projection -----")
        print("Name : {} (epsg:{}) -- {}".format(name,epsg,n))

        visible_url = url_epsg.split(".")
        visible_url = ".".join(visible_url[:-1:])
        
        print("URL : {}".format(visible_url ))
        print("Area and scope : {} \n{})".format(area,scope))
    else :
        print("Fichier géographique : non")


def can_evaluate(string):
    try:
        return type(eval(string))
    except Exception :
        return type("e")


def detect_types(results, **kwargs):
    

    # on créé les dataframes suivant les types de fichier

    real_dataframe = results

    classement = []

    list_columns = list(real_dataframe)
    for column in list_columns :
        dico ={}
        items = real_dataframe[column].tolist()
        # print("colonne, items = "+str(column)+" "+str(items))
        
        for item in items:
            
            item = str(item)
            # print("item "+str(item))
            item = item.replace(' ','')
            # print("item after replace = "+item)
            typef = can_evaluate(item)
            # print("typef = "+str(typef))

            if typef in dico:
                dico[typef] += 1
            else:
                # print("typef = "+str(typef))
                dico[typef] = 1
    
        # print("\ndic =="+str(dico)+"\n")
        typed = determine_final_type(dico)
        typed = typed.split("'")
        classement.append(typed[1])
    
    return classement


def determine_final_type(dico):
    # on trie le dictionnaire qu'on nous a donné en paramètre
    s_data = sorted(dico.items(), key=lambda item: item[1],reverse=True)
    # on veut récupérer la valeur qui a servi de clé pour le dictionnaire
    return str(s_data[0][0])

def get_projection(file_path):

    wkt = proj42wkt(file_path)

    name, epsg, url_epsg = wkt2srid(wkt)
    area, scope, n = get_info_epsg(url_epsg)

    return name, epsg, url_epsg, area, scope, n



def proj42wkt(file_path):

    c = fiona.open(file_path)
    "res/geo/subjects/42-loire/42-.dbf"
    prj4 = to_string(c.crs)

    sr = osr.SpatialReference()
    sr.ImportFromProj4(prj4)
    wkt = sr.ExportToWkt()

    return wkt


def wkt2srid(wkt):
    query = urlencode({
        'exact': True,
        'error': True,
        'mode': 'wkt',
        'terms': wkt})

    webres = urlopen('http://prj2epsg.org/search.json', query.encode())
    jres = json.loads(webres.read().decode())

    # on s'occupe que du premier système de référence spatial (le principal) 
    results = jres['codes'][0]


    name = results['name']
    epsg = results['code']
    url_epsg = results['url']

    return name, epsg, url_epsg


def get_info_epsg(url_epsg):

    with urlopen(url_epsg) as url:
        data = json.loads(url.read().decode())

    area = data['area']
    scope = data['scope']
    n = data['name']

    return area, scope, n

def info_features(file_path):
    """
    Only for geodata files
    .dat,excel,xls ne marche pas
    .mid .mif .shp .dbf .shx .tab
    """

    # on créé un GeoDataFrame à partir du fichier
    gdf = GeoDataFrame.from_file(file_path)

    d = gdf.to_json()
    print(d)

    # on charge le json
    dat = json.loads(d)

    # on affiche de composants graphiques (POLYGON, LINESTRING, ...)
    print(len(dat['features']))

    # on affiche le nombre de POLYGONS, LINESTRING, ...
    charts = {}
    for feature in dat['features']:
        one_type = feature['geometry']['type']
        if one_type not in charts.keys():
            charts[one_type] = 1
        else:
            charts[one_type] += 1

    # on affiche le dictionnaire associant forme et nombre d'apparitions
    print(charts)

def coord_accepted(coord):
    """
    Analyse de chaînes pour les coordonnées
    """

    """
    Principe général un projet -->
        on veut que l'utilisateur signale une position.
        On s'inspire de celle d'excel et LibreCalc. 
        Des lettres pour les colonnes, des nombres pour les lignes

        Attention plus de 26 colonnes, on passe à AA, le numéro de colonnes sera 27.

    """
    if not bool(re.match('[a-zA-Z]*,[0-9]*', coord)):
        # Raise errors
        pass

    coord = coord.lower()
    tab = coord.split(',')
    index_col = tab[0] 
    index_line = tab[1]
    

    alphabet = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,
        'j':10,'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,
        't':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}



    value_word = 0
    if len(index_col) > 1:  
        for letter in index_col[:-1]:
            value_word += alphabet[letter]*26
    
    value_word += alphabet[index_col[-1]]
    
    
    return value_word-1,int(index_line)