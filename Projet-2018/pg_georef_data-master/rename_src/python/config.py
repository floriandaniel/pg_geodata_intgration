# coding=utf-8
import sys

import json
from os.path import abspath, join, dirname, normpath, exists

# ________________________________ actions à effectuer au lancement


# on rend accessible les variables globales définies ici
path_of_here = abspath(__file__)
sys.path.append(path_of_here)

# assignation temporaire de valeurs temporaires
# en effet le temps du chargement de la configuration,
# ces variables sont nécessaires à l'affichage de l'exception
# car importée par la fonction utilitaire qui s'en charge
SEVERITY_LEVELS = ['error', 'warn', 'info']
LOG_LEVEL = 'info'
VISUAL_SEPARATOR_CARACTER = '.'
VISUAL_SECTION_DECORATOR_LENGTH = 32

from packages.utils.log import printex, log, log_task
from packages.utils.string import simplify
from os.path import extsep

log_task('configuration', 'start')


# ________________________________
# ________________________________ définition de fonction(s) wrapper(s)
# ________________________________


# noinspection PyGlobalUndefined
def load_general_config(filename):
    """
    Charge un fichier de configuration.
    
    :param filename: string le chemin du fichier de configuration à charger 
    """

    with open(filename, 'r') as f:

        all_is_ok = False
        j = json.load(f)
        try:

            # emplacement racine à utiliser
            global PLACE_TO_GO

            # dossier de travail
            global WORK_ROOT

            # racine du stockage des fichiers de configuration
            global CONFIG_ROOT

            # racine du stockage des documents téléchargés
            global DOWNLOAD_ROOT

            # racine du stockage des données converties
            global CONVERSION_ROOT

            # nom du dossier pour les données copiées
            global COPIED_DATA_DIRNAME

            # fichier retenant les imports yaant été effectués
            global REMEMBER_IMPORT_FILE_NAME
            global REMEMBER_IMPORT_FILE_EXT
            global REMEMBER_IMPORT_FILENAME
            global REMEMBER_IMPORT_FILE_PATH

            # niveaux de sévérité
            global SEVERITY_LEVELS

            # niveau de verbosité
            global LOG_LEVEl

            # longueur de la décoration placée à droite et à gauche des logs délimitant les tâches principales
            global VISUAL_SECTION_DECORATOR_LENGTH

            # caractère de séparation visuelle utilisé pour les exceptions dans les logs
            global VISUAL_SEPARATOR_CARACTER

            # taille minimale et maximale d'un nom court
            global SHORTNAME_MIN_LENGTH
            global SHORTNAME_MAX_LENGTH

            # groupes d'extensions
            global EXTENSION_GROUPS
            global KEY_EXTS
            global MANDATORY_EXT_GROUPS
            global OPTIONAL_EXT_GROUPS
            global INTERESTING_EXTS

            # caractéristiques des champs ajoutés
            global YEAR_NAME
            global YEAR_TYPE
            global YEAR_LENGTH
            global VERSION_NAME
            global VERSION_TYPE
            global VERSION_LENGTH
            global SRID_NAME
            global SRID_TYPE
            global SRID_LENGTH
            global GEOMETRY_NAME
            global GEOMETRY_TYPE

            # correspondance entre les types tels que représentés dans les structure python générées par fiona et les types au sein de postgresql
            global TO_POSTGRESQL_TYPE

            # paramètres de connection à la base de données
            global DB_HOST
            global DB_PORT
            global DB_NAME
            global DB_USER_NAME
            global DB_USER_PASSWORD

            # chemin du fichier dynamique de configuration "general"
            global DYNAMIC_CONFIG_GENERAL_FILE_PATH

            # chemin du fichier dynamique de configuration "data"
            global DYNAMIC_CONFIG_DATA_FILE_PATH

            # définit les modes d'import valides
            global IMPORT_MODES

            # renseigne les proxys
            global PROXIES

            # attribution des valeurs
            PLACE_TO_GO = j['place_to_go']
            WORK_ROOT = join(PLACE_TO_GO, j['work_root_name'])
            CONFIG_ROOT = join(WORK_ROOT, j['config_root_name'])
            DOWNLOAD_ROOT = join(WORK_ROOT, j['download_root_name'])
            CONVERSION_ROOT = join(WORK_ROOT, j['conversion_root_name'])
            COPIED_DATA_DIRNAME = join(j['copied_data_dirname'])
            REMEMBER_IMPORT_FILE_NAME = j['remember_import_file_name']
            REMEMBER_IMPORT_FILE_EXT = j['remember_import_file_ext']
            REMEMBER_IMPORT_FILENAME = '{}{}{}'.format(REMEMBER_IMPORT_FILE_NAME, extsep, REMEMBER_IMPORT_FILE_EXT)
            REMEMBER_IMPORT_FILE_PATH = join(CONFIG_ROOT, REMEMBER_IMPORT_FILENAME)
            SEVERITY_LEVELS = j['severity_levels']
            LOG_LEVEl = j['log_level']
            VISUAL_SECTION_DECORATOR_LENGTH = j['visual_section_decorator_length']
            VISUAL_SEPARATOR_CARACTER = j['visual_separator_caracter']
            SHORTNAME_MIN_LENGTH = j['shortname_min_length']
            SHORTNAME_MAX_LENGTH = j['shortname_max_length']
            EXTENSION_GROUPS = j['extension_groups']
            KEY_EXTS = [gg[0][0] for gg in EXTENSION_GROUPS]
            MANDATORY_EXT_GROUPS = [g for gg in EXTENSION_GROUPS for g in gg[0]]
            OPTIONAL_EXT_GROUPS = [g for gg in EXTENSION_GROUPS for g in gg[1]]
            INTERESTING_EXTS = MANDATORY_EXT_GROUPS + OPTIONAL_EXT_GROUPS
            YEAR_NAME = j['year_name']
            YEAR_TYPE = j['year_type']
            YEAR_LENGTH = j['year_length']
            VERSION_NAME = j['version_name']
            VERSION_TYPE = j['version_type']
            VERSION_LENGTH = j['version_length']
            SRID_NAME = j['srid_name']
            SRID_TYPE = j['srid_type']
            SRID_LENGTH = j['srid_length']
            GEOMETRY_NAME = j['geometry_name']
            GEOMETRY_TYPE = j['geometry_type']
            TO_POSTGRESQL_TYPE = j['types_map']
            DB_HOST = j['database_host']
            DB_PORT = j['database_port']
            DB_NAME = j['database_name']
            DB_USER_NAME = j['database_user_name']
            DB_USER_PASSWORD = j['database_user_password']
            IMPORT_MODES = j['import_modes']
            PROXIES = j['proxies']

            DYNAMIC_CONFIG_GENERAL_FILE_PATH = join(CONFIG_ROOT, CONFIG_GENERAL_FILENAME)
            DYNAMIC_CONFIG_DATA_FILE_PATH = join(CONFIG_ROOT, CONFIG_DATA_FILENAME)

        except KeyError as e:
            printex(e, 'incorrect or missing node in "{}" (bad file structure)'.format(config_file_to_load))
        except Exception as e:
            printex(e)
        else:
            all_is_ok = True
            log('general purpose configuration file "{}" correctly loaded'.format(filename))

        # problème inconnu quelconque : on crash, puisque l'on aura de toute façon besoin des configs pour focntionner correctement
        if not all_is_ok:
            log('can\'t load correctly the permanent general configuration file (see the reason above). exiting', 'error')
            exit(1)


