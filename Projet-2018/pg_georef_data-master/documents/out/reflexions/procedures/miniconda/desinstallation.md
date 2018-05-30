# Si l'on souhaite supprimer complètement miniconda

## Soit re-modifier le fichier `.bashrc`
_(si on n'utilise pas personnellement le `.bashrc`)_

Cette méthode conserve le `.bashrc` actuel en retirant les changements effectués par conda.

Une commande possible pour connaître ces changements est `grep conda ~/.bashrc`.
Retirer la ligne de commentaire ainsi que la ligne de la forme `export PATH="/path/to/miniconda/installation/bin:$PATH"`).

## Soit restaurer le fichier `.bashrc-miniconda2.bak` de backup
_(si on utilise personnellement le `.bashrc`)_

* Garder le `.bashrc` actuel en stock
`mv ~/.bashrc ~/.bashrc.bak`

* Restaurer le `.bashrc-miniconda2.bak` de backup  
`mv ~/.bashrc-miniconda2.bak ~/.bashrc`

* _(contraignant)_ Porter manuellement tout changement effectué par l'utilisateur dans `/.bashrc.bak` depuis l'installation de **miniconda** dans le `~/.bashrc` restauré !

## Puis supprimer miniconda

Supprimer simplement son dossier d'installation :  
 
`rm -rf ~/miniconda`

**ATTENTION**  
c'est une suppression **récursive** et **sans confirmation**, être prudent
