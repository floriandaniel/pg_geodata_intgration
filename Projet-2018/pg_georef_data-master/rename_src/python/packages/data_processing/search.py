from config import DOWNLOAD_ROOT, INTERESTING_EXTS, MANDATORY_EXT_GROUPS
from packages.data_processing.extensions import get_path_from_params
from packages.database.fill import to_database, xls_handler
from packages.utils.log import log
from packages.utils.path import path_splitter, search_with_criteria
from packages.utils.string import simplify


def process_group(files, ressource, conn):
    """
    Envoie à traiter une ressource donnée.
    
    :param files: les fichiers à utiliser pour la conversion
    :param ressource: le mode d'import et ses paramètres
    :param conn: la connexion à la base de données
    :return: bool True si le traitement s'est déroulée sans encombre, False sinon
    """

    # définitions facilitatrices
    params = ressource['params']

    # construction de la liste des extensions des fichiers possédés
    exts = []
    for f in files:
        dirpath, name, ext = path_splitter(f)
        exts.append(ext)

    # journalisation
    okko, handled, time_to_break = False, False, False

    # on recherche la correspondance entre
    # les fichiers à disposition (leurs extensions)
    # et les regroupement associés à un traitement

    for g in MANDATORY_EXT_GROUPS:
        for _, e in enumerate(exts):

            # les différents traitements sont précisés ci-dessous
            # il est possible de les distinguer par types (ex: shp, xls) puis par organisation (ex: insee, ign)

            if e.lower() == g:

                # -------- formats gérés par fiona
                if g in ['shp', 'mif']:

                    handled = True

                    # c'est ici que l'on récupère des informations bonus
                    # ces informations sont à intégrer dans le dictionnaire des paramètres
                    # elles pourront alors faire l'objet de traitement spécifiques, dans les fonctions de plus bas niveau

                    # interesting_files = []
                    # for f in files:
                    #     dirpath, name, ext = path_splitter(f)
                    #     if ext.lower() in OPTIONAL_EXT_GROUPS:
                    #         interesting_files.append(f)

                    # la donnée est reconnue comme "à importer"
                    okko = to_database(ressource, conn)
                    time_to_break = True

                # -------- autres formats géographiques, que l'on ramène à des formats gérés par fiona

                # elif g == 'remplacer_par_l_extension_a_gerer':

                    # exemple de code pour facilement supporter d'autres formats géographiques non gérés par fiona
                    # la fonction remplacer_par_l_extension_a_gerer2shp() aurait une documentation comme présentée ci-dessous
                    # """
                    # Effectue la conversion d'un fichier d'un format spécifique non supporté par fiona, en fichier shape et renvoie la ressource à importer.
                    #
                    # :param ressource: dict l'import à effectuer
                    # :return: la ressource modifiée (uri)     et     True si tout est OK False sinon
                    # :rtype: dict, bool
                    # """
                    # de même, elle peut procéder comme suit pour le fichier intermédiaire
                    # converted_file_dir = get_path_from_params(params, CONVERSION_ROOT)
                    # create_dir_if_not_exists(converted_file_dir)
                    # converted_file_name = '{}{}{}'.format(simplify(params['shortname']), extsep, 'shp')
                    # converted_file_path = join(converted_file_dir, converted_file_name)

                    # enfin, ici, laisser uniquement ces trois lignes
                    # ressource, okko = remplacer_par_l_extension_a_gerer2shp(ressource)
                    # okko = to_database(ressource, conn)
                    # time_to_break = True

                # -------- données non géographiques

                elif g in ['xls', 'xlsx']:

                    handled = True
                    okko = xls_handler(ressource, conn)
                    time_to_break = True

            if time_to_break:
                break
        if time_to_break:
            break

    if not handled:
        log('sorry, the processing for the file format group {} is not implemented yet'.format(exts), 'warn')
    else:
        if not okko:
            log('sorry, processing failed for this atomic data', 'error')
        else:
            log('successfully processed this atomic data')

    return okko


def is_data_file(params):
    """
    Définit si un fichier est constitutif d'une donnée.
    
    :param params: dict les paramètres d'import
    :return: True si le fichier est un fichier de données, False sinon
    """

    data_name = params['data_name'].lower()
    dirpath, name, ext = path_splitter(params['path'])
    ok_name = name.lower() == data_name if data_name != '' else True
    ok_ext = ext.lower() in INTERESTING_EXTS

    return ok_name and ok_ext


def search_for_files_to_process(a_res):
    """
    Construit la liste des données à traiter.

    :param a_res: dict la configuration associée à la donnée atomique
    :return: une liste de liste de chemins complets de fichiers se rapportant à la même donnée atomique et les paramètres (complétés) associés
    """

    # -------- déclarations préliminaires

    results = []
    params = a_res['params']
    shortname = simplify(params['shortname'])
    path_to_search_in = get_path_from_params(params, DOWNLOAD_ROOT)

    # traitement de la présence/abscence du data_name
    data_name = params['data_name'] if 'data_name' in params else ''
    validator_params = {'data_name': data_name}

    # -------- journalisation

    info_msg = '{}'.format(shortname) if data_name == '' else '{} / {}'.format(shortname, data_name)
    log('exploring data about "{}"'.format(info_msg))

    # -------- recherche d'une donnée atomique

    data_files = search_with_criteria(path_to_search_in, is_data_file, validator_params=validator_params, search_depth=-1)
    data_files_names = []

    for df in data_files:
        dirpath, name, ext = path_splitter(df)
        data_files_names.append(name)

    list_of_unique_names = list(set(data_files_names))
    number_of_atomic_data = len(list_of_unique_names)
    we_caught_one_atomic_data = number_of_atomic_data == 1

    # -------- une/l' unique donnée atomique a été trouvée

    if we_caught_one_atomic_data:
        if data_name == '':
            detected_data_name = list_of_unique_names[0]
            log('auto-detect found an atomic data called "{}"'.format(detected_data_name))
            params['data_name'] = detected_data_name
        results = data_files  # results = data_files[:]        serait plus lent, car recopierai au lieu d'agir par référence
    else:
        if data_name == '':
            if number_of_atomic_data == 0:
                log('sorry, auto-detect did not found any data', 'warn')
            else:
                log('sorry, auto-detect will need you to define manually the data name because several atomic data have been found', 'warn')
        else:
            log('sorry, there is no matching data', 'warn')

    return results, params
