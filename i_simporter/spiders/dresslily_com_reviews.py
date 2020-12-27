import scrapy
from .locators import Locators
from ..items import DresslilyComViewsItem
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class DresslilyComReviewsSpider(scrapy.Spider):
    name = 'dresslily_com_reviews'
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
        'FEED_URI': '../i_simporter/iii_results/ii_reviews/%(batch_id)02d-dresslily_com_reviews.csv',
        'FEED_EXPORT_FIELDS': [
            'product_id',
            'rating',
            'timestamp',
            'text',
            'size',
            'color',
        ],
    }

    def __init__(self):
        super().__init__()
        driver_path = 'e:/Installation Programs/3.2 Chrome/chromedriver/chromedriver.exe'
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('-—incognito')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    def parse(self, response, **kwargs):
        items = DresslilyComViewsItem()

        product_id = response.xpath(Locators.PRODUCT_ID).get()

        total_reviews = response.xpath(Locators.TOTAL_REVIEWS).get()
        if total_reviews is not None:
            reviews = response.xpath(Locators.REVIEWS)
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

        self.driver.get(response.url)
        comment_pages = int(self.driver.find_element_by_xpath(Locators.COMMENT_PAGES).text)
        if comment_pages > 1:
            for _ in range(comment_pages-1):
                next_button = self.driver.find_element_by_xpath(Locators.NEXT_BUTTON)
                action = ActionChains(self.driver)
                action.move_to_element(next_button).perform()
                action.click(next_button).perform()
                time.sleep(2)
                reviews = self.driver.find_elements_by_xpath(Locators.REVIEWS)
                for review in reviews:
                    rating = len(review.find_elements_by_xpath(Locators.RATING))
                    timestamp = int(
                        time.mktime(time.strptime(
                            review.find_element_by_xpath(Locators.TIMESTAMP1).text, '%b,%d %Y %H:%M:%S')))
                    text = review.find_element_by_xpath(Locators.TEXT1).text

                    size = review.find_element_by_xpath(Locators.SIZE1).text.split(': ')[1]
                    color = review.find_element_by_xpath(Locators.COLOR1).text.split(': ')[1]

                    items['product_id'] = product_id
                    items['rating'] = rating
                    items['timestamp'] = timestamp
                    items['text'] = text
                    items['size'] = size
                    items['color'] = color

                    yield items
