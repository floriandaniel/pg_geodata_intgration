#!/usr/bin/python3
from hurry.filesize import size, alternative
import os
import magic
import mimetypes
import pandas as pd

# -------INFO FILE-------

def file_info(file_path) :
#check if it's an excel file
#make a config file with spreadsheets formats
#là ils sont codés en dur

	try :
		if real_file(file_path) :
			
			name = file_name(file_path)
			extension = file_extension(file_path)
			size_bytes,size_unit = file_size(file_path)
				

			print("------"+file_path+"------")
			print("name : {}".format(name))
			print("type : {}".format(extension))
			print("size : {} ({} bytes)".format(size_unit,size_bytes))
			
			if file_path.endswith((".xls",".xlsx")) :
				sheets_count = file_count_sheets(file_path)		
				print("number of sheets : {}".format(sheets_count))
		
	except FileNotFoundError as error :
		print(error,'File not found.')

	except Exception as e:
		print(e,'Unknown error.')





def real_file(file_path) :
	if os.path.isfile(file_path) :
		return True
	else : 
		raise FileNotFoundError("File not found et ouais !!!")


def file_name(file_path) :
	name = os.path.basename(file_path)

	return name


def file_extension(file_path) :
	_, file_extension = os.path.splitext(file_path)
	return file_extension


def file_size(file_path) :
	sizeBytes = os.path.getsize(file_path)
	readingSize = size(sizeBytes, system=alternative)

	return sizeBytes,readingSize


def file_count_sheets(file_path) :
	xl = pd.ExcelFile(file_path)
	countSheets = len(xl.sheet_names)

	return countSheets


def path_folder(file_path) :
	path_folder = dirname(abspath(file_path))

	return path_folder













# Exemples d'utilisation de la méthode file_info

# file_info("memory.png")
# file_info("file1.csv")
# file_info("fileInfo.py")
# file_info("fileOut.csv")
# file_info("memory.png")
# file_info("memorydq.png")
