#!/usr/bin/python3
from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError

# Vérifie si un fichier est une archive
# @param String file path

# @return bool
# @return string caption

def is_compressed(file_path) :
	try :
		res = test_archive("fichiers shape.zip", verbosity=-1, interactive=False)
	except PatoolError :
		return False,"the file is not an archive or not correctly defined"
	return True,"the file is an archive"



# -------TESTS BASIQUES-------
res,string = is_compressed("fichiers shape.zip")
print(res)
print(string)
