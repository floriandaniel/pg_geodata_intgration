from psycopg2 import connect

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER_NAME, DB_USER_PASSWORD


def connect_to_database():
    """
    Se connecte à la base de données et renvoie la connexion créée.

    À n'appeler qu'une seule fois, afin de ne maintenir qu'une seule connexion.
    Faire alors descendre cette connexion en cascade.
    """
    return connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER_NAME, password=DB_USER_PASSWORD)
