# Shopee Reviews Crawler

This is a crawler to crawl reviews from Shopee, to modify the country, you can change the country code in `country` variable in `crawler/config.yml`.

## Install dependencies

```bash
pip install -r requirements.txt
```

## Usage


```python
from crawler.collector import Collector

c = Collector()
c.collect_reviews_product('sentiments.txt', max_products=10)
```


## Acknowledgements
This repository is the refactored version of [Shopee Reviews Crawler](https://github.com/quocthang0507/GetShopeeReviews)