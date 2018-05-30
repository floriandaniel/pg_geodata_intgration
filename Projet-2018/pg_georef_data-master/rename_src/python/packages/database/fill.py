from os.path import exists

import fiona
from fiona.ogrext import OrderedDict
from xlrd import open_workbook
from xlrd.timemachine import xrange

from config import YEAR_NAME, YEAR_TYPE, YEAR_LENGTH, VERSION_NAME, VERSION_TYPE, VERSION_LENGTH, SRID_NAME, SRID_TYPE, SRID_LENGTH, GEOMETRY_NAME, GEOMETRY_TYPE, DOWNLOAD_ROOT, REMEMBER_IMPORT_FILE_PATH, TO_POSTGRESQL_TYPE
from packages.data_processing.extensions import find_key_file_from_params
from packages.data_processing.geographic import get_user_srids, get_detected_srids
from packages.database.query import build_insert_query, create_schema_if_not_exists, create_table_if_not_exists, table_empty, execute_query
from packages.utils.log import log, printex
from packages.utils.my_geo import reproject
from packages.utils.my_json import check_for_node_in_parent
from packages.utils.string import simplify, check_for_line_in_file


def to_database(ressource, conn):
    """
    Parcoure la donnée et l'insère dans la base de données en créant dynamiquement les requêtes.

    Travaille les données en flux uniquement.
    Pour cela, on utilise les générateurs python et les requêtes sont construites à la volée pour chaque tuple (au sens base de données) de la donnée d'entrée.
    """

    # déclarations
    okko = True
    cur = conn.cursor()
    import_mode = ressource['import_mode']
    params = ressource['params']
    mode = ''
    if check_for_node_in_parent('mode', params):
        mode = params['mode']
    data_name = params['data_name']
    shortname = simplify(params['shortname'])

    # on trouve le fichier clé pour ce traitement
    input_file = find_key_file_from_params(params, DOWNLOAD_ROOT)
    if input_file == '':
        log('ignoring data about "{} / {}" because a crucial file is missing'.format(shortname, data_name), 'warn')
        okko = False
    else:

        # la donnée aurait-elle déjà été importée ?
        already_done = False
        if exists(REMEMBER_IMPORT_FILE_PATH):
            already_done = check_for_line_in_file(remember_line_builder(params), REMEMBER_IMPORT_FILE_PATH)

        # on ignore la donnée si l'import a déjà été effectué précédemment
        if already_done:
            log('ignoring data "{} / {}" because previously imported into database 1'.format(shortname, data_name))
        else:
            mode_msg = 'automatic' if mode == '' else mode
            log('importing data about "{} / {}" in mode "{} / {}" in schema.table "{}.{}"'.format(shortname, data_name, import_mode, mode_msg, params['schema'], params['table']))

            with fiona.drivers():

                # on ouvre le fichier d'entrée
                # ajoute, conserve, et modifie les colonnes désirées
                # et écrit le tout dans un fichier de sortie
                # l'ensemble des traitements s'effectuent en flux

                with fiona.open(input_file, 'r') as in_data:

                    # on part du schéma initial
                    in_schema = in_data.schema.copy()

                    # effectuer les modifications sur les champs
                    properties, prop_changes_ok = apply_params_to_properties(params, in_schema['properties'], from_where='create')
                    okko = prop_changes_ok and okko

                    if okko:
                        try:

                            # -------- schéma et table

                            # si le schéma (au sens espace de noms pour la base de données) n'existe pas, le créer
                            create_schema_if_not_exists(params['schema'], conn)

                            # création éventuelle de la table
                            if import_mode == 'controlee_nouvelle_table':
                                # on fait en sorte que la table existe en tentant systématiquement de la créer
                                create_table_if_not_exists(properties, params, conn)

                            # -------- détection des projections I/O

                            srid_src_user, srid_dst_user = get_user_srids(params)
                            srid_src_detected, srid_dst_detected = get_detected_srids(in_data.crs_wkt, params, conn)
                            srid_src, srid_dst = None, None

                            # -------- réactions aux projections à disposition (source)

                            if srid_src_user is not None:
                                if srid_src_user != srid_src_detected and srid_src_detected is not None:
                                    log('detected source SRID ({}, ignored) is different from the enforced one that you gave ({}, picked)'.format(srid_src_detected, srid_src_user), 'warn')
                                srid_src = srid_src_user
                            else:
                                if srid_src_detected is not None:
                                    srid_src = srid_src_detected
                                else:
                                    okko = False
                                    log('sorry, you will need to define manually the source SRID', 'error')

                            # -------- réactions aux projections à disposition (destination)
                            if okko:
                                if import_mode == 'controlee_nouvelle_table':
                                    srid_dst = srid_src
                                    if srid_dst_user is not None:
                                        srid_dst = srid_dst_user
                                    params[SRID_NAME] = srid_dst
                                else:
                                    if srid_dst_user is not None:
                                        log('ignoring the given destination SRID, which is useless regarding the import mode', 'warn')
                                    if srid_dst_detected is not None:
                                        srid_dst = srid_dst_detected
                                        params[SRID_NAME] = srid_dst
                                    else:
                                        okko = False
                                        msg_beginning = 'weird, cannot find destination SRID.'
                                        if table_empty(params, conn):
                                            msg_ending = 'table exists but is empty. drop it manually, change the import mode, then retry'
                                        else:
                                            msg_ending = 'check in database that the SRID column is named "{}"'.format(SRID_NAME)
                                        log('{} {}'.format(msg_beginning, msg_ending), 'error')

                            # -------- modifications structurelles et import

                            if okko:

                                reprojection_needed = okko and (srid_src != srid_dst)
                                proj_src, proj_dst = None, None
                                if reprojection_needed:
                                    prefix = 'epsg:'
                                    proj_src, proj_dst = '{}{}'.format(prefix, srid_src), '{}{}'.format(prefix, srid_dst)
                                    log('data will be reprojected from SRID {} to {}'.format(srid_src, srid_dst))

                                # si nouveaux champs, les ajouter à la table en base de données
                                log('adding new fields to table in database')
                                if check_for_node_in_parent('new_fields', params):
                                    for nf in params['new_fields']:
                                        the_name = nf['name']
                                        the_type_name, the_type_length = nf['type'].split(':')
                                        query = 'ALTER TABLE "{}"."{}" ADD COLUMN {} {}({});'.format(params['schema'], params['table'], the_name, the_type_name, the_type_length)
                                        execute_query(query, conn)

                                # on travaille les données en flux, chaque feature aura son "INSERT"
                                for feature in in_data:

                                    # recopie des valeurs attributaires pour chaque feature
                                    prop, okko = apply_params_to_properties(params, feature['properties'])
                                    prop[SRID_NAME] = srid_dst
                                    prop[YEAR_NAME] = params['year']
                                    prop[VERSION_NAME] = params['version']

                                    # -------- reprojection
                                    geom = feature['geometry']
                                    prop[GEOMETRY_NAME] = reproject(geom, proj_src, proj_dst) if reprojection_needed else geom

                                    # construction de la requête dynamiquement
                                    insert_query = build_insert_query(prop, params)
                                    cur.execute(insert_query)

                        except Exception as e:
                            conn.rollback()
                            okko = False
                            printex(e, 'insert query failed into table "{}"'.format(params['table']))
                        else:
                            conn.commit()
                            remember_this_import(params)

    return okko