def my_json_res_file_checker(path):
    """
    Vérifie la validité du fichier JSON contenant les liens de téléchargement et affiche des informations en conséquence.

    :param path: string le chemin du fichier de configuration data à vérifier
    """

    with open(path, 'r') as f:
        j = json.load(f)

        everything_is_fine = False
        try:
            for ressource in j['res']:

                s = ressource['params']

                # -------- vérification du mode d'import

                import_mode = ressource['import_mode']
                if import_mode not in IMPORT_MODES:
                    everything_is_fine = False
                    log('unrecognized import mode "{}"'.format(import_mode), 'warn')

                # -------- vérification du formatage du shortname

                # génération d'un avertissement pour chaque nom court incorrect
                # le nom de correction peut être donné
                # avant le 1er avertissement, les critères de validité de taille requise d'un nom court sont indiquées

                shortname_length = len(s['shortname'])

                # c'est trop court
                if shortname_length < SHORTNAME_MIN_LENGTH:
                    if not everything_is_fine:
                        give_shortname_info()
                        everything_is_fine = True
                    log('shortname "{}" is too short (length is {}, minimum is {})'.format(s['shortname'], shortname_length, SHORTNAME_MIN_LENGTH), 'warn')

                # c'est trop long
                if shortname_length > SHORTNAME_MAX_LENGTH:
                    if not everything_is_fine:
                        give_shortname_info()
                        everything_is_fine = True
                    log('shortname "{}" is too long (length is {}, maximum is {})'.format(s['shortname'], shortname_length, SHORTNAME_MAX_LENGTH), 'warn')

                # c'est mal formaté
                if s['shortname'] != simplify(s['shortname']):
                    if not everything_is_fine:
                        give_shortname_info()
                        everything_is_fine = True
                    log('shortname "{}" is poorly formated. you should consider changing it manually to something like "{}" for example'.format(s['shortname'], simplify(s['shortname'])), 'warn')

        except KeyError as e:
            printex(e, 'incorrect or missing node in "{}" (bad file structure)'.format(path))

        log('filecheck "{}" complete'.format(path))


