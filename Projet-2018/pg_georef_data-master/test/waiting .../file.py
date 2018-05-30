#!/usr/bin/python3
from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError
from os import listdir
from os.path import join,isfile,dirname,abspath,isdir
import os


def create_dir(dir_path) :
	# si il n'existe pas, on le créé
	if not isdir(dst_dir) :
		os.makedirs(dst_dir)
	else :
	# WARN ou INFO
		print("WARN")



def get_files_directory(dir_path) :
	# # onlyfiles = [f for f in listdir(dir_path) if path.isfile(str.join(dir_path, f))]
	# onlyfiles = []
	# for f in listdir(dir_path) :
	# 	print(str(f))
	# 	file_path = join(dir_path,f)
	# 	# print("OK ==>  "+res)

	# 	if isfile(join(dir_path,f)) :
	# 		onlyfiles.append(f)

	# print(onlyfiles)
	# # print(onlyfiles)
	onlyfiles = [f for f in listdir(dir_path) if path.isfile(join(dir_path, f))]
	return onlyfiles


def move_file(src_file_path,dst_file_path) :
	os.rename(src_dir+file, dst_dir+file)


def aire_rectangle2(**kwargs):  # les arguments passes en parametre sont paquetes dans kwargs qui se comporte comme un dictionnaire
    if len(kwargs) == 2:

    	if "number" in kwargs.keys():
    		print("number".get)
        # for key, value in kwargs.items():
        #     result *=value
        # return result
    else:
        print('Merci de stipuler deux parametres')

print(aire_rectangle2(number="several"))
