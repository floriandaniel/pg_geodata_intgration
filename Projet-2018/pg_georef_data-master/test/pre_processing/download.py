#!/usr/bin/python3
import urllib.parse
import os
import urllib.request




def download(link, target_folder = "/srv/geodata/download/") :
	print("params--> {}  {}".format(link,target_folder))
	
	# on récupère le nom du fichier
	a = urllib.parse.urlparse(link)
	name = os.path.basename(a.path)
		
	# on récupère le nom du site et son domaine
	# pour construire le nom du dossier
	netloc = urllib.parse.urlsplit(link).netloc
	
	# on découpe le nom du site pour enlever "www"
	split_domain_name = netloc.split(".")

	# si l'url commence par "www" on le supprimer
	# sinon on garde le nom du site comme tel 
	if netloc.startswith("www") :
		netloc = split_domain_name[1:]
	else :
		netloc = netloc

	# s'il y a des sous domaines comme "madoc.univ-nantes.fr" on le reconstuit
	inter_folder_name = '.'.join(netloc)+"/"


	target_directory = target_folder+inter_folder_name

	if not os.path.isdir(target_directory) :
		# INFO - Un folder est créé
		os.makedirs(target_directory)


	proxy = urllib.request.ProxyHandler({"http": "http://snancache01.ifsttar.fr:3128"})
	proxies = urllib.request.getproxies()
	opener = urllib.request.build_opener(proxy)	
	urllib.request.install_opener(opener)



	if not os.path.isfile(target_directory+name) :
		file_retrieved,_ = urllib.request.urlretrieve(link,target_directory+name)
	elif confirm_download_again(target_directory+name) :
		file_retrieved,_ = urllib.request.urlretrieve(link,target_directory+name)


	res = list()
	res.append(target_directory+name)
	return res



def confirm_download_again(file_path_file) :
	saisie_correct = False
	
	while saisie_correct != True :

		# WARN de Rémy
		print("Il semble que le fichier existe déjà dans le dossier")
		response = input("Proceed (y/n) ?")

		if response == "y" :
			saisie_correct = True
			return True
		elif response == "n" :
			saisie_correct = True
			return False


def is_file(file_path) :
	if os.path.isfile(file_path) :
		return True
	else : 
		raise FileNotFoundError("File not found et ouais !!!")



# print(download("https://www.insee.fr/fr/statistiques/fichier/2388572/filo-revenu-pauvrete-menage-2013.zip","/home/florian-stage/Projet-2018/pg_georef_data-master/viewing(test)/test/"))





















# exemples de liens à télécharger via URL
# https://www.insee.fr/fr/statistiques/fichier/2388572/filo-revenu-pauvrete-menage-2013.zip
# http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Themes/Energies_et_climat/Les_differentes_energies/Electricite/enquete_livraison/2014/livraison-electricite-2014-communes-b.xls
# https://www.insee.fr/fr/statistiques/fichier/2388572/filo-revenu-pauvrete-menage-2013.zip

