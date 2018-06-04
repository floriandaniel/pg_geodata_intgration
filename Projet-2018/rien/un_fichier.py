#!/usr/bin/python3

from src.pre_processing.fileInfo import file_info
from src.pre_processing.download import download
from src.pre_processing.extract import extract

from src.data_process.data_view import data_view
from src.data_process.data_info import data_info
from src.data_process.in_memory import in_memory


# file_info("res/excels/commune.xls")
# file_info("res/archives/81-tarn.zip")
# file_info("res/geo/subjects/42-loire/42-.shp")
# file_info("res/geo/subjects/42-loire/42-.dbf")
# file_info("res/geo/mif/EXTRACT_POLYGON.mif")


une_var = download("https://www.insee.fr/fr/statistiques/fichier/2388572/filo-revenu-pauvrete-menage-2013.zip", target_folder=".")
print(une_var)

une_var2 = extract("res/archives/81-tarn.zip", target_folder=".", create_folder=None)
print(une_var2)

data_view("res/excels/commune.xls",nb_rows_beg=5,nb_rows_end=5,nb_col_max = 3,type="excel",worksheet="Donnees")


data_info("res/geo/subjects/42-loire/42-.dbf","A,2","C,4",type="geo")
en_memoire = in_memory("res/geo/subjects/42-loire/42-.dbf","A,2","C,4",type="geo")
print(en_memoire)