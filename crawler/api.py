from utils import cfg
import json 
import urllib.request


def get_json_product(itemid, limit, offset, shopid, type=0):
    '''Get JSON of a product
    * type = 0: get all ratings
    * type = 1..5: get ratings based on rating stars
    * country_code = 'vn' or 'sg'
    '''
    url = 'https://shopee.{}/api/v2/item/get_ratings?filter=0&flag=1&itemid={}&limit={}&offset={}&shopid={}&type={}'.format(
        cfg.country_code, itemid, limit, offset, shopid, type)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data


def get_json_recommend(limit, offset):
    url = 'https://shopee.{}/api/v4/recommend/recommend?bundle=daily_discover_main&limit={}&offset={}'.format(
        cfg.country_code, limit, offset)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data


def get_json_campaign(label, limit, offset):
    url = 'https://shopee.{}/api/v4/recommend/recommend?bundle=daily_discover_campaign&label={}&limit={}&offset={}'.format(
        cfg.country_code, label, limit, offset)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    return data