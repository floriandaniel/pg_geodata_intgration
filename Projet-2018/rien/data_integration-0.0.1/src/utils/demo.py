# -*- coding: utf-8 -*-

from demo2 import printAllo

def ma_fonction_simple(numerateur, denominateur):
    """
    Effectue une division

    :param numerateur: le numerateur de la division
    :type numerateur: int
    :param denominateur: le denominateur de la division
    :type denominateur: int
    :return: la valeur entiere de la division
    :rtype: int
    """
    printAllo()
    if denominateur == 0:
        print("denominateur interdit")
        print_something()   
    else:
        result = int(numerateur)/int(denominateur)
        return result

def some_function(first, second="two", **kwargs):
    r"""Fetches and returns this thing

    :param first:
        The first parameter
    :type first: ``int``
    :param second:
        The second parameter
    :type second: ``str``
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *extra* (``list``) --
          Extra stuff
        * *supplement* (``dict``) --
          Additional content

	   * *Alloo*

    """
