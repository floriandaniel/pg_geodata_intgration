from packages.database.query import get_table_srid
from packages.utils.my_geo import wkt2srid
from packages.utils.my_json import check_for_node_in_parent


def get_user_srids(params):
    """
    Récupère les projections source et destination renseignées par l'utilisateur.

    :param params: dict les paramètres d'import
    :return: (srid_src_user, srid_dst_user)
    :rtype: tuple of ints/None values
    """

    # SRID source
    srid_src_user = None
    if check_for_node_in_parent('srid_source', params):
        srid_src_user = params['srid_source']

    # SRID destination
    srid_dst_user = None
    if check_for_node_in_parent('srid_destination', params):
        srid_dst_user = params['srid_destination']

    return srid_src_user, srid_dst_user


def get_detected_srids(wkt, params, conn):
    """
    Détecte les projections source et destination.

    :param wkt: str le well-known text de la donnée
    :param params: dict les paramètres d'import
    :param conn: la connexion à la base de données
    :return: (srid_src_detected, srid_dst_detected)
    :rtype: tuple of ints/None values
    """

    # SRID source
    srid_src_detected = wkt2srid(wkt)

    # SRID destination
    srid_dst_detected = get_table_srid(params, conn)

    return srid_src_detected, srid_dst_detected
