#!/usr/bin/python3
import urllib.parse
import urllib.error
import os
import urllib.request
import shutil
from ..utils.folder import add_slash2path
from urllib import parse,error,request
__all__ = ['download']


def download(link, target_folder="/srv/geodata/download/"):
    """
    Télécharge un fichier via son URL, dans un dossier cible

    :param link: lien URL où se situe le fichier que l'on souhaite télécharger fjf fbfbf  dffj
    :type link: ``str``
    :param target_folder: dossier cible où va être placé le fichier téléchargé

        * *par défault* -- ``/srv/geodata/download/``
    :type target_folder: ``str``

    :key nom_key: description
    :return: une liste des chemins de fichiers téléchargés
    :rtype: ``list``

    """
    try:
        # On récupère le nom du site et son domaine,
        # pour construire le nom du dossier
        netloc = urllib.parse.urlsplit(link).netloc

        # on découpe le nom du site pour enlever "www"
        split_domain_name = netloc.split(".")

        # Si l'url commence par "www" on le supprime,
        # sinon on garde le nom du site comme tel
        if netloc.startswith("www"):
            netloc = split_domain_name[1:]
        else:
            netloc = netloc

        print("netloc = "+str(netloc))
        # s'il y a des sous domaines comme "madoc.univ-nantes.fr" on le reconstuit

        
        
        target_folder = add_slash2path(target_folder)
        # on récupère le nom du fichier
        a = urllib.parse.urlparse(link)
        name = os.path.basename(a.path)
        inter_folder_name = '.'.join(netloc)
        inter_folder_name = add_slash2path(inter_folder_name)
        target_directory = target_folder+inter_folder_name

        print("inter_folder_name = "+inter_folder_name)
        print(target_directory)
        
        # on checke le proxy, on récupère ses infos 
        proxy = urllib.request.ProxyHandler({
            "http": "http://snancache01.ifsttar.fr:3128"})
        proxies = urllib.request.getproxies()
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)

        if not os.path.isfile(target_directory+name):
            file_retrieved, _ = urllib.request.urlretrieve(link, name)
        elif confirm_download_again(target_directory+name):
            file_retrieved, _ = urllib.request.urlretrieve(link, name)
        else:
            return

        if not os.path.isdir(target_directory):
            # INFO - Un folder est créé
            print(os.makedirs(target_directory))

        shutil.move(name,target_directory+name)
        res = list()
        res.append(target_directory+name)
        return res

    except error.HTTPError as http:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', http.code)

    except error.URLError as url:
        print("The URL link is not correct")
        print("Reason: ",url.reason)



def confirm_download_again(file_path_file):

    saisie_correct = False

    while saisie_correct is not True:

        # WARN de Rémy
        print("Il semble que le fichier existe déjà dans le dossier")
        response = input("Proceed (y/n) ?")

        if response == "y":
            saisie_correct = True
            return True
        elif response == "n":
            saisie_correct = True
            return False

# exemples de liens à télécharger via URL
# https://www.insee.fr/fr/statistiques/fichier/2388572/filo-revenu-pauvrete-menage-2013.zip
# http://www.statistiques.developpement-durable.gouv.fr/fileadmin/documents/Themes/Energies_et_climat/Les_differentes_energies/Electricite/enquete_livraison/2014/livraison-electricite-2014-communes-b.xls
# https://www.insee.fr/fr/statistiques/fichier/2388572/filo-revenu-pauvrete-menage-2013.zip
