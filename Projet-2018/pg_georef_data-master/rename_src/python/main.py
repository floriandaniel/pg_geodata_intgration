#!/usr/bin/env python
# coding=utf-8


"""Contient l'exécution séquentielle des différentes fonctions"""


# /!\ ne pas déplacer /!\
# évite de générer des dossier __pycache__ indésirables dans l'arborescence du projet
import sys

sys.dont_write_bytecode = True


# ________________________________ imports


# chargement de la configuration
from config import *


# imports des fonctions de plus haut niveau, qui seront appelées tour à tour
from packages.data_retrieving.retrieve import retrieve_all
from packages.data_retrieving.extract import extract_all
from packages.data_processing.convert import convert_then_import_all

# ________________________________ exécution


retrieve_all()
extract_all()
convert_then_import_all()


# TODO le castage de types en fonction de la config des imports
# TODO tout refaire "de zéro" en programation orienté objet
