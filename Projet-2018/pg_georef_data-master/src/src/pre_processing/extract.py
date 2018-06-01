#!/usr/bin/python3

from patoolib import extract_archive, test_archive, list_archive
from patoolib.util import PatoolError
import urllib.parse
from os import listdir
from os.path import join,isfile,dirname,abspath,isdir
import urllib.request
from .fileInfo import file_extension, file_name
from ..utils.folder import get_files_directory,add_slash2path
from ..utils.exceptions import TmpFolderAlreadyExists
import os
import shutil

__all__ = ['extract']

def extract(file_path, target_folder = "/srv/geodata/download/", create_folder=None) :
	"""
	Extraire une archive d'un chemin donné, vers un dossier cible. Possibilité de personnaliser.

	:param file_path: chemin du fichier que l'on va extraire
	:type file_path: ``str``
	:param target_folder: dossier cible où va être extrait l'archive
		
		* *par défault* -- ``/srv/geodata/download/``

	:type target_folder: ``str``

	:key name_folder: Personnalise la structure du dossier cible

		* *manual* (``str``) -- Place l'archive dans un dossier comportant le nom de l'

		* *auto* (``str``) -- Additional content

	.. ipython:: python
	
		from src.pre_processing.extract import extract

		archive_extracted2 = extract("../res/archives/file.gz","./","yes")
		archive_extracted2

	"""

	target_folder = add_slash2path(target_folder)
	name = file_name(file_path)
	filename, file_extension = os.path.splitext(name)

	# print("liste_archive = "+str(type(list_archive(file_path))))

	try:
		temp_folder = "tmp"
		if not isdir(temp_folder) :
			os.makedirs(temp_folder)
			extract_archive(file_path, verbosity=0,outdir="tmp", interactive=False)

			if contains_geo_files(temp_folder):
				path_from_filepath = dirname(abspath(file_path))
				outdir_folder = ''.join([target_folder,filename])
			else :
				if create_folder is None :
					outdir_folder = target_folder
				
				else:
					outdir_folder = ''.join([target_folder,filename])	

			result = move_all_files_directory(temp_folder,outdir_folder)
		
			print("Archive extraite vers \"{}\"".format(outdir_folder))
			shutil.rmtree(temp_folder)

		else:
			raise TmpFolderAlreadyExists()

		return result

	except TmpFolderAlreadyExists as e :
		print(e,"Le dossier temporaire \"tmp\" existe déjà")

	except PatoolError as error:
		print(str(error)+"""
			\nFichier non trouvé ou extension non compatible.""")
	
	except Exception as exception:
		print(exception)

	except TypeError as t_error:
		print(t_error,"dbdfuidf")	

		# le nom est trompeur, on pratique ici un déplacement de fichier
		# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

		# if not isdir(target_folder) :
		# 	os.makedirs(target_folder)

			
		
			
		# 	# move_all_files_directory(local_tmp_folder,target_folder+filename)

		# 	else : 
		# 		print("WARN")

		# else :
			# on prend chaque fichier et on extrait son nom puis on créé des dossiers 
			# suivant l'option en paramètre


		# REMOVE TMP FOLDER



# Vérifie si un fichier est une archive
# @param String file path

# @return bool
# @return string caption

def is_compressed(file_path) :
	try :
		res = test_archive(file_path, verbosity=1, interactive=True)
	except PatoolError as error:
		return False #ptet un RAISE EXCEPTION
	return True



def contains_geo_files(dir_path) :
	onlyfiles = get_files_directory(dir_path)
		
	for file in onlyfiles :
		ext = file_extension(file)

		# Faire un JSON regroupant tous les formats de fichiers géographiques
		if ext in ['.shp','.shx','.dbf','.prj','.sbn','.sbx'] :
			return True
		else :
			return False

def move_all_files_directory(src_dir, dst_dir) :
	
	result = []
	if src_dir[-1] != "/" :
		src_dir = src_dir+"/"

	
	if dst_dir[-1] != "/" :
		dst_dir = dst_dir+"/"

	files = get_files_directory(src_dir)
		
	# si il n'existe pas, on le créé
	if not isdir(dst_dir) :
		os.makedirs(dst_dir)


	for file in files :
		shutil.move(src_dir+file, dst_dir+file)
		result.append(dst_dir+file)

	return result











# TEST en exécution
# extract("/srv/geodata/download/42-loire.zip","/srv/geodata/download/42-loire/", name_folder="auto")
# print(file_name("commune1.xls"))

