#!/usr/bin/python3

from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError
import urllib.parse
from os import listdir
from os.path import join,isfile,dirname,abspath,isdir
import urllib.request
from pre_processing.fileInfo import file_extension, file_name
import os
import shutil


def extract(file_path, target_folder = "/srv/geodata/download/",**kwargs) :
	print("params--> {}  {}".format(file_path,target_folder))

	if 'name_folder' in kwargs :
		if kwargs.get("name_folder") == "auto" :
			name = file_name(file_path)
			filename, file_extension = os.path.splitext(name)

		elif kwargs.get("name_folder") == "manual" :
			filename = ""

		else : 
			print("WARN")

	
	if is_compressed(file_path) :
		print("Est compressée")
		mypath = "/srv/geodata/"

		# le nom est trompeur, on pratique ici un déplacement de fichier
		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

		path_folder = dirname(abspath(file_path))
		local_tmp_folder = path_folder+"/tmp/"

		if not isdir(local_tmp_folder) :
			os.makedirs(local_tmp_folder)

		
		extract_archive(file_path, verbosity=1,outdir=local_tmp_folder, interactive=False)
		if contains_geo_files(local_tmp_folder) :			
			path_from_filepath = dirname(abspath(file_path))
			
			move_all_files_directory(local_tmp_folder,target_folder+filename)


		# else :
			# on prend chaque fichier et on extrait son nom puis on créé des dossiers 
			# suivant l'option en paramètre

		shutil.rmtree(local_tmp_folder)

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



def get_files_directory(dir_path) :
	onlyfiles = []
	for f in listdir(dir_path) :
		file_path = join(dir_path,f)

		if isfile(join(dir_path,f)) :
			onlyfiles.append(f)

	print(onlyfiles)
	return onlyfiles


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