def apply_params_to_properties(params, properties, from_where='insert'):
    """
    Effectue les modifications sur les propriétés en fonction des paramètres.

    Ces modifications portent sur les attributs.
    On touche donc à la structure, ce qui équivaudrait à un "ALTER".
    :param params: les paramètres
    :param properties: les propriétés
    :param from_where: d'où cette fonction a été appellée (pour évter de log un message identique pour n tuples)
    :return: les propriétés modifiées   et    True si tout s'est bien passé sinon False
    """
    okko = False
    pp = OrderedDict()

    try:

        # déclarations en noms courts
        mode = ''
        if check_for_node_in_parent('mode', params):
            mode = params['mode']
        bb = {}
        some_b_is_waiting_for_each_one = []
        if check_for_node_in_parent('bindings', params):
            bb = params['bindings']
            some_b_is_waiting_for_each_one = [b['from'] for b in bb]

        # on effectue les modifications précisées dans bindings
        for prop_key in properties.keys():
            need_to_copy_the_attribute = mode != 'keep_only'  # MODIFIED & KEEP_ONLY

            for b in bb:
                    b_from = b['from']
                    b_to = b['to']

                    if prop_key == b_from:

                        # -------- DROP
                        if b_to == '':
                            if mode == 'keep_only':
                                # on est sur un DROP + KEEP_ONLY, ce n'est pas valide
                                # on avertit et ignore la clause DROP
                                # en effet copy est déjà à False
                                if from_where != 'insert':
                                    log('ignoring non-sense DROP of attribute "{}" because of KEEP_ONLY mode'.format(b_from), 'warn')
                            else:
                                # l'attribut ne sera pas retenu, c'est-à-dire non copié
                                need_to_copy_the_attribute = False

                        # changement de nom de champ
                        else:
                            pp[b_to] = properties[prop_key]
                            # on vient de le copier en le renommant, inutile de le copier à nouveau "comme s'il n'était pas à modifier"
                            need_to_copy_the_attribute = False

                    # champ inchangé
                    already_copied = prop_key in pp.keys()
                    some_b_is_waiting_for_it = prop_key in some_b_is_waiting_for_each_one
                    if need_to_copy_the_attribute and not already_copied and not some_b_is_waiting_for_it:
                        pp[prop_key] = properties[prop_key]

            # pas de bindings donc on recopie sans se poser de questions
            if not check_for_node_in_parent('bindings', params):
                pp[prop_key] = properties[prop_key]

        # ajout des champs communs à tous les modes d'import
        pp[YEAR_NAME] = '{}:{}'.format(YEAR_TYPE, YEAR_LENGTH)
        pp[VERSION_NAME] = '{}:{}'.format(VERSION_TYPE, VERSION_LENGTH)
        pp[SRID_NAME] = '{}:{}'.format(SRID_TYPE, SRID_LENGTH)
        pp[GEOMETRY_NAME] = '{}:'.format(GEOMETRY_TYPE)

    except KeyError as e:
        printex(e, 'incorrect or missing node')
    except Exception as e:
        printex(e)
    else:
        okko = True

    return pp, okko


