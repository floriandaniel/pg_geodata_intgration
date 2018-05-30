#!/usr/bin/python3

from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError
import urllib.parse
from os import listdir
from os.path import join,isfile,dirname,abspath,isdir
import urllib.request
from .fileInfo import file_extension, file_name
from ..utils.folder import get_files_directory,add_slash2path
import os
import shutil

__all__ = ['extract']

def extract(file_path, target_folder = "/srv/geodata/download/",**kwargs) :
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

	"""

	print("params--> {}  {}".format(file_path,target_folder))

	target_folder = add_slash2path(target_folder)
	name = file_name(file_path)
	filename, file_extension = os.path.splitext(name)

	
	if is_compressed(file_path) :
		print("Est compressée")

		# le nom est trompeur, on pratique ici un déplacement de fichier
		# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

		if not isdir(target_folder) :
			os.makedirs(target_folder)

		
		if contains_geo_files(target_folder):			
			path_from_filepath = dirname(abspath(file_path))
			print(path_from_filepath)
			outdir_folder = ''.join([target_folder,filename])			
			
			# move_all_files_directory(local_tmp_folder,target_folder+filename)
		else:
			if 'name_folder' in kwargs :
				if kwargs.get("name_folder") == "auto" :

					outdir_folder = ''.join([target_folder,filename])	
					print(name, filename, file_extension)


				elif kwargs.get("name_folder") == "manual" :
					outdir_folder = target_folder
			else : 
				print("WARN")

		extract_archive(file_path, verbosity=0,outdir=outdir_folder, interactive=False)
		print("Archive extraite vers \"{}\"".format(outdir_folder))
		# else :
			# on prend chaque fichier et on extrait son nom puis on créé des dossiers 
			# suivant l'option en paramètre
	else:
		print("Le fichier n'est pas compressé, override it !")

		# REMOVE TMP FOLDER



# Vérifie si un fichier est une archive
# @param String file path

# @return bool
# @return string caption

def is_compressed(file_path) :
	try :
		res = test_archive(file_path, verbosity=-1, interactive=False)
	except PatoolError :
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
	
	if src_dir[-1] != "/" :
		src_dir = src_dir+"/"

	
	if dst_dir[-1] != "/" :
		dst_dir = dst_dir+"/"

	files = get_files_directory(src_dir)
		
	# si il n'existe pas, on le créé
	if not isdir(dst_dir) :
		os.makedirs(dst_dir)
	else :
		# WARN ou INFO
		print("WARN")

	for file in files :
		os.rename(src_dir+file, dst_dir+file)












# TEST en exécution
# extract("/srv/geodata/download/42-loire.zip","/srv/geodata/download/42-loire/", name_folder="auto")
# print(file_name("commune1.xls"))

