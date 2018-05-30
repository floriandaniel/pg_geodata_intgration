import json
from os.path import exists

from config import DYNAMIC_CONFIG_DATA_FILE_PATH, CONVERSION_ROOT
from packages.data_processing.extensions import get_path_from_params
from packages.data_processing.search import process_group, search_for_files_to_process
from packages.database.communicate import connect_to_database
from packages.database.query import delete_empty_schemes
from packages.utils.log import log_task, printex, log
from packages.utils.string import simplify


def convert_then_import_all():
    """Convertit/prépare l'ensemble des ressources, puis les importe en base."""

    taskname = 'converting and importing'
    log_task(taskname, 'start')

    # variables de journalisation
    amount_of_atomic_data_processed = 0
    amount_of_data_files_processed = 0
    things_were_done = False
    no_problem = True

    # on itère les ressources du fichier de configuration
    with open(DYNAMIC_CONFIG_DATA_FILE_PATH, 'r') as f:
        j = json.load(f)

        # connexion à la base de données
        conn = connect_to_database()
        try:

            for ressource in j['res']:

                # on recherche 'LA' donnée atomique
                to_process, params = search_for_files_to_process(ressource)

                # on envoie à traiter la donnée trouvée
                amount_of_data_files = len(to_process)
                if amount_of_data_files > 0:
                    log('{} data file found'.format(amount_of_data_files))

                    # on traite le groupe
                    if process_group(to_process, ressource, conn):
                        things_were_done = True
                        amount_of_data_files_processed += amount_of_data_files
                        amount_of_atomic_data_processed += 1
                    else:
                        no_problem = False
                        log('encountered some problem(s) with this data', 'error')

        except KeyError as e:
            printex(e, 'incorrect or missing node in "{}" (bad file structure)'.format(DYNAMIC_CONFIG_DATA_FILE_PATH))
        except Exception as e:
            printex(e)
        finally:
            delete_empty_schemes(conn)
            conn.close()

    # on journalise
    if things_were_done:
        log('{} atomic data successfully processed ({} files)'.format(amount_of_atomic_data_processed, amount_of_data_files_processed))
    else:
        if no_problem:
            log('nothing were done, because all found data were already prepared')
        else:
            log('nothing were done, because all found & processed data encountered errors', 'warn')

    log_task(taskname, 'end')
