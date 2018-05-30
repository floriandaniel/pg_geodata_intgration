#!/usr/bin/env bash





# Modifier simplement les lignes ci-dessous pour choisir le nom de la base ainsi que le mot de passe associé à l'utilisateur "postgres".
dbname='maps'
random_password='ifsttar' # eventually, there isn't much randomness is that password...





########################################################
#
############ Prérequis
#
# - Aucune trace restante d'une précédente quelconque installation de Postgresql, c'est-à-dire partir de zéro.
#
############ Rôle
#
#### Installation
#
# - appels à apt-get pour installer postgresql + postgis
#
#### Configuration
#
# - autoriser les connexions à distance
# - log des connexions et déconnexions
# - ajout support UTF-8 pour "template1"
# - création des extensions
# - création de deux rôles (groupes) distincts ; lecture ("r" pour "read") et écriture ("w" pour "write")
# - création d'un mot de passe pour l'utilisateur "postgres"
# - création de la base
#
########################################################
#
# Explications (aide à la compréhension globale) :
#
# - Postgres ne permet pas de distinction entre statut (= un ensemble de permissions, que j'appellerais "groupe") et "utilisateurs". En effet il permet uniquement de définir des "rôles". Un "rôle" duquel on ne peut pas se connecter, ayant certains droits, est utilisé en tant que groupe. Un rôle héritant d'un ou plusieurs groupes est alors un utilisateur.
# - Les utilisateurs ajoutés manuellement par la suite auront simplement à hériter l'un ou deux de ces rôles en fonction des droits souhaités.
# - Choix effectué d'utiliser la base "postgres", qui n'a pas de rôlé prédéfini, comme base stockant les groupes et les utilisateurs.
# - Le mot de passe assigné à l'utilisateur "postgres" --e-s-t--a-l-é-a-t--o-i-r-e-- et peut être retrouvé sur la sortie standard ainsi que dans un fichier texte placé dans le même répertoire que ce script.
# - Ce script a pour charge de créer la base afin que l'on puisse s'y connecter par la suite. En aucun cas il ne se charge de créer les tables, relations, ou utilisateurs.
#
########################################################
#
# Remarques (qualité du script, aspects plus techniques) :
#
# - L'ordre des actions est importante. Certains blocs doivent être exécutés avant les autres. Exemple : création de la base APRÈS modification du "template1".
# - Les versions utilisées ne sont pas destinées à être modifiées. Dans cette optique, les versions sont écrites en brutes dans le script.
# - Des commandes bash dites "wrappers" telles que "dropdb" existent. J'ai délibéremment choisi de ne pas les utiliser. Motivation : être sûr de ce que l'on fait réellement.
# - Ce script "d'initialisation" est destiné à être lancé une unique fois. Cela explique le fait que la gestion des erreurs soit "absente". En effet, le choix de se fier simplement aux logs des commandes lancées ainsi qu'à ceux de postgres permet une économie de code. De plus, l'intérêt serait limité, puisque les erreurs des commandes lancées sont explicites, et avec les logs du script il est aisé de retrouver, le cas échéant, la ligne en question. Cela permet un gain de clarté car le code reste aéré.
#
########################################################





########################################################
#
# DÉFINITION DE FONCTION(S) UTILITAIRE(S) AU SCRIPT
#
########################################################

# attention : les logs de ce script concernent ce script uniquement
# ces logs ne se subsitutent en rien aux logs de postgres lui-même
# logs de postgres sous ubuntu (exemple) :	tail -f /var/log/postgresql/postgresql-10-main.log
function log { echo -e "[$(echo "$1" | tr '[:lower:]' '[:upper:]')] $2" >&2; }





########################################################
#
# DÉTECTION DE L'EXÉCUTION EN TANT QUE ROOT (SUDO)
#
########################################################

# http://stackoverflow.com/questions/18215973/how-to-check-if-running-as-root-in-a-bash-script#18216122
if [[ $EUID > 0 ]]
    then log "error" "root permissions are required. please run with sudo. exiting"
    exit
fi





########################################################
#
# TÉLÉCHARGEMENT ET INSTALLATION DE POSTGRES & POSTGIS
#
########################################################

# ajout du dépôt
#url_repo="http://apt.postgresql.org/pub/repos/apt/"
#log "info" "adding apt-get repository \"$url_repo\""
#apt-get install -y software-properties-common &>/dev/null
#add-apt-repository "deb $url_repo xenial-pgdg main"

