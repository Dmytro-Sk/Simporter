import scrapy
from .locators import Locators
from ..items import DresslilyComProductsItem
import csv
from selenium import webdriver


class DresslilyComProductsSpider(scrapy.Spider):
    name = 'dresslily_com_products'
    allowed_domains = ['dresslily.com']

    with open('../i_simporter/iii_results/dresslily_com_urls.csv') as f:
        reader = csv.reader(f)
        url_list = []
        for line in reader:
            url_list.append(*line)

    start_urls = url_list[1:]

    custom_settings = {
        'FEED_EXPORT_BATCH_ITEM_COUNT': 100,
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../i_simporter/iii_results/i_products/%(batch_id)02d-dresslily_com_products1.csv',
        'FEED_EXPORT_FIELDS': [
            'product_id',
            'product_url',
            'name',
            'discount',
            'discounted_price',
            'original_price',
            'total_reviews',
            'product_info',
        ],
    }

    def __init__(self):
        super().__init__()
        driver_path = 'e:/Installation Programs/3.2 Chrome/chromedriver/chromedriver.exe'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    def parse(self, response, **kwargs):
        items = DresslilyComProductsItem()

        self.driver.get(response.url)
        discount = self.driver.find_element_by_xpath(Locators.DISCOUNT).text
        if discount is '':
            discount = 0
            discounted_price = 0
            original_price = self.driver.find_element_by_xpath(Locators.DISCOUNTED_PRICE).text.replace('$', '')
        else:
            discounted_price = self.driver.find_element_by_xpath(Locators.DISCOUNTED_PRICE).text.replace('$', '')
            original_price = self.driver.find_element_by_xpath(Locators.ORIGINAL_PRICE).text.replace('$', '')

        product_id = response.xpath(Locators.PRODUCT_ID).get()
        product_url = response.url
        name = response.xpath(Locators.NAME).get()
        total_reviews = response.xpath(Locators.TOTAL_REVIEWS).get()
        if total_reviews is None:
            total_reviews = 0
        product_info_raw = response.xpath(Locators.PRODUCT_INFO).getall()
        product_info_new = [i.replace('\n', '').strip() for i in list(filter(lambda x: x.strip(), product_info_raw))]
        product_info_new_combined = list(zip(product_info_new[::2], product_info_new[1::2]))
        product_info = ''
        for i in product_info_new_combined:
            product_info += f"{''.join(i)};"

        items['product_id'] = product_id
        items['product_url'] = product_url
        items['name'] = name
        items['discount'] = discount
        items['discounted_price'] = discounted_price
        items['original_price'] = original_price
        items['total_reviews'] = total_reviews
        items['product_info'] = product_info

        yield items
