import sys

from config import SEVERITY_LEVELS, LOG_LEVEL, VISUAL_SEPARATOR_CARACTER, VISUAL_SECTION_DECORATOR_LENGTH


def printerr(msg):
    """
    Affiche un message sur stderr.

    :param msg: string le message
    """
    sys.stderr.write(msg + '\n')


def log(msg, lvl='info'):
    """
    Journalise les évènements de manière formatée.

    Les messages seront préfixés du niveau de sévérité.
    Le LOG_LEVEL précise l'importance moindre à partir de laquelle afficher le message.
    :param msg: string le message
    :param lvl: string le niveau
    """

    def print_it():
        printerr('[{}] {}'.format(lvl.upper(), msg))

    levels_to_print = SEVERITY_LEVELS[:SEVERITY_LEVELS.index(LOG_LEVEL)+1]

    if lvl in levels_to_print:
        print_it()

    # niveau spécial non défini par défaut
    # on affiche donc le message indépendemment du LOG_LEVEL
    if lvl not in SEVERITY_LEVELS:
        print_it()


def printex(e, msg='unknown'):
    """
    Affiche une exception de manière lisible.

    :param e: Exception l'exception
    :param msg: string la raison
    """

    etype = type(e).__name__
    log('an exception occured. reason : "{}". see the stacktrace dump below'.format(msg), 'error')

    # séparateur visuel de longueur adaptée
    symbol = VISUAL_SEPARATOR_CARACTER
    sep = symbol * (len(etype) + 4)

    printerr('\n{}\n{}\n{}\n{}\n{}\n'.format(sep, '{} {} {}'.format(symbol, etype, symbol), sep, str(e), sep))
    log('end of stacktrace dump', 'error')


def log_task(taskname, begin_or_end):
    """
    Affiche de façon formatée le début ou la fin d'une tâche.

    :param taskname: string le nom de la tâche, si possible en un unique verbe+ing, en anglais
    :param begin_or_end: string 'begin' ou 'end' selon le statut
    """
    decorator = VISUAL_SEPARATOR_CARACTER * VISUAL_SECTION_DECORATOR_LENGTH
    if begin_or_end == 'start':
        log('{0} starting {1} task {0}'.format(decorator, taskname))
    if begin_or_end == 'end':
        log('{0} {1} task complete {0}'.format(decorator, taskname))
