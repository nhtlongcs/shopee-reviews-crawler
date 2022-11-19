import datetime
from utils import format_string


def get_ratings_from_json(json_data, min_len_str=4):
    data = json_data['data']
    ratings = data['ratings'] if data != None else None
    result = []
    if ratings != None:
        for r in ratings:
            itemid = r['itemid']
            shopid = r['shopid']
            userid = r['userid']
            cmtid = r['cmtid']
            mtime = datetime.datetime.fromtimestamp(
                r['mtime']).strftime('%d-%m-%Y %H:%M:%S')
            rating_star = r['rating_star']
            comment = format_string(r['comment'])
            if comment != None and len(comment) >= min_len_str:
                result.append({
                    'itemid': itemid,
                    'shopid': shopid,
                    'userid': userid,
                    'cmtid': cmtid,
                    'mtime': mtime,
                    'rating_star': rating_star,
                    'comment': comment
                })
    return result


def get_products_from_json(json_data, get_top_product=False):
    data = json_data['data']
    sections = data['sections'] if data != None else []
    result = []
    for s in sections:
        data = s['data']
        item = data['item']
        if item != None:
            for i in item:
                shopid = i['shopid']
                itemid = i['itemid']
                product_name = i['name']
                shop_name = i['shop_name']
                shop_rating = i['shop_rating']
                sold = i['sold']
                rating_star = i['item_rating']['rating_star']
                rating_count = i['item_rating']['rating_count']
                result.append({
                    'shopid': shopid,
                    'itemid': itemid,
                    'product_name': product_name,
                    'shop_name': shop_name,
                    'shop_rating': shop_rating,
                    'sold': sold,
                    'rating_star': rating_star,
                    'rating_count': rating_count
                })
        if get_top_product:
            top_product = data['top_product']
            if top_product != None:
                for t in top_product:
                    list = t['list']
                    data = list['data']
                    item_lite = data['item_lite']
                    if item_lite != None:
                        for i in item_lite:
                            shopid = i['shopid']
                            itemid = i['itemid']
                            product_name = i['name']
                            shop_name = i['shop_name']
                            shop_rating = i['shop_rating']
                            sold = i['sold']
                            rating_star = i['item_rating']['rating_star']
                            rating_count = i['item_rating']['rating_count']
                            result.append({
                                'shopid': shopid,
                                'itemid': itemid,
                                'product_name': product_name,
                                'shop_name': shop_name,
                                'shop_rating': shop_rating,
                                'sold': sold,
                                'rating_star': rating_star,
                                'rating_count': rating_count
                            })
    return result