# ajout de la clé
#url_key="https://www.postgresql.org/media/keys/ACCC4CF8.asc"
#log "info" "adding apt-get key \"$url_key\""
#wget -qO- "$url_key" | apt-key add -


# installation
log "info" "starting postgresql download & installation, this may take a while. here are the apt-get logs\n\n\n"
# màj de la liste des paquets disponibles
apt-get update
# téléchargement & installation
apt-get install -y --allow-unauthenticated postgresql-10 pgadmin4 postgresql-10-postgis-2.3
echo -e "\n\n\n"
log "info" "end of apt-get logs"





########################################################
#
# CONFIGURATION DES MÉTHODES D'AUTHENTIFICATION
#
########################################################

# Cete partie ajoute les lignes ci-dessous dans "pg_hba.conf", en commantant le reste du fichier.
#
#	#TYPE DATABASE USER [ADDRESS] METHOD
#	local all postgres peer
#	host all all 0.0.0.0/0 md5
#
#
# "local all postgres peer" autorise l'utilisateur "postgres", en tant que compte système, à se connecter à la base de données sans autre(s) vérification(s).
# Cela signifie que n'importe quel utilisateur "sudoers" du système peut faire "sudo -u postgres psql" afin de se faire passer pour l'utilisateur "postgres". Ainsi, il peut accéder à la base de données sans mot de passe (autre que le mot de passe de son compte système, nécessaire pour passer root sur le système).
#
#
# "host all all 0.0.0.0/0 md5" autorise l'ensemble des connexions sur toutes les interface réseau, quel que soit l'utilisateur.
# Cependant il doit correspondre à un rôle dans la base et doit obligatoirement renseigner le mot de passe associé à ce compte afin d'accéder à la base de données.
#

authentification_config_file_path=$(sudo -u postgres psql -c 'SHOW hba_file;' 2>/dev/null | grep '.conf$' | xargs)

# commenter toutes les lignes non commentées
sed -i 's@^\([^#].*\)$@#\1@g' "$authentification_config_file_path"

# ajout d'une ligne donnant l'intitulé des colonnes
echo -e "\n\n\n####################################" | tee -a "$authentification_config_file_path" &>/dev/null
echo -e "#TYPE DATABASE USER [ADDRESS] METHOD" | tee -a "$authentification_config_file_path" &>/dev/null
# on accepte les connexions en local pour l'utilisateur "postgres" (conservation d'un accès non distant à condition d'être sudoers se faisant passer pour postgres avec "sudo -u postgres")
echo -e "local all postgres peer" | tee -a "$authentification_config_file_path" &>/dev/null
# on accepte toutes les connexions, quel que soit l'utilisateur ou la base, sur toutes les interfaces, mais avec mot de passe
echo -e 'host all all 0.0.0.0/0 md5' | tee -a "$authentification_config_file_path" &>/dev/null

log "info" "postgresql configuration file \"$authentification_config_file_path\" edited : defined the valid ways to get authenticated"





########################################################
#
# AUTORISATION DES CONNEXIONS À DISTANCE
#
########################################################

# dans "postgresql.conf", changement de
#	#listen_addresses = 'localhost'
# en
#	listen_addresses = '*'

configuration_file_path=$(sudo -u postgres psql -c 'SHOW config_file;' 2>/dev/null | grep '.conf$' | xargs)
sed -i 's#^.*\(listen_addresses = \d39\)localhost\(\d39.*\)$#\1\*\2#' "$configuration_file_path"
log "info" "postgresql configuration file \"$configuration_file_path\" edited : enabled remote connexions"




########################################################
#
# LOG DES (DÉ)CONNEXIONS
#
########################################################

# ce sont des informations intéressantes à journaliser qui ne le sont pas par défaut : on modifie ce comportement
sed -i 's#^.*\(log_connections = \).*\(\#*.*\)$#\1on\2#' "$configuration_file_path"
sed -i 's#^.*\(log_disconnections = \).*\(\#*.*\)$#\1on\2#' "$configuration_file_path"
log "info" "postgresql configuration file \"$configuration_file_path\" edited : enabled (dis)connexion's logs"





########################################################
#
# SUPPORT DE L'UTF-8
#
########################################################


# re-création de template1 avec l'encodage en UTF-8
# https://coderwall.com/p/j-_mia/make-postgres-default-to-utf8
# NB: les requêtes ne sont pas englobées dans des variables bash car le drop de la db doit se faire indépendemment
sudo -u postgres psql -c "UPDATE pg_database SET datistemplate=FALSE WHERE datname='template1';" &>/dev/null
sudo -u postgres psql -c "DROP DATABASE template1;" &>/dev/null
sudo -u postgres psql -c "CREATE DATABASE template1 WITH owner=postgres template=template0 encoding='UTF8';" &>/dev/null
sudo -u postgres psql -c "UPDATE pg_database SET datistemplate=TRUE WHERE datname='template1';" &>/dev/null
log "info" "configured UTF-8 support as default on \"template1\""





