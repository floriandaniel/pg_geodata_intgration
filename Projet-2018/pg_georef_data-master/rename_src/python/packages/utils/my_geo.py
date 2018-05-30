import json
from urllib.parse import urlencode

from fiona.transform import transform_geom
from pip._vendor.requests import get
from shapely.geometry import shape

from config import PROXIES
from packages.utils.log import log


def geometry2wkt(geometry):
    """
    Produit le WKT à partir de la structure de géométrie.

    :param geometry: dict la géométrie
    :return: le WKT correspondant à la géométrie
    :rtype: string
    """
    return shape(geometry)


def wkt2srid(wkt):
    """
    Convertit un WKT en SRID.

    Repose sur un service web : utilisation de l'API REST http://prj2epsg.org/apidocs.html.
    :return: le SRID/le code EPSG correspondant au WKT d'entrée si trouvé, None sinon
    :rtype: int
    """

    # ---- point de départ : une réponse de "jatorre" dans le fil de discussion ci-dessous
    # https://gis.stackexchange.com/questions/7608/shapefile-prj-to-postgis-srid-lookup-table#7633

    # ---- avec osgeo, mais ne fonctionne pas dans beaucoup de cas
    # http://www.gdal.org/osr_tutorial.html
    # http://freecontent.manning.com/wp-content/uploads/using-spatial-references-with-osr.pdf
    # srs = SpatialReference()
    # srs.ImportFromESRI([wkt])
    # srs.AutoIdentifyEPSG()
    # srid = srs.GetAuthorityCode(None)

    # -------- préparation de la requête http
    query = urlencode({'exact': True, 'error': True, 'mode': 'wkt', 'terms': wkt})
    rest_api_url = 'http://prj2epsg.org/search.json'
    full_url = '{}{}{}'.format(rest_api_url, '?', query)

    # -------- récupération des résultats
    results = get(full_url, verify=False, proxies=PROXIES).content.decode()  # pas 'unicode_escape' car besoin   \"   , non pas   "
    r = json.loads(results)

    # -------- parsage de la réponse
    srid = None
    if r['exact']:
        srid = int(r['codes'][0]['code'])
    # else:
    #     if r['totalHits'] > 1:
    #         possible_srids = [int(cd['code']) for cd in r['codes']]
    #         log('several suitable source SRIDs have been detected : {}'.format(possible_srids))

    return srid


def reproject(geom, proj_src, proj_dst):
    """
    Reprojète un champ géométrie exprimé dans un référentiel source vers un référentiel cible.

    Cette fonction ne se soucie pas du cas d'égalité entre les projections source et cible. Cela doit être effectué dans les fonctions appelantes.

    Attention certaines ressources présentées dans les liens ci-dessous sont relativement anciennes.
    http://web.archive.org/web/20160802172057/http://www.remotesensing.org/geotiff/proj_list/
    https://gist.github.com/sgillies/1886782#file-even-more-functional-py
    https://gist.github.com/sgillies/3642564#file-1-py
    http://all-geo.org/volcan01010/2012/11/change-coordinates-with-pyproj/
    https://glenbambrick.com/2016/01/24/reproject-shapefile/

    :param geom: dict le champ géométrie de la donnée
    :param proj_src: str la projection d'entrée
    :param proj_dst: str la projection de sortie
    :return: le champ geometry, reprojeté
    :rtype: dict
    """

    return transform_geom(proj_src, proj_dst, geom)
