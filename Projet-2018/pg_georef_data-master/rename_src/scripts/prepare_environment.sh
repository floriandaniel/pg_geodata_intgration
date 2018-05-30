#!/usr/bin/env bash





########################################################
#
#### Rôle
#
# Ce script a pour rôle de préparer l'environnement nécessaire au code python pour s'exécuter sans embûche.
#
#### Prérequis
#
# - Le mot de passe pour "sudo" pourra être demandé à plusieurs reprises au cours de l'exécution. Le renseigner.
# - Ce script doit être exécuté en se situant dans son répertoire.
# - Vérifier que la variable "venv_name" ci-dessous (partie "MODIFICATIONS DIVERSES SUR L'ENVIRONNEMENT") a bien pour valeur le nom du fichier .yml dans src/res.
#
#### Tâches réalisées
#
# - changement des permissions sur la racine utilisée par défaut par le code python
# - installation du paquet "p7zip"
# - installation de miniconda
# - import de l'environnement conda
#
########################################################





########################################################
#
# DÉFINITION DE FONCTION(S) UTILITAIRE(S) AU SCRIPT
#
########################################################

function log { echo -e "[$(echo "$1" | tr '[:lower:]' '[:upper:]')] $2" >&2; }

function space { echo -e "\n\n\n"; }





########################################################
#
# VÉRIFICATION QUE LE SCRIPT EST SOURCÉ
#
########################################################

# le script est-il sourcé ?
# http://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced#34642589
$(return >/dev/null 2>&1)
if [ "$?" -eq "0" ]
then # oui, le script est sourcé





################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################





########################################################
#
# MODIFICATIONS DIVERSES SUR L'ENVIRONNEMENT
#
########################################################




# modification de droits

# dans config.py, récupération du nom du fichier de configuration
# le chemin relatif utilisé est considéré comme fixe
# les deux lignes suivantes nous intéressent
#
# CONFIG_GENERAL_NAME = 'general.conf'
# ALL_CONFIG_FILE_EXTENSION = '.json'

# changement des permissions sur la racine utilisée par défaut par le code python

python_config_file_path="../python/config.py"
log "info" "retrieving permanent general configuration file path from \"$python_config_file_path\""
config_general_name="$(sed -nr 's#^CONFIG_GENERAL_NAME *= *\d39([^\d39]*)\d39$#\1#p' "$python_config_file_path" 2>/dev/null)"
all_config_file_extension="$(sed -nr 's#^ALL_CONFIG_FILE_EXTENSION *= *\d39([^\d39]*)\d39$#\1#p' "$python_config_file_path" 2>/dev/null)"
res_dir="../res"
permanent_config_general_file_path="$res_dir/$config_general_name$all_config_file_extension"
log "info" "found \"$permanent_config_general_file_path\""

log "info" "retrieving the \"directory to use\" path from \"$permanent_config_general_file_path\""
place_to_be="$(sed -nr 's#^[^"]*"place_to_go":"([^"]*)",?$#\1#p' "$permanent_config_general_file_path" 2>/dev/null)"
log "info" "found \"$place_to_be\""
sudo chmod 777 "${place_to_be}"
log "info" "permissions changed on \"$place_to_be\""

# installation des paquets "p7zip" et "xzdec"
log "info" "starting p7zip + xzdec download & installation. here are the apt-get logs"
space
sudo apt-get install -y p7zip xzdec
space
log "info" "end of apt-get logs"



########################################################
#
# INSTALLATION DE MINICONDA
#
########################################################

# définition de variables afin de clarifier les appels
download_filename="Miniconda3-latest-Linux-x86_64.sh"
download_url="https://repo.continuum.io/miniconda/$download_filename"
script_name="miniconda.sh"
install_script="/tmp/$script_name"
install_dir="$HOME/miniconda"
conda_executable_dir="$install_dir/bin"
venv_name="gd"
venv_to_import="$res_dir/$venv_name.yml"


# installation de miniconda
log "info" "downloading miniconda"
wget -q "$download_url" -O "$install_script"
chmod +x "$install_script"
log "info" "installing miniconda. here are the logs"
space
bash "$install_script" -b -p "$install_dir"
space
log "info" "end of miniconda install logs. miniconda installation complete"


# suppression du script d'installation
log "info" "deleting installation script \"$install_script\""
rm -f "$install_script"


# ajout de conda au path
echo -e "\n\n# adding conda to path\nexport PATH=\"$PATH:$install_dir/bin\"" >> "$HOME/.bashrc"
. "$HOME/.bashrc"
log "info" "conda added to path (\"$conda_executable_dir\")"


# ajout de conda-forge en tant que dépôt prioritaire
log "info" "adding conda-forge as default repository"
conda config --add channels conda-forge &>/dev/null


# mise-à-jour de conda
log "info" "updating conda. here are the logs"
space
yes | conda update conda
space
log "info" "end of miniconda update log. miniconda update complete"




########################################################
#
# IMPORT DU VIRTUALENV
#
########################################################

# import de l'environnement virtuel (= création à partir des spécifications contenues dans le fichier YAML)
log "info" "creating virtualenv from file \"$venv_to_import\". here are the logs"
space
conda env create -f "$venv_to_import"
space
log "info" "end of import related logs"


# activation de l'environnement virtuel
log "info" "activating virtualenv \"$venv_name\""
. activate "$venv_name"





################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################





else # non, le script n'est pas sourcé

    log "error" "please source the script as follows : \". $0\". exiting"
    exit

fi
