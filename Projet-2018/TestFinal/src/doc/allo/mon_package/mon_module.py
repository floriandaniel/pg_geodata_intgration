# -*- coding: utf-8 -*-

"""
Ce module n'est la qu'a titre demonstratif
"""
def print_something() :
    print("c'est moi")

class MaClasse():
    """
    ceci constitue l'unique classe de mon_package.mon_module

    :param arg: argument du constructeur
    :type arg: int
    """

    def __init__(self, arg):
        """
        Ceci est le constructeur de MaClasse

        :param param: p1
        :type param: int
        """
        None

    def print_hello(self, name):
        """
        Permet d'imprimer le message « hello <nom> »

        :param name: le nom de l'usager
        :type name: str
        :return: un message personnalise
        :rtype: string
        """
        print(" hello " + name)
        return " Bonjour souhaite a " + name

if __name__ == "__main__":
    mon_objet = MaClasse()
    print (mon_objet.print_hello(" ami lecteur "))

