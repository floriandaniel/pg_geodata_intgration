# coding=utf-8
"""Fonctions utilitaires relatives aux traitement de chaîne des caractères."""

import re
import unicodedata


def simplify(s):
    """
    Donne une représentation épurée ascii de la chaîne de caractères en entrée.
    
    Transforme toute suite de caractères (longueur 1 à n), qui ne sont ni alphanumériques ni un underscore, en un unique underscore.
    N'autorise pas deux underscores successifs.
    N'autorise pas d'underscore en début ou fin de chaîne.
    :param s: string la chaîne à simplifier
    :return: la chaîne épurée
    :rtype: string
    """

    # passage des caractères unicodes dans leur "équivalent" ascii (on retire les accents)
    ascii_only = ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')

    # uniquement constituée de caractères alphanumériques et d'underscores
    alphanums_and_underscores_only = ''.join(re.sub('[^\\w_]', '_', ascii_only))

    # pas d'underscores consécutifs, ni en début ou fin
    the_cleaned_input = ''.join(re.sub('_+', '_', alphanums_and_underscores_only)).strip('_')

    return the_cleaned_input


def get_website_name_from_url(url):
    """
    Récupère le nom d'un site web à partir de son url.
    
    :param url: string une url quelconque
    :return: string le nom du site web associé
    """

    regex = re.compile(r"^[^/]*://(?:w{3}[.])?([^/]+)/.*$")
    site = regex.sub(r"\1", url)

    return site


def check_for_line_in_file(line, file):
    """
    Vérifie la présence d'une ligne dans un fichier.
    
    :param line: la ligne, sans le caractère de suat de ligne
    :param file: le chemin complet du fichie, qui doit être accessible en écriture 
    :return: True si line in file, False sinon
    """

    present = False
    with open(file, 'r') as f:
        present = line in f.read().splitlines()
    return present