########################################################
#
# CRÉATION DE LA BASE DE DONNÉES
#
########################################################

create_db_query="CREATE DATABASE $(echo "$dbname") WITH TEMPLATE template1;"
drop_db_query="DROP DATABASE $(echo "$dbname");"
sudo -u postgres psql -c "$create_db_query" &>/dev/null
log "info" "database \"$dbname\" created"





########################################################
#
# CRÉATION DES EXTENSIONS
#
########################################################

create_extension_postgis_query="CREATE EXTENSION postgis;"
create_exension_postgis_topology_query="CREATE EXTENSION postgis_topology;"
sudo -u postgres psql -d "$dbname" -c "$create_extension_postgis_query" &>/dev/null
sudo -u postgres psql -d "$dbname" -c "$create_exension_postgis_topology_query" &>/dev/null
log "info" "created postgis extension"





########################################################
#
# AJOUT DE RÔLES (GROUPES) "read" et "write"
#
########################################################

# Comment supprimer un rôle possédant des droits
# http://stackoverflow.com/questions/3023583/postgresql-how-to-quickly-drop-a-user-with-existing-privileges
#
# testé mais non suffisant : 	ALTER DEFAULT PRIVILEGES FOR ROLE read REVOKE ALL ON TABLES FROM public;	(agit seulement sur les tuples existants en base, pas sur les éventuels futurs tuples créés, donc droits toujours présents et impossibilité de supprimer le rôle)

# lecture
create_role_r_query='CREATE ROLE r; ALTER DEFAULT PRIVILEGES GRANT SELECT ON TABLES TO r;'
delete_role_r_query='REASSIGN OWNED BY r TO postgres; DROP OWNED BY r; DROP ROLE r;'
sudo -u postgres psql -c "$create_role_r_query" &>/dev/null
log "info" "read-only role added"

# écriture
create_role_w_query='CREATE ROLE w; ALTER DEFAULT PRIVILEGES GRANT INSERT,UPDATE ON TABLES TO w;'
delete_role_w_query='REASSIGN OWNED BY w TO postgres; DROP OWNED BY w; DROP ROLE w;'
sudo -u postgres psql -c "$create_role_w_query" &>/dev/null
log "info" "write-only role added"





########################################################
#
# AJOUT D'UN MOT DE PASSE POUR L'UTILISATEUR "postgres"
#
########################################################

# on génère un mot de passe aléatoire et on l'affiche (utilisation de md5sum, mais aucune contrainte sur la fonction de hachage à utiliser : ici cela permet seulement de générer un mot de passe de taille constante. cela n'a bien évidemment strictement rien à voir avec les modes d'authentification md5 de postgres)

#random_password=$(head -100 /dev/urandom | md5sum | sed -nr 's#([[:alnum:]]+).*#\1#p')
#log "info" "random generated password is \"$random_password\""

# sauvegarde du mdp dans un fichier
res_dir="$(dirname $(realpath $0))/../res"
postgres_user_password_filename='postgres_password.txt'
pg_pw_save_as="$res_dir/$postgres_user_password_filename"
echo "$random_password" > "$pg_pw_save_as"

#### /!\ ATTENTION /!\ ####
#
# Le mot de passe, par facilité, sera celui indiqué en brut en haut de ce script ! bien comprendre qu'ici c'est un choix spécifique et concerté, à ne pas reproduire aveuglément donc)
# En effet il serait de bonne pratique d'utiliser le mot de passe précédemment généré (pour l'exercice... il ne sera donc pas utilisé).
# Après discussion, cette sécurité ne s'avère pas nécessaire voire contraignante.
#
####

# [connexion à distance] mise-à-jour du mot de passe de l'utilisateur "postgres" de la base
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD $(echo "'$random_password'");" &>/dev/null
log "info" "\"postgres\" user password is now \"$random_password\", please carefully keep it in a safe place"

# [connexion en local] mise-à-jour du mot de passe du compte utilisateur "postgres" de cette machine
echo "postgres:$random_password" | chpasswd

log "info" "\"postgres\" user password was saved to \"$postgres_user_password_filename\""





# redémarrage du service, nécessaire afin d'appliquer les changement de configuration effectués
service postgresql restart
