from os.path import join

from config import EXTENSION_GROUPS, KEY_EXTS, COPIED_DATA_DIRNAME
from packages.utils.log import log
from packages.utils.path import search_with_criteria, path_splitter
from packages.utils.string import simplify, get_website_name_from_url


def get_mandatory_ext_list_by_key(key_ext):
    """
    Récupère la liste des extensions primordiales pour un groupe d'extensions.

    :param key_ext: string l'extension "clé"
    """
    return [e for ll in EXTENSION_GROUPS for l in ll for e in l if l[0] == key_ext]


def is_a_key_ext(candidate_ext):
    """
    Détermine si une extension est clé d'un groupe.
    
    :param candidate_ext: string l'extension à tester
    """
    return candidate_ext in KEY_EXTS


def find_key_file_from_params(params, step_dir):
    """Trouve le fichier clé à partir des paramètres d'une donnée."""

    key_file = ''
    in_d = get_path_from_params(params, step_dir)
    data_name = params['data_name']

    def is_the_main_data_file_we_are_looking_for(vparams):
        """Définit si un fichier est clé pour ce traitement."""
        dd, nn, ee = path_splitter(vparams['path'])
        return data_name.lower() == nn.lower() and ee.lower() in KEY_EXTS

    results = search_with_criteria(in_d, is_the_main_data_file_we_are_looking_for, search_depth=-1)

    match_count = len(results)

    if match_count == 1:
        key_file = results[0]

    elif match_count > 1:

        # priorité déterminée par la précédence de l'extension clé dans la liste KEY_EXTS

        candidates = []

        for file_idx, file in enumerate(results):
            for ext_idx, ext in enumerate(KEY_EXTS):
                if file.lower().endswith(ext):
                    candidates.append([file_idx, ext_idx])
        candidates.sort(key=lambda e: e[1])

        key_file = results[candidates[0][0]]

    return key_file


def get_path_from_params(params, step_directory):
    """
    Donne le chemin du dossier "feuille" dans lequel travailler pour une donnée.
    
    :param params: dict les paramètres tirés de la configuration
    :param step_directory: string le chemin absolu du dossier correspondant à la racine de la tâche appropriée
    :return: string le chemin complet du répertoire approprié (qu'il existe ou non !)
    """

    answer = ''
    uri = params['uri']
    about = simplify(params['shortname'])

    if uri.startswith('htt'):
        site = get_website_name_from_url(uri)
        answer = join(step_directory, site, about)

    elif uri.startswith('file:///'):
        answer = join(step_directory, COPIED_DATA_DIRNAME, about)

    else:
        log('can\'t find associated path from params because of unrecognized uri "{}"'.format(uri), 'warn')

    return answer
