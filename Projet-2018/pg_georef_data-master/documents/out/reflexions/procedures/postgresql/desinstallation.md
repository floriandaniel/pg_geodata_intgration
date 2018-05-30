# Si l'on souhaite vérifier que l'installation part de zéro

- s'assurer de l'abscence de postgres

Pour cela, vérifier que le résultat de la commande suivante est vide.
_(sauf une ligne éventuellement présente contenant `pgdg-keyring`)_  

`dpkg -l | grep postgresql`  

Si ce n'est pas le cas, effectuer les deux étapes ci-après.  
Attention, cela supprimera toute installation de `postgresql` !

- purger les paquets listés via la commande précédente

Il faut remplacer les noms des paquets avec ceux listés précédemment.  

`sudo apt-get purge -y postgresql-9.6 postgresql-9.6-postgis-2.3 postgresql-9.6-postgis-2.3-scripts postgresql-client-9.6 postgresql-client-common postgresql-common postgresql-contrib-9.6`

- supprimer les paquets inutilisés (dont aucun autre ne dépend)
`sudo apt-get autoremove -y`
