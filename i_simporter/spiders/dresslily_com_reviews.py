import scrapy, csv, json, time, math
from scrapy.crawler import CrawlerProcess
from i_simporter.i_simporter.spiders.locators import Locators
from i_simporter.i_simporter.items import DresslilyComViewsItem


class DresslilyComReviewsSpider(scrapy.Spider):
    name = 'dresslily_com_reviews'

    with open('../../iii_results/dresslily_com_urls.csv') as f:
        reader = csv.reader(f)
        url_list = []
        for line in reader:
            url_list.append(*line)

    start_urls = url_list[1:2]

    custom_settings = {
        'FEED_EXPORT_BATCH_ITEM_COUNT': 100,
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../../iii_results/ii_reviews/%(batch_id)02d-dresslily_com_reviews1.csv',
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
        items = DresslilyComViewsItem()

        reviews_amount = response.xpath(Locators.TOTAL_REVIEWS).get()
        pages_amount = math.ceil(int(reviews_amount)/4)
        goods_id = response.url.split('product')[1].replace('.html', '')
        if reviews_amount is not None:
            global product_id
            product_id = response.xpath(Locators.PRODUCT_ID).get()
            reviews = response.xpath(Locators.REVIEWS)
            print(len(reviews))
            for review in reviews:
                rating = len(review.xpath(Locators.RATING).getall())
                timestamp = int(time.mktime(time.strptime(review.xpath(Locators.TIMESTAMP).get(), '%b,%d %Y %H:%M:%S')))
                text = review.xpath(Locators.TEXT).get()
                size = review.xpath(Locators.SIZE).get().split(': ')[1]
                color = review.xpath(Locators.COLOR).get().split(': ')[1]

                items['product_id'] = product_id
                items['rating'] = rating
                items['timestamp'] = timestamp
                items['text'] = text
                items['size'] = size
                items['color'] = color

                yield items

            if pages_amount > 1:
                for page in range(2, pages_amount+1):
                    items['product_id'] = product_id
                    url = f'https://www.dresslily.com/m-review-a-view_review_list-goods_id-{goods_id}-page-{page}?odr=0'
                    yield scrapy.Request(url, callback=self.parse_reviews, headers=self.headers)

    @staticmethod
    def parse_reviews(response):
        items = DresslilyComViewsItem()

        data = json.loads(response.body)
        for i in data['data']['review']['review_list']:
            rating = i['rate_overall']
            timestamp = int(time.mktime(time.strptime(i['adddate'], '%b,%d %Y %H:%M:%S')))
            text = i['pros']
            size = i['goods']['size']
            color = i['goods']['color']

            items['product_id'] = product_id
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