def give_shortname_info():
    """Donne un ensemble d'informations et de chemins utiles à propos des shortnames."""
    log('in file "{}", one or several mistakes are present in shortname\'s formating, see the details below'.format(DYNAMIC_CONFIG_DATA_FILE_PATH), 'warn')
    log('the default values that defines some criteria of a shortname\'s validity can be found in config file "{}", feel free to change them'.format(DYNAMIC_CONFIG_DATA_FILE_PATH))


# ________________________________

# ________________________________
# ________________________________ configurations permanentes nécessaires au bon chargement des autres configurations
# ________________________________
# #
# /!\ ATTENTION /!\
#
# les variables de cette grande section ne doivent pas être modifiées
# elles sont nécessaires au bon fonctionnement du système de configuration
#
# ________________________________


# ################
# valeurs uniques
#
# ces valeurs :
#
# - ne sont définies qu'ici et nulle part ailleurs
#
# ################

# la visibilité de python s'arrête à ce répertoire et ses descendants
ROOT = normpath(join(dirname(path_of_here), '..'))

# racine des sources python
PYTHON_SRC_ROOT = dirname(path_of_here)

# racine des ressources
RES_ROOT = join(ROOT, 'res')

# extension imposée pour les fichiers de configuration
ALL_CONFIG_FILE_EXTENSION = '.json'

# les 2 premières variables directement ci-dessous sont, à titre d'exception, modifiables à souhait
CONFIG_GENERAL_NAME = 'general.conf'
CONFIG_DATA_NAME = 'data.conf'
CONFIG_GENERAL_FILENAME = '{}{}'.format(CONFIG_GENERAL_NAME, ALL_CONFIG_FILE_EXTENSION)
CONFIG_DATA_FILENAME = '{}{}'.format(CONFIG_DATA_NAME, ALL_CONFIG_FILE_EXTENSION)

# chemin du fichier permanent de configuration "general"
PERMANENT_CONFIG_GENERAL_FILE_PATH = join(RES_ROOT, CONFIG_GENERAL_FILENAME)

# chemin du fichier permanent de configuration "data"
PERMANENT_CONFIG_DATA_FILE_PATH = join(RES_ROOT, CONFIG_DATA_FILENAME)

# ################
# valeurs définies en double dans le fichier de configuration dynamique
#
# ces valeurs :
#
# - sont chargées à partir du fichier de configuration permanent
# - sont celles utilisées lorsque le fichier de configuration dynamique est absent
# - sont écrasées lors du chargement du fichier de configuration dynamique
#
# ################

load_general_config(PERMANENT_CONFIG_GENERAL_FILE_PATH)

# ________________________________
# ________________________________ chargement des configurations dynamiques
# ________________________________


# -------- imports
# effectués obligatoirement ici et non en haut de fichier
# en effet ces fonctions utilisent des variables définies ci-dessus

from packages.utils.path import create_dir_if_not_exists
from shutil import copyfile

# -------- configuration générale
if exists(DYNAMIC_CONFIG_GENERAL_FILE_PATH):
    load_general_config(DYNAMIC_CONFIG_GENERAL_FILE_PATH)
    log('the dynamic configuration file values overriden the permanent configuration file ones')

else:
    # création de l'arborescence
    create_dir_if_not_exists(CONFIG_ROOT)

    # on copie le permanent afin de créer le dynamique
    # (dans ce cas, pas besoin de charger le dynamique, puisqu'il est identique au permanent)
    log('generating dynamic general purpose configuration file "{}" from the permanent one "{}"'.format(DYNAMIC_CONFIG_GENERAL_FILE_PATH, PERMANENT_CONFIG_GENERAL_FILE_PATH))
    copyfile(PERMANENT_CONFIG_GENERAL_FILE_PATH, DYNAMIC_CONFIG_GENERAL_FILE_PATH)

# -------- configuration data

if exists(DYNAMIC_CONFIG_DATA_FILE_PATH):
    # vérification structurelle du dynamique
    log('checking dynamic configuration file "{}"'.format(CONFIG_DATA_FILENAME))
    my_json_res_file_checker(DYNAMIC_CONFIG_DATA_FILE_PATH)

else:

    # vérification structurelle du permanent
    log('checking permanent configuration file "{}"'.format(CONFIG_DATA_FILENAME))
    my_json_res_file_checker(PERMANENT_CONFIG_DATA_FILE_PATH)

    # création de l'arborescence
    create_dir_if_not_exists(CONFIG_ROOT)

    # on copie le permanent afin de créer le dynamique
    log('generating dynamic data configuration file "{}" from the permanent one "{}"'
        ''.format(DYNAMIC_CONFIG_DATA_FILE_PATH, PERMANENT_CONFIG_DATA_FILE_PATH))
    copyfile(PERMANENT_CONFIG_DATA_FILE_PATH, DYNAMIC_CONFIG_DATA_FILE_PATH)

log_task('configuration', 'end')
