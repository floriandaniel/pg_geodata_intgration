from os import listdir
from os.path import dirname, join

from patoolib import extract_archive, test_archive
from patoolib.util import PatoolError

from config import DOWNLOAD_ROOT, COPIED_DATA_DIRNAME
from packages.utils.log import log_task, printex, log
from packages.utils.path import search_with_criteria


def extract_all():
    """
    Décompresse toutes les archives à disposition.

    Solutions explorées :
    - "lzma" ne gère pas les archives, mais seule la (dé)compression d'un unique fichier compressé en ".7z"
    - la bibliothèque C "libarchive" (téléchargée via conda) via un wrapper python "libarchive-c" (téléchargée via pip)

    Choix final porté sur "patoolib" car gère beaucoup de formats.
    En réalité c'est un wrapper.
    Après détection des types MIME, il fait appel aux exécutables/librairies appropriés ("7zr" par exemple).
    """

    taskname = 'extracting'
    log_task(taskname, 'start')

    # liste des chemins complets des archives à extraire
    log('searching for archives to extract in "{}". this may take a while'.format(DOWNLOAD_ROOT))
    archives_to_extract = search_with_criteria(DOWNLOAD_ROOT, is_archive, search_depth=2)
    archives_to_extract += search_with_criteria(join(DOWNLOAD_ROOT, COPIED_DATA_DIRNAME), is_archive, search_depth=2)
    total = len(archives_to_extract)
    log('{} archive(s) found in "{}"'.format(total, DOWNLOAD_ROOT))

    # on extrait archive par archive
    no_exception = True
    some_action_performed = False
    done = 0
    for archive_path in archives_to_extract:

        # journalisation de l'avancement global
        done += 1

        # on vérifie que l'archive n'a pas déjà été extraite
        archive_dir = dirname(archive_path)
        if len(listdir(archive_dir)) > 1:
            # si archive pas seule dans le dossier, on considère qu'elle a été extraite
            log('archive "{}" ignored because previously extracted ({}/{})'.format(archive_path, done, total))

        else:

            log('extracting archive "{}" ({}/{})'.format(archive_path, done, total))

            try:
                extract_archive(archive_path, verbosity=-1, outdir=archive_dir, interactive=False)
            except PatoolError as e:
                no_exception = False
                printex(e, 'the file extension probably does not match the real data type')
            except Exception as e:
                no_exception = False
                printex(e)
            finally:
                some_action_performed = True

    if no_exception:
        if some_action_performed:
            log('all retrieved archives extracted successfully')
        else:
            log('nothing were done, because all archives were already extracted')
    else:
        log('sorry, some retrieved archives could not be extracted', 'warn')

    log_task(taskname, 'end')


def is_archive(params):
    """
    Détermine si le fichier passé en paramètre est une archive.

    :param params: les paramètres
    :return: True si c'est une archive, False sinon
    """
    # noinspection PyBroadException
    try:
        test_archive(params['path'], verbosity=-1, interactive=False)
    except Exception:
        return False
    return True
