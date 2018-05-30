#!/usr/bin/python3
from exceptions import OptionNotFound,ValueNotMatchOption

# Permet de contrôler la véracité des kwargs
# Ici, on vérifie que la paire clé-valeur existe dans l'oracle
# défini par le développeur

def is_correct_kwargs(oracle_kwargs,kwargs_test) :

	# params = {'inte':'marché'}
	# oracle_kwargs = {'inter':'marché','va':'mos'}
	params = kwargs_test.items()
	res = True
	
	for key,value in params :
		print("hello")
		# print(key,value)
		# print(oracle_kwargs)
		if key not in oracle_kwargs :
			raise OptionNotFound("Option non trouvée.")
			# print("je suis dans le ifff")
			# raise OptionNotFound("alo")
			print("oui")
		else : 
			# print(oracle_kwargs.get(key))
			if value not in oracle_kwargs.get(key) :
				raise ValueNotMatchOption("ggd")
			
	print(res)		
	return res

def allo() :
	raise ValueNotMatchOption("ggd	")
	print("Hello !!")
	return True

# is_correct_kwargs({'inter':'marché'},{'inte':'marché'})