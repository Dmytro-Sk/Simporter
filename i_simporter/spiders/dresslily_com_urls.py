import scrapy
from .locators import Locators
from ..items import DresslilyComUrlsItem


class DresslilyComUrlsSpider(scrapy.Spider):
    name = 'dresslily_com_urls'
    allowed_domains = ['dresslily.com']
    start_urls = ['https://www.dresslily.com/hoodies-c-181.html']
    custom_settings = {
        'ITEM_PIPELINES': {
            'i_simporter.pipelines.ISimporterPipeline': 300
        },
        'FEED_FORMAT': 'csv',
        'FEED_URI': '../i_simporter/iii_results/dresslily_com_urls.csv',
        'FEED_EXPORT_FIELDS': [
            'url',
        ],
    }

    def parse(self, response, **kwargs):
        items = DresslilyComUrlsItem()

        urls = response.xpath(Locators.URLS)
        for url in urls:
            url = url.get()
            items['url'] = url

            yield items

        yield from response.follow_all(xpath=Locators.ITEM_PAGES, callback=self.parse)