def remember_this_import(params):
    """
    Garde une trace de l'import effectué via le chemin de la donnée.
    
    :param params: dict les paramètres de la donnée qui a été importée avec succès
    """
    with open(REMEMBER_IMPORT_FILE_PATH, 'a') as f:
        f.write(remember_line_builder(params) + '\n')


def remember_line_builder(params):
    """
    Donne la ligne permettant de retenir l'import d'une donnée.

    :param params: dict les paramètres de la donée atomique concernée
    """
    line = '{} {}'.format(params['uri'], params['data_name'])
    return line


def xls_handler(ressource, conn):
    """Parse et importe directement une donnée non géographique en base."""

    # déclarations
    okko = True
    params = ressource['params']
    import_mode = ressource['import_mode']
    shortname, data_name = params['shortname'], params['data_name']
    schema, table = params['schema'], params['table']

    # la donnée aurait-elle déjà été importée ?
    already_done = False
    if exists(REMEMBER_IMPORT_FILE_PATH):
        already_done = check_for_line_in_file(remember_line_builder(params), REMEMBER_IMPORT_FILE_PATH)

    # on ignore la donnée si l'import a déjà été effectué précédemment
    if already_done:
        log('ignoring data "{} / {}" because previously imported into database'.format(shortname, data_name))

    else:

        # fichier d'entrée
        in_f = find_key_file_from_params(params, DOWNLOAD_ROOT)
        if in_f == '':
            okko = False
            log('ignoring data about "{} / {}" because a crucial file is missing'.format(shortname, data_name), 'warn')
        else:
            log('importing data about "{} / {}" in mode "{}" in schema.table "{}.{}"'.format(shortname, data_name, import_mode, schema, table))
            try:
                cur = conn.cursor()
                # parsage et import
                with open_workbook(in_f) as f:
                    for sn in f.sheet_names():
                        s = f.sheet_by_name(sn)

                        # -------- traitements préliminaires

                        # structure intermédiaire
                        attrs_and_their_types = [(x[0], TO_POSTGRESQL_TYPE[x[1]]) for x in [s.cell(0, ci).value.rsplit(':', 1) for ci in xrange(s.ncols)]]

                        # champs pour requêtes
                        scheme_dot_table = '"{}"."{}"'.format(schema, table)
                        fields_list = '({})'.format(', '.join(['{} {}'.format(the_attr, the_type) for the_attr, the_type in attrs_and_their_types]))
                        columns = [the_attr for the_attr, the_type in attrs_and_their_types]

                        # requête
                        query = 'CREATE TABLE IF NOT EXISTS {} {};'.format(scheme_dot_table, fields_list)

                        # -------- création de la table
                        if import_mode == 'controlee_nouvelle_table':
                            create_schema_if_not_exists(schema, conn)
                            execute_query(query, conn)

                        # -------- remplissage de la table
                        for ri in xrange(1, s.nrows):

                            values = [s.cell(ri, ci).value for ci in xrange(s.ncols)]
                            fionalike_struct = OrderedDict()

                            for index, v in enumerate(values):
                                # on repasse les "faux floats" en int
                                try:
                                    v = int(v)
                                except ValueError:
                                    pass
                                fionalike_struct[columns[index]] = v

                            query = build_insert_query(fionalike_struct, params, georef=False)
                            cur.execute(query)

            except Exception as e:
                conn.rollback()
                okko = False
                printex(e, 'insert query failed into table "{}"'.format(table))
            else:
                conn.commit()
                remember_this_import(params)

    return okko
