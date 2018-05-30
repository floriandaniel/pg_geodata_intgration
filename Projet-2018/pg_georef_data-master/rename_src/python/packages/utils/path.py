# coding=utf-8
from os import makedirs, listdir, rmdir
from os.path import exists, isdir, join, sep, basename, abspath, dirname, extsep
from re import sub

from packages.utils.log import log, printex


def create_dir_if_not_exists(path):
    """
    Crée un répertoire si celui-ci est inexistant.
    
    :param path: string le chemin absolu du dossier à créer
    """
    if not exists(path):
        try:
            makedirs(path)
        except PermissionError as e:
            path_top_level = sub(r"^({0}?[^{0}]*){0}.*$".format(sep), r"\1", path)
            printex(e, 'cannot create the directory "{}". check rights on "{}"'.format(path, path_top_level))
            exit(1)
        except Exception as e:
            printex(e, 'while attempting to create directory "{}".'.format(path))
            log('some directory could not be created. crashing.', 'error')
            exit(1)
        else:
            log('directory "{}" created'.format(path))


def remove_empty_dirs_in_dir(path):
    """
    Supprime récursivement les répertoires vides contenus dans le répertoires passé en paramètre.
    
    Codé à partir du lien suivant, mais opté pour une solution utilisant une fonction interne.
    
    https://www.jacobtomlinson.co.uk/2014/02/16/python-script-recursively-remove-empty-folders-directories/
    :param path: string le chemin absolu du dossier dans lequel effectuer le nettoyage 
    """
    # valable uniquement pour un dossier
    if not isdir(path):
        return

    def remove_empty(path_of_dir):
        """Fonction interne afin de pouvoir conserver le dossier parent."""

        # partie récursion
        files = listdir(path_of_dir)
        if len(files):
            for file in files:
                child_path = join(path_of_dir, file)
                if isdir(child_path):
                    remove_empty(child_path)

        # partie suppression
        files = listdir(path_of_dir)  # actualisation de la liste des fichiers
        if len(files) == 0:
            rmdir(path_of_dir)

    # protection du dossier racine à partir duquel on supprime via ce niveau d'imbrication
    fichiers = listdir(path)
    for f in fichiers:
        chemin_fichier_enfant = join(path, f)
        remove_empty(chemin_fichier_enfant)


def search_with_criteria(path_to_search_in, validator, validator_params=None, search_depth=0):
    """
    Recherche les fichiers du dossier spécifié qui matchent un critère.
    
    :param path_to_search_in: string le chemin absolu dans lequel rechercher
    :param search_depth: int la profondeur de recherche (valeur négative pour ne pas stopper la récursivité et tout explorer jusqu'aux répertoires feuilles)
    :param validator: func une fonction qui renvoie un booléen pour un fichier donné
    :param validator_params: dict paramètres (autres que le chemin) à relayer à la fonction de validation
    :return: la liste des chemins complets des fichiers trouvés
    """

    if validator_params is None:
        validator_params = {}

    def swc(p, v, vp, d):
        """Fonction interne de recherche."""

        # -------- déclarations
        r = []
        vp_with_path = dict(vp)

        # -------- recherche
        for f in listdir(p):

            # on travaille toujours avec le chemin complet
            fullpath = join(p, f)

            # ajout du chemin aux paramètres
            vp_with_path['path'] = fullpath

            # un de trouvé !
            if v(vp_with_path):
                r.append(fullpath)

            # on descend dans les sous-dossiers
            if isdir(fullpath):
                if d < 0:
                    r += swc(fullpath, v, vp, -1)
                else:
                    r += swc(fullpath, v, vp, d-1)

        # -------- résultat
        return r

    # on imbrique d'un niveau avec swc afin de vérifier que le chemin passé en paramètre correpond à un répertoire

    results = []

    if not isdir(path_to_search_in):
        return results

    results = swc(path_to_search_in, validator, validator_params, search_depth)

    return results


def path_splitter(path):
    """
    Sépare un chemin en trois composantes.
    
    :param path: le chemin à traiter
    :return: dirpath, name, extension
    """

    dirpath = dirname(abspath(path))
    filename = basename(path)
    result = filename.rsplit(extsep, 1)
    name, ext = '', ''

    if len(result) == 2:
        name, ext = result
    else:
        name = result[0]

    return dirpath, name, ext
