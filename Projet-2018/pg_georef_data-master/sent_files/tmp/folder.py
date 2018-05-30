#!/usr/bin/python3
from exceptions import OptionNotFound,FolderAlreadyExists,ValueNotMatchOption
from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError
from os import listdir
from os.path import join,isfile,dirname,abspath,isdir
import os


def create_dir(dir_path,**kwargs) :
	
	if 'if_exists' in kwargs :
		print(True)
		
		option_exists = kwargs.get('if_exists')

		if option_exists not in ({"continue","error"}) :
			raise ValueNotMatchOption("The value of the option is not correct.")



		# si il n'existe pas, on le créé
		if not isdir(dir_path) :
			os.makedirs(dir_path)
		else :
			print(option_exists)
			if option_exists == "continue" :
				print("Warning ! Folder is not created, because it already exists.")
			elif option_exists == "error" :
				raise FolderAlreadyExists("The folder already exists.")
	else :
		raise OptionNotFound("Sorry, the key option does not exist.")



def get_files_directory(dir_path) :
	onlyfiles = [f for f in listdir(dir_path) if path.isfile(join(dir_path, f))]
	return onlyfiles


def move_file(src_file_path,dst_file_path) :
	os.rename(src_dir+file, dst_dir+file)


