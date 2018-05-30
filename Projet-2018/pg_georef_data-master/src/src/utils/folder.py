#!/usr/bin/python3
from .exceptions import OptionNotFound,FolderAlreadyExists,ValueNotMatchOption
from .check_kwargs import is_correct_kwargs
from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError
from os import listdir
from os.path import join,isfile,dirname,abspath,isdir
import os


def create_dir(dir_path,**kwargs) :
	
	if 'if_exists' in kwargs :
		
		option_exists = kwargs.get('if_exists')

		if option_exists not in ({"continue","error"}) :
			raise ValueNotMatchOption("The value of the option is not correct.")



		# si il n'existe pas, on le créé
		if not isdir(dir_path) :
			os.makedirs(dir_path)
		else :
			if option_exists == "continue" :
				print("Warning ! Folder is not created, because it already exists.")
			elif option_exists == "error" :
				raise FolderAlreadyExists("The folder already exists.")
	else :
		raise OptionNotFound("Sorry, the key option does not exist.")


def get_files_directory(dir_path,**kwargs) :
	onlyfiles = []
	if is_correct_kwargs({'path':['yes','no']},kwargs) :

		for f in listdir(dir_path) :
			file_path = join(dir_path,f)

			if isfile(join(dir_path,f)) :
				if kwargs.get("path") == "yes" :
					onlyfiles.append(join(dir_path,f))
				else :
					onlyfiles.append(f)
		print(onlyfiles)
	
	return onlyfiles

def move_file(src_file_path,dst_file_path) :
	os.rename(src_dir+file, dst_dir+file)


def add_slash2path(string):
    if not string.endswith("/"):
        string = string+"/"

    return string

