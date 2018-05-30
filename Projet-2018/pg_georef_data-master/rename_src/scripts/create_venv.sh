#!/usr/bin/env bash





########################################################
#
#### Prérequis
#
# - la commande conda doit être fonctionnelle et à jour (miniconda ou anaconda, peu importe)
# - conda-forge doit être le dépôt par défaut pour conda
# - que la valeur de la variable "venv_name" ci-dessous (partie "DÉFINITION DE VARIABLES") n'entre pas en conflit avec le nom d'un environnement déjà existant
#   la commande "conda info --envs" permet de lister les environnements conda existants
#   s'il y a effectivement un environnement portant déjà ce nom, il faut changer la valeur de la variable "venv_name" de manière à éviter un conflit
#
#### Rôle
#
# Ce script a pour rôle de créer l'environnement virtuel conda afin de l'exporter en YAML.
#
#### Procédure suivie par le script
#
# 1) Création de l'environnement virtuel
# 2) Activation de cet environnement virtuel dans le terminal appelant
# 2) Installation des paquets nécessaires sur cet environnement ("conda install" et "pip install")
# 3) Export de l'environnement virtuel en fichier YAML dans src/res
# 4) Suppression de l'environnement créé
#
#### Remarque(s) sur la qualité du script
#
# - Il aurait tout à fait été possible de créer directement le fichier YAML décrivant l'environnement.
# - Cependant, l'export via conda est la méthode la plus sûre. En effet, conda n'échouera pas dans le formatage, la version des paquets, etc. du fichier YAML.
#
########################################################





########################################################
#
# DÉFINITION DE FONCTION(S) UTILITAIRE(S) AU SCRIPT
#
########################################################

function log { echo -e "[$(echo "$1" | tr '[:lower:]' '[:upper:]')] $2" >&2; }

function space { echo -e "\n\n"; }






########################################################
#
# DÉFINITION DE VARIABLES
#
########################################################

venv_name="gd"
venv_filename="$venv_name.yml"
res_dir="$(dirname $(realpath $0))/../res"
venv_file_path="$res_dir/$venv_filename"
python_version="3.5"


########################################################
#
# CRÉATION DE L'ENVIRONNEMENT VIRTUEL
#
########################################################

log "info" "creating virtualenv \"$venv_name\" with python version \"$python_version\". here are the logs"
space
yes | conda create -n "$venv_name" python="$python_version"
space
log "info" "end of \"miniconda create\" logs. virtualenv creation complete"


. activate "$venv_name"
log "info" "virtualenv \"$venv_name\" activated"


# installation des bibliothèques nécessaires
log "info" "installing libraries into virtualenv \"$venv_name\". here are the logs"
space
yes | pip install patool
yes | conda install xlrd fiona shapely psycopg2
space
log "info" "end of install related logs. libraries installation complete"


########################################################
#
# EXPORT DE L'ENVIRONNEMENT
#
########################################################

conda env export > "$venv_file_path" 2>/dev/null
log "info" "virtualenv exported as \"$venv_file_path\""

# désactivation de l'environnement virtuel
. deactivate "$venv_name"
log "info" "virtualenv \"$venv_name\" deactivated"


########################################################
#
# NETTOYAGE
#
########################################################

log "info" "deleting virtual environnement \"$venv_name\". here are the logs"
space
yes | conda remove -n "$venv_name" --all
space
log "info" "virtualenv \"$venv_name\" deleted"
