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
	onlyfiles = [f for f in listdir(dir_path) if path.isfile(join(dir_path, f))]
	return onlyfiles


def move_file(src_file_path,dst_file_path) :
	os.rename(src_dir+file, dst_dir+file)

