import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import json
import math
import time

from i_simporter.i_simporter.spiders.locators import Locators
from i_simporter.i_simporter.items import DresslilyComViewsItem


class DresslilyComReviewsSpider(scrapy.Spider):
    name = 'dresslily_com_reviews'

    with open('../../iii_results/dresslily_com_urls.csv') as f:
        reader = csv.reader(f)
        url_list = []
        for line in reader:
            url_list.append(*line)

    start_urls = url_list[1:]

    custom_settings = {
        'FEED_EXPORT_BATCH_ITEM_COUNT': 100,
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../../iii_results/ii_reviews/%(batch_id)02d-dresslily_com_reviews.csv',
        'FEED_EXPORT_FIELDS': [
            'product_id',
            'rating',
            'timestamp',
            'text',
            'size',
            'color',
        ],
    }

    headers = {'x-requested-with': 'XMLHttpRequest'}

    def parse(self, response, **kwargs):
        reviews_amount = response.xpath(Locators.TOTAL_REVIEWS).get()
        if reviews_amount is not None:
            pages_amount = math.ceil(int(reviews_amount) / 4)
            goods_id = response.url.split('product')[1].replace('.html', '')
            product_id = response.xpath(Locators.PRODUCT_ID).get()
            for page in range(1, pages_amount + 1):
                url = f'https://www.dresslily.com/m-review-a-view_review_list-goods_id-{goods_id}-page-{page}?odr=0'
                yield scrapy.Request(url, callback=self.parse_reviews, headers=self.headers,
                                     meta={'product_id': product_id})

    @staticmethod
    def parse_reviews(response):
        items = DresslilyComViewsItem()

        data = json.loads(response.body)
        for i in data['data']['review']['review_list']:
            rating = i['rate_overall']
            timestamp = int(time.mktime(time.strptime(i['adddate'], '%b,%d %Y %H:%M:%S')))
            text = i['pros']
            if i['goods'] is False:
                size = None
                color = None
            else:
                size = i['goods']['size']
                color = i['goods']['color']

            items['product_id'] = response.meta['product_id']
            items['rating'] = rating
            items['timestamp'] = timestamp
            items['text'] = text
            items['size'] = size
            items['color'] = color

            yield items


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(DresslilyComReviewsSpider)
    process.start()
