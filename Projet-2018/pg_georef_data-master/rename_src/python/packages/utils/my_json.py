def check_for_node_in_parent(node_name, parent):
    """
    Vérifie la présence d'une node, non vide, dans une node parente.
    
    Ne vérifie pas de manière récursive, mais seulement au "niveau 0".
    :param node_name: string la node à rechercher
    :param parent: dict la node parente
    :return: True si node_name présente dans la node parente et non vide, False sinon
    """
    return node_name in parent and parent[node_name]
