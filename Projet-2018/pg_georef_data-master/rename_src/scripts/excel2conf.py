#!/usr/bin/env python
# coding=utf-8

"""
Convertit un fichier excel "de confiance et connu" en un fichier de configuration pour import.

Les arguments sont les chemins complets des fichiers excel à convertir.
/!\ Aucune robustesse face à des fichiers tableur mal formatés en entrée. /!\
"""


import sys
from collections import OrderedDict
from json import dumps
from os.path import basename, extsep, abspath, dirname, join

from xlrd import open_workbook
from xlrd.timemachine import xrange

# erreur si aucun fichier n'a été spécifié
if len(sys.argv) == 1:
    sys.stderr.write('{0}\n'.format('[ERROR] at least one file must be provided. exiting'))
    exit()


def replace_types_nf(l):
    """Remplace les types tels qu'exprimés dans un format qui s'apparente à ceux que l'on peut trouver dans les python générées par Fiona, pour les new_fields."""

    # "l" est une liste de dicos, qui possèdent les nodes "from" "type" et "to"
    liste_modif = []

    for e in l:
        e_modif = OrderedDict()

        # recopie du name
        e_modif['name'] = e['name']

        # changement de la désignation du type
        e_modif['type'] = give_replacement(e['type'])

        # on ajoute l'élément avec type modifié à la liste de retour
        liste_modif.append(e_modif)

    return liste_modif


def replace_types_b(l):
    """Remplace les types tels qu'exprimés dans un format qui s'apparente à ceux que l'on peut trouver dans les python générées par Fiona, pour les bindings."""

    # "l" est une liste de dicos, qui possèdent les nodes "from" "type" et "to"
    liste_modif = []

    for e in l:
        e_modif = OrderedDict()

        # recopie du from
        e_modif['from'] = e['from']

        # changement de la désignation du type
        e_modif['type'] = give_replacement(e['type'])

        # recopie du to
        e_modif['to'] = e['to']

        # on ajoute l'élément avec type modifié à la liste de retour
        liste_modif.append(e_modif)

    return liste_modif


def give_replacement(in_type):
    """Renvoie le type de remplacement adéquat."""
    out_type = ''
    if in_type == 'character varying':
        out_type = 'str:1024'
    elif in_type in ['integer', 'int']:
        out_type = 'int:1024'
    elif in_type == 'numeric':
        out_type = 'float:1024'
    return out_type

# on procède de manière identique pour tous les fichiers
for in_f in sys.argv[1:]:

    # journalisation
    one_sheetname_is_ok = False
    print('[INFO] parsing "{0}"'.format(in_f))

    # entrée
    in_d = dirname(abspath(in_f))
    in_f_name, in_f_extension = basename(in_f).rsplit(extsep, 1)

    # sortie
    out_dict = {'res': []}
    out_d = in_d
    out_f = join(in_d, '{0}{1}data{1}conf{1}json'.format(in_f_name, extsep))

    # le mode d'import doit être le nom de la feuille
    valid_import_modes = ['controlee_nouvelle_table', 'controlee_table_existante']

    # attributs à dump tel quels
    easy_attrs = ['shortname', 'data_name', 'uri', 'schema', 'table', 'year', 'version', 'srid_source', 'srid_destination']

    # attributs qui requièrent un traitement "spécial", au cas par cas (nodes à plusieurs niveaux)
    difficult_attrs = ['new_fields', 'modified', 'keep_only', 'drop']

    # on traite ce fichier
    with open_workbook(in_f) as f:
        for sn in f.sheet_names():

            if sn not in valid_import_modes:
                print('[WARN] ignoring sheet "{0}" because it doesn\'t match any import mode'.format(sn))

            else:

                # au moins une feuille avait un nom OK
                one_sheetname_is_ok = True

                # la feuille
                s = f.sheet_by_name(sn)

                # on itère les lignes
                for row_index in xrange(s.nrows):

                    # objet pour la donnée de cette ligne
                    o = {'import_mode': sn, 'params': {}}
                    p = o['params']

                    # on n'ajoute pas l'objet créé si on est sur la ligne d'en-tête
                    if row_index != 0:
                        out_dict['res'].append(o)

                    # on itère les colonnes
                    for col_index in xrange(s.ncols):

                        # intitulé de la colonne
                        candidate_attr = s.cell(0, col_index).value

                        # si c'est une donnée, la traiter
                        if row_index != 0:

                            # valeur de la case
                            v = s.cell(row_index, col_index).value

                            # ne nécessite pas de traitement de faveur
                            if candidate_attr in easy_attrs:

                                # tous les nombres dans excel sont des floats
                                # pour éviter les années & srid avec une décimale
                                # on les passe ici en int
                                v_int = None
                                try:
                                    v_int = int(v)
                                except ValueError:
                                    pass
                                p[candidate_attr] = v_int if v == v_int else v

                            # bénéficie d'un traitement de faveur
                            elif candidate_attr in difficult_attrs and v != '':

                                if candidate_attr == 'new_fields':

                                    # création d'une structure intermédiaire d'entrée
                                    names_and_types = [s.split(',') for s in v.split(';')]
                                    # création d'une structure intermédiaire de sortie
                                    new_fields = []
                                    for nat in names_and_types:
                                        nf = OrderedDict([('name', nat[0]), ('type', nat[1])])  # si erreur veuillez vérifier les , et ; du fichier tableur
                                        # ajout du champ créé à la node des nouveaux champs
                                        if nf != {}:
                                            new_fields.append(nf)
                                    p['new_fields'] = replace_types_nf(new_fields)

                                if candidate_attr in ['modified', 'keep_only', 'drop']:

                                    # création d'une structure intermédiaire d'entrée
                                    from_type_to = [s.split(',') for s in v.split(';')]

                                    # création d'une structure intermédiaire de sortie
                                    bindings = []

                                    # on renseigne le mode
                                    if candidate_attr != 'drop':
                                        p['mode'] = candidate_attr

                                    # on standardise DROP pour avoir la même structure que MODIFIED et KEEP_ONLY
                                    else:
                                        from_type_to = [[e[0], '', ''] for e in from_type_to]

                                    # remplissage de bindings
                                    for ftt in from_type_to:
                                        bindi = OrderedDict([('from', ftt[0]), ('type', ftt[1]), ('to', ftt[2])])

                                        # ajout du champ créé à la node des nouveaux champs
                                        if bindi != {}:
                                            bindings.append(bindi)
                                    p['bindings'] = replace_types_b(bindings)

    if one_sheetname_is_ok:
        with open(out_f, 'w') as f:
            f.write(dumps(out_dict, indent=4, separators=(',', ': '), ensure_ascii=False) + '\n')
            print('[INFO] successfully generated configuration file "{}"'.format(out_f))

    else:
        print('[INFO] sorry, no configuration generated for this one. reason : found any sheet with an import mode as name')
