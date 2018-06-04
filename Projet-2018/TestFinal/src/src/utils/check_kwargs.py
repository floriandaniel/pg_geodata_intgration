#!/usr/bin/python3
from .exceptions import OptionNotFound,ValueNotMatchOption

import sys

# Permet de contrôler la véracité des kwargs
# Ici, on vérifie que la paire clé-valeur existe dans l'oracle
# défini par le développeur

def is_correct_kwargs(oracle_kwargs,kwargs_test) :
	r"""Affiche les inforamations d'un document (nom, taille, extension, ...)
	:param oracle_kwargs:
		Chemin du fichier ou du dossier
	:type kwargs_test: ``str``
        :param kwargs_test:
		Chemin du fichier ou du dossier
	:type kwargs_test: ``str``
	"""
	# params = {'inte':'marché'}
	# oracle_kwargs = {'inter':'marché','va':'mos'}
	params = kwargs_test.items()
	res = True
	
	for key,value in params:
		# print(key,value)
		# print(oracle_kwargs)

		if key not in oracle_kwargs :
			raise OptionNotFound("Option non trouvée.")
		else :
			oracle_value = oracle_kwargs.get(key)
			if type_of_value(value,oracle_value):
				res = True				
			elif value not in oracle_value :
				raise ValueNotMatchOption("ggd")
					
	return res

def allo() :
	raise ValueNotMatchOption("ggd	")
	print("Hello !!")
	return True

def foo(out=sys.stdout):
	print("hello world!")

# is_correct_kwargs({'inter':'marché'},{'inte':'marché'})

def type_of_value(value,oracle):
	types_string = ['str','int']
	res = False
	if oracle in types_string:
		if oracle == 'str' and type(value) is str:
			res = True
		elif oracle == 'int' and type(value) is int:
			res = True
		else:
			res = False
	return res