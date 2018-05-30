import json
from os import rename
from os.path import join, exists, isfile, extsep
from shutil import copyfile, copytree
from urllib.error import URLError
from urllib.parse import urlparse

from patoolib import get_archive_format
from patoolib.util import PatoolError
from pip._vendor.requests import get

from config import DOWNLOAD_ROOT, DYNAMIC_CONFIG_DATA_FILE_PATH, PROXIES, WORK_ROOT
from packages.data_processing.extensions import get_path_from_params
from packages.utils.log import log, log_task, printex
from packages.utils.path import create_dir_if_not_exists, remove_empty_dirs_in_dir, path_splitter
from packages.utils.string import simplify, get_website_name_from_url


# noinspection PyBroadException
def retrieve_all():
    """Rapatrie l'ensemble des ressources."""

    taskname = 'retrieving'
    log_task(taskname, 'start')

    some_action_performed = False
    no_exception = True

    with open(DYNAMIC_CONFIG_DATA_FILE_PATH, 'r') as f:

        j = json.load(f)
        try:
            for ressource in j['res']:
                params = ressource['params']
                print("PARAMS "+str(params))
                uri = params['uri']

                # chaque uri est traitée de façon adéquate
                print("1111111111111111")
                if uri.startswith('htt'):
                    if get_data_from_url(params):
                        some_action_performed = True
                    
                elif uri.startswith('file:///'):
                    if get_data_from_filepath(params):
                        some_action_performed = True
                    print("22222222222222")
                else:
                    log('unimplemented processing for uri "{}"'.format(uri), 'warn')

        except KeyError as e:
            no_exception = False
            printex(e, 'incorrect or missing node in "{}" (bad file structure)'.format(DYNAMIC_CONFIG_DATA_FILE_PATH))
        except Exception as e:
            no_exception = False
            printex(e)

        if no_exception:
            if some_action_performed:
                log('all data downloaded successfully')
            else:
                log('nothing were done, because all data were already retrieved')
        else:
            log('sorry, some data could not be downloaded', 'warn')

        if some_action_performed:
            # nettoyage (suppression récursive) des dossiers vides potentiellement présents dans le répertoire de récupération des données
            log('removed potentially useless created directories in "{}"'.format(WORK_ROOT))
            remove_empty_dirs_in_dir(DOWNLOAD_ROOT)

        log_task(taskname, 'end')


def get_data_from_url(params):
    """Récupère une ressource web distante."""

    # récupération du chemin dans lequel télécharger la ressource
    save_to = get_path_from_params(params, DOWNLOAD_ROOT)

    # pour journalisation
    about = simplify(params['shortname'])
    done_something = False

    # si un dossier de ce nom existe déjà, on passe
    if exists(save_to):
        log('ignored "{}" because data has already been downloaded (directory "{}" exists)'.format(about, save_to))

    else:

        # déclarations
        uri = params['uri']
        site = get_website_name_from_url(uri)

        # création de la destination
        create_dir_if_not_exists(save_to)
        save_as = join(save_to, about)

        # téléchargement de la ressource
        log('fetching data from the "{}" website about "{}"'.format(site.upper(), about))

        # le try/catch interne à la boucle permet de passer outre les URLS invalides et de continuer
        try:
            # @deprecated ne permet pas de gérer les certificats SSL
            # urlretrieve(uri, save_as)

            with open(save_as, 'wb') as output_file:
                response = get(uri, verify=False, proxies=PROXIES)
                output_file.write(response.content)

        # gestion des exceptions
        except URLError as e:
            printex(e, 'problem during "{}" ressource download'.format(uri))
        except Exception as e:
            printex(e)  # problème inconnu quelconque

        # aucun problème n'est survenu
        else:

            done_something = True
            # renommage : ajout de l'extension au nom de l'archive téléchargée
            try:
                extension = get_archive_format(save_as)[0]
                file_with_extension = '{}{}{}'.format(save_as, extsep, extension)
                rename(save_as, file_with_extension)
                print("PRINT DATA_NAME   :  "+params['data_name'])

            except PatoolError as e:
                printex(e, 'the ressource located at "{}" is probably not an archive, download may have failed somehow. just copying it'.format(uri))

                # ressources distantes fichiers solo
                filename = '{}{}{}'.format(params['data_name'], extsep, params['extension'])
                filepath = join(save_to, filename)
                rename(save_as, filepath)

            except Exception as e:
                printex(e)

            log('successfully downloaded data about "{}"'.format(about))

    return done_something


def get_data_from_filepath(params):
    """
    Récupère une ressource locale en la copiant dans le dossier de téléchargement spécifié.
    
    urlretrieve() permettrait également de copier des fichiers en local
    Cependant il a été préféré de garder une meilleure maîtrise (indépendance du traitement en fonction de l'URI).
    """

    # récupération du chemin dans lequel copier la ressource
    save_to = get_path_from_params(params, DOWNLOAD_ROOT)

    # pour journalisation
    about = simplify(params['shortname'])

    # si un dossier de ce nom existe déjà, on passe
    done_something = False
    if exists(save_to):
        log('ignored "{}" because data has already been copied ("{}" exists)'.format(about, save_to))

    else:

        done_something = True

        # dossier final de destination
        create_dir_if_not_exists(save_to)

        # récupération du chemin de la ressource
        file_or_dir = urlparse(params['uri'])
        source_path = file_or_dir.path

        log('copying data about "{}" from "{}" to "{}"'.format(about, source_path, save_to))
        print("C'EST MOIIIIII")

        # c'est un unique fichier de données ou une archive
        if isfile(source_path):
            dirpath, name, extension = path_splitter(source_path)
            filename = '{}{}{}'.format(simplify(params['data_name']), extsep, extension)
            print("FILENAME = "+filename)
            save_as = join(save_to, filename)
            copyfile(source_path, save_as)

        # c'est un dossier non compressé
        else:
            copytree(source_path, save_to)

    return done_something
