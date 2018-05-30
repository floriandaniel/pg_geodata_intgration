
# But recherché

Il est ici question d'installer l'environnment système souhaité à l'aide de `miniconda` sous **Ubuntu _(64-bit)_**.

## Installation de miniconda

* Télécharger le script d'installation  
`wget -q 'https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh'`

* Rendre ce script exécutable  
`chmod +x Miniconda3-latest-Linux-x86_64.sh`

* Le lancer en tant que **root**  
`sudo ./Miniconda3-latest-Linux-x86_64.sh`

* Suivre les étapes et donner le répertoire souhaité comme répertoire d'installation lorsque demandé. Accepter d'ajouter au path.

* Supprimer l'installateur  
`rm Miniconda3-latest-Linux-x86_64.sh`

* Mettre-à-jour **conda**  
`conda update conda`

## Setup de l'environnement

* Ajout du dépôt **conda-forge**  
`conda config --add channels conda-forge`

* Création d'un nouvel environnement
`conda create -n gd python=3.5`

* Activation du nouvel environnement  
`. activate gd`

* Installation des packages nécessaires
`pip install patool`
