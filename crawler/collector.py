import time
from datetime import datetime
from parser import get_products_from_json, get_ratings_from_json

from api import get_json_campaign, get_json_product, get_json_recommend
from tqdm import tqdm
from utils import export_to_text_file


class Collector:

    def __init__(self):
        pass

    def get_all_reviews(self,
                        itemid,
                        shopid,
                        limit=6,
                        offset=0,
                        max_cmt=100,
                        min_len_cmt=4,
                        type=0):
        result = []
        with tqdm(total=(max_cmt // limit + 1) * limit) as pbar:
            while True:
                json_data = get_json_product(itemid, limit, offset, shopid,
                                             type)
                ratings = get_ratings_from_json(json_data, min_len_cmt)
                if ratings == []:
                    break
                else:
                    result += ratings
                offset += limit
                pbar.update(limit)
                if len(result) >= max_cmt:
                    break
        return result[:max_cmt]

    def get_all_recommended_products(self,
                                     max_products=100,
                                     limit=10,
                                     offset=0,
                                     get_top_product=False):
        result = []
        if max_products < limit:
            limit = max_products
        with tqdm(total=(max_products // limit + 1) * limit) as pbar:
            while True:
                start_time = time.time()
                # Notes: The number of products may be smaller than limit number although max_products < limit
                # So the number of result can be larger than the max_products
                json_data = get_json_recommend(limit, offset)
                products = get_products_from_json(json_data, get_top_product)
                if products == [] or len(result) >= max_products:
                    break
                else:
                    result += products
                    pbar.set_description(
                        'Đã lấy về {} sản phẩm trên tổng số tối đa {} sản phẩm. Mất {:0.2f} mili giây'
                        .format(len(result), max_products,
                                (time.time() - start_time) * 1000))
                offset += limit
                pbar.update(limit)

        return result[:max_products]

    def collect_reviews_product(self,
                                filename,
                                max_products,
                                min_len_cmt=4,
                                ratetypes=[]):
        '''Collect all reviews of products with specific rating_star
        * type = array [0]: get all rating_stars
        * type = array [1..5]: get only these rating_stars
        '''
        products = self.get_all_recommended_products(max_products=max_products,
                                                     get_top_product=True)
        length_products = len(products)
        export_to_text_file(None, None, filename, True)
        pbar = (products)
        stat = {'total': 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for p in pbar:
            start_time = time.time()
            itemid = p['itemid']
            shopid = p['shopid']
            shopname = p['shop_name']
            reviews = []
            if ratetypes != None and ratetypes != []:
                for t in ratetypes:
                    reviews += self.get_all_reviews(itemid,
                                                    shopid,
                                                    min_len_cmt=min_len_cmt,
                                                    type=t)
            else:
                reviews += self.get_all_reviews(itemid,
                                                shopid,
                                                min_len_cmt=min_len_cmt)
            export_to_text_file(array_of_json=reviews,
                                product_info=p,
                                filename=filename)
            length_products -= 1
            # pbar.set_description(

            print(
                'Đã thu thập và ghi {} đánh giá của sản phẩm {} tại shop \"{}\". Còn {} sản phẩm nữa'
                .format(len(reviews), itemid, shopname, length_products))

            stat['total'] += len(reviews)
            for r in reviews:
                stat[r['rating_star']] += 1
        print('Thống kê số lượng đánh giá ghi nhận:')
        for k, v in stat.items():
            print('{}*: {} reviews'.format(k, v))