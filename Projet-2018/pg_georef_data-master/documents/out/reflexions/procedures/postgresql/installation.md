# Installation

Il est ici question de l'installation d'une base de données `postgresql` sous **Ubuntu**.

## À partir des sources

Comme toute compilation à partir des sources, à chaque étape, il suffit de suivre pas-à-pas les étapes décrites dans les fichiers types "README". De manière générale, on essaie de privilégier les installations qui s'effectuent à partir d'un dépôt si celui-ci existe. La raison principale qui peut pousser à installer à partir des sources est l'absence dans les dépôts de la version désirée et/ou de la distribution désirée.

* [dl et compilation/installation zlib à partir de la source](http://zlib.net/)
* installation des paquets suivants

>libreadline6/xenial,now 6.3-8ubuntu2 amd64  
>	Bibliothèques GNU readline et GNU history (bibliothèques d'exécution)
>  
>libreadline6-dev/xenial,now 6.3-8ubuntu2 amd64
>	Bibliothèques GNU readline et GNU history, fichiers de développement
>
>lib64readline6/xenial,now 6.3-8ubuntu2 i386
>	Bibliothèques GNU readline et GNU history, bibliothèques d'exécution (64-bit)
>
>lib64readline6-dev/xenial,now 6.3-8ubuntu2 i386
>	Bibliothèques GNU readline et GNU history, fichiers de développement (64-bit)

* [dl et installation de pg](http://www.postgresql.org/download)

---

## Via dépôt (méthode utilisée par le script)

Il suffit de suivre les [instructions indiquées ici](http://apt.postgresql.org/pub/repos/apt/README).

* ajout de la clé  
`wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add`
* màj de la liste des paquets disponibles  
`sudo apt-get update`
* installation  
`sudo apt-get install -y postgresql-9.6 postgresql-9.6-postgis-2.3`

---

# Troubleshooting

Si une fois installé la base `postgresql` ne semble pas être accessible, voici une suite d'étapes et un ensemble de commandes `bash` pouvant être utilisées afin de deviner la cause du problème et de tenter de le résoudre.

#### Ma base fonctionne-t-elle ?

Si la commande `sudo -u postgres psql -c "SELECT version();"` ne retourne pas d'erreur et donne, comme attendu, des informations de version, à priori `postgresql` fonctionne correctement. Cela signifie que le service fontionne et qu'il est possible de s'y connecter **localement**.

#### Le service `postgresql` est-il en cours de fonctionnement sur ma machine ?

Si `service postgresql status` retourne
>● postgresql.service  
>   Loaded: not-found (Reason: No such file or directory)  
>   Active: inactive (dead)  

alors `postgresql` ne s'est probablement pas installé ou installé correctement.

Pour lancer/relancer le service, il suffit de faire `sudo service postgresql start`/`sudo service postgresql restart`.

#### Connections distantes

Après l'installation, `postgresql` **n'accepte pas les connexions** autres que par `peer`, c'est-à-dire en tant que l'utilisateur par défaut `postgres` localement. Cela signifie que les connexions distantes seront rejetées. S'assurer d'avoir modifié les fichiers `postgresql.conf` et `pg_hba.conf` en conséquence.

Pour tenter de s'y connecter sur la boucle locale en tant que l'utilisateur `postgres`, faire `psql -h IP_DE_CETTE_MACHINE -d maps -U postgres`. La commande varie peu pour une connexion extérieure, remplacer simplement `127.0.0.1` par une des adresses ips autorisées dans `pg_hba.conf`. L'option `-U` de `psql` permet de préciser le rôle sous lequel on souhaite se connecter. Ajouter l'option `-W` afin qu'il nous soit demandé un mot de passe. `-d` précise la base de données voulue.

#### Le service `postgresql` est-il à l'écoute ?

Si le port par défaut (5432) indiqué dans `postgresql.conf` n'a pas été modifié, `sudo netstat -anp | grep 5432` permet de vérifier que le service est bien en `LISTEN` sur les interfaces réseau.

#### Le port est-il ouvert ?

`nmap -T4 IP_DE_CETTE_MACHINE -p 5432` va scaner le port `5432` et tenter de déterminer s'il est ouvert (`STATE` aura alors pour valeur `open`). On peut également utiliser la commande `netcat` comme suit : `nc -zv IP_DE_CETTE_MACHINE 5432`.

#### Connaître les actions du service `postgresql` : où puis-je trouver une journalisation des évènements ?

En tant que `daemon`, le service `postgresql` produit des logs sous `/var/log`. La commande `tail -f /var/log/postgresql/postgresql-9.6-main.log` permet de suivre l'activité de `postgresql` en temps réel. Appuyer sur `ctrl+c` pour la stopper.  
_(Ici, pour Ubuntu et une version donnée, le chemin est bien entendu à adapter)_  
