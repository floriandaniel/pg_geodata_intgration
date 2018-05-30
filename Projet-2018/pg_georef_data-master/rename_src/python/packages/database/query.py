from psycopg2._psycopg import ProgrammingError

from config import GEOMETRY_NAME, TO_POSTGRESQL_TYPE, SRID_NAME
from packages.utils.my_geo import geometry2wkt


def execute_query(query, conn):
    """Exécute une requête et en renvoie les résultats, le cas échéant."""
    results = []

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    try:
        results = cur.fetchall()
    except ProgrammingError as e:
        pass
    return results


def create_schema_if_not_exists(schema_name, conn):
    """Crée le schéma donné en paramètre si celui-ci est inexistant."""
    query = 'CREATE SCHEMA IF NOT EXISTS {}'.format(schema_name)
    execute_query(query, conn)


def create_table_if_not_exists(properties, params, conn):
    """Crée la table donnée en paramètre si celle-ci est inexistante."""
    query = build_create_table_query(properties, params)
    execute_query(query, conn)


def delete_empty_schemes(conn):
    """Nettoie (supprime) tous les schémas vides éventuellement créés au sein de la base."""

    # on récupère la liste de tous les schémas
    # noinspection SqlResolve
    select_query = 'SELECT schema_name FROM information_schema.schemata;'
    results = execute_query(select_query, conn)
    schemes = [str(s[0]) for s in results]

    # par défaut, DROP SCHEMA est en mode RESTRICT
    # "Refuse to drop the schema if it contains any objects. This is the default."
    # cf le lien ci-dessous
    # https://www.postgresql.org/docs/current/static/sql-dropschema.html
    # pour éviter les erreurs, on enlève de la liste les tables "dangeureuses"

    protected = ['public', 'information_schema'] + [t for t in schemes if t.startswith('pg_')]
    drop_list = [t for t in schemes if t not in protected]
    drop_empty_schemes_query = 'DROP SCHEMA IF EXISTS {};'.format(', '.join(drop_list))
    try:
        execute_query(drop_empty_schemes_query, conn)
    except Exception:
        pass


def build_create_table_query(properties, params):
    """Construit une requête de création de table à partir de propriétés données."""

    # champs pour requêtes
    attrs_and_their_types = '({})'.format(', '.join(['{} {}'.format(the_attr, TO_POSTGRESQL_TYPE[the_type.split(':')[0]]) for the_attr, the_type in properties.items()]))
    scheme_dot_table = '"{}"."{}"'.format(params['schema'], params['table'])

    query = 'CREATE TABLE IF NOT EXISTS {} {};'.format(scheme_dot_table, attrs_and_their_types)

    return query


def build_insert_query(properties, params, georef=True):
    """Construit une requête d'insertion dans une table à partir d'une feature donnée."""

    # valeurs intermédiaires
    columns = list(properties.keys())
    wkt, srid, geometry_field = None, None, None
    if georef:
        wkt = geometry2wkt(properties['geometry'])
        srid = params[SRID_NAME]
        geometry_field = "ST_GeomFromText('{}', {})".format(wkt, srid)

    fields_pg_repr = []
    for attr, p in properties.items():

        # valeurs manquantes
        if p is None or p == '':
            attr_repr = 'NULL'

        # champ géométrie
        elif georef and attr == GEOMETRY_NAME:
            attr_repr = geometry_field

        # chaînes de caractères à échapper au niveau de PostgreSQL en doublant les guillemets simples
        elif isinstance(p, str):
            attr_repr = "'{}'".format(p.replace("'", "''"))

        # champs ne posant pas de problèmes particuliers, on utilise leur représentation standard
        else:
            attr_repr = str(p)

        # on ajoute la représentation adéquate à la liste
        fields_pg_repr.append(attr_repr)

    # champs pour requêtes
    table_name = '"{}"."{}"'.format(params['schema'], params['table'])
    fields_list = '({})'.format(', '.join(columns))
    values = '({})'.format(', '.join(fields_pg_repr))

    query = 'INSERT INTO {} {} VALUES {};'.format(table_name, fields_list, values)

    return query


def table_empty(params, conn):
    """
    Permet de savoir si une table est vide ou non.

    :param params: dict les paramètres d'import, notamment le nom du schémas et de la table
    :param conn: la connexion à la base de données
    :return: True si la table est vide, False Sinon
    """
    query = 'SELECT CASE WHEN EXISTS (SELECT * FROM "{}"."{}" LIMIT 1) THEN 0 ELSE 1 END;'.format(params['schema'], params['table'])
    return bool(execute_query(query, conn)[0][0])


def get_table_srid(params, conn):
    """
    Donne le SRID de la table dont le nom est fourni en paramètre.

    Assume que toutes les données de la table sont stockées dans un seul et même référentiel.
    :param params: dict les paramètres d'import, notamment le nom du schémas et de la table
    :param conn: la connexion à la base de données
    :return: le srid si la table n'est pas vide, None sinon
    """

    srid = None

    if not table_empty(params, conn):
        query = 'SELECT "{}" FROM "{}"."{}" LIMIT 1;'.format(SRID_NAME, params['schema'], params['table'])
        srid = execute_query(query, conn)[0][0]

    return srid
