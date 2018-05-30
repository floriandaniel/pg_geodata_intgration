#!/usr/bin/python3

from ..mes_methodes import une_methode
from ..exceptions import exceptions

def allo() :
	str = ""
	if une_methode.main() == True :
		str += "main() de méthode est VRAI\n"
	else :
		str += "Y'a un truc de faux, lààà\n"	
	if exceptions.une_exception == 10 :
		str += "une_exception est VRAI\n"
	else :
		str += "Y'a un deuxième de faux lààààà\n"
	
	return str


