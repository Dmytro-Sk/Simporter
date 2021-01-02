import scrapy
from scrapy.crawler import CrawlerProcess
import csv
import json

from i_simporter.i_simporter.spiders.locators import Locators
from i_simporter.i_simporter.items import DresslilyComProductsItem


class DresslilyComProductsSpider(scrapy.Spider):
    name = 'dresslily_com_products'
    allowed_domains = ['dresslily.com']

    with open('../../iii_results/dresslily_com_urls.csv') as f:
        reader = csv.reader(f)
        url_list = []
        for line in reader:
            url_list.append(*line)

    start_urls = url_list[1:2]

    # custom_settings = {
    #     'FEED_EXPORT_BATCH_ITEM_COUNT': 100,
    #     'FEED_FORMAT': 'csv',
    #     'FEED_URI': '../../iii_results/i_products/%(batch_id)02d-dresslily_com_products1.csv',
    #     'FEED_EXPORT_FIELDS': [
    #         'product_id',
    #         'product_url',
    #         'name',
    #         'discount',
    #         'discounted_price',
    #         'original_price',
    #         'total_reviews',
    #         'product_info',
    #     ],
    # }

    headers = {
        # ':authority': 'www.dresslily.com',
        # ':method': 'POST',
        # ':path': '/ api / borrowHistoryController.php',
        # ':scheme': 'https',
        # 'accept': 'application/json, text/javascript, */*; q=0.01',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'en-US,en;q=0.9',
        # 'cache-control': 'no-cache',
        # 'content-length': '197',
        # 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'x-country-code=UA; AKAM_CLIENTID=9ed575f262123fe27191ae08e00e5e12; _gcl_au=1.1.613451023.1608894926; ADAID=2bb92448-e1af-57ee-8c73-3640c322970216088949261491608894926; aff_mss_info_bak={"bak":"bak"}; adid=160889492647148; cookie_lang=en; _fbp=fb.1.1608894926901.1261200256; od=100091608894927876e00e5e12392297; globalegrow_user_id=180008e8-ef2d-ae47-9c07-b1c0f4e0ddb8; web-push-token=messaging%2Fpermission-blocked; _pin_unauth=dWlkPU1tVTVOamd5WlRNdFpESm1ZaTAwTURnNExXRm1abVl0T0RoaFpHUXdZVFUyTVdVeg; postback_id=%7B%22cid%22:%225fe5ca6b112a2100014a74d0%22%7D; linkid=14765099; _ga=GA1.2.1409162697.1608895090; landingUrl=https://www.dresslily.com/?lkid=14765099&cid=5fe5ca6b112a2100014a74d0; aff_mss_info={"lkid":"14765099","cid":"5fe5ca6b112a2100014a74d0"}; subscribetags=1; D_SESSIONID=t3gqj666riv7q9feolt0609sa1; countryCode=UA; isMothersDayFlag=0; bizhong=USD; setbizhong=3; _ngroup=[{"tid":3,"v":[{"n":"_nlnkid","v":"14765099"}],"lt":1609591279,"ct":1609591279}]; _gid=GA1.2.713087448.1609591279; osr_landing=https%3A%2F%2Fwww.dresslily.com%2Freviews; osr_referrer=originalurl; logsss-search-fmd=mp; historyArray=378240126%40%40378240101%40%40378240102%40%40378240109%40%40234166712%40%40232911201; scarab.visitor=%221E8FB191E24EF1F4%22; __atuvc=1%7C52%2C1%7C53%2C2%7C0; WEBF_guid=2bb92448-e1af-57ee-8c73-3640c322970216088949261491608894926_1609615195; globalegrowbigdata2018_globalegrow_session_id=b3aab12d-c186-a89c-9e9d-57467d526adf; globalegrowbigdata2018_globalegrow_session_id_b3aab12d-c186-a89c-9e9d-57467d526adf=false; gb_pf=%7B%22rp%22%3A%22originalurl%22%2C%22lp%22%3A%22https%3A%2F%2Fwww.dresslily.com%2Frivet-long-sleeve-drawstring-hoodie-product8163410.html%22%2C%22wt%22%3A1609615793404%7D; WEBF_predate=1609616053; _uetsid=cfea0f704cf711eba4eea7725bd7c998; _uetvid=7d295f7046a211ebb502dd2b1ece2726; _dc_gtm_UA-34813272-1=1',
        # 'origin': 'https://www.dresslily.com',
        # 'pragma': 'no-cache',
        # 'referer': 'https://www.dresslily.com/contrast-lion-graphic-front-pocket-product8268277.html',
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    def parse(self, response, **kwargs):

        # product_id = response.xpath(Locators.PRODUCT_ID).get()
        # product_url = response.url
        # name = response.xpath(Locators.NAME).get()
        # total_reviews = response.xpath(Locators.TOTAL_REVIEWS).get()
        # if total_reviews is None:
        #     total_reviews = 0
        # product_info_raw = response.xpath(Locators.PRODUCT_INFO).getall()
        # product_info_new = [i.replace('\n', '').strip() for i in list(filter(lambda x: x.strip(), product_info_raw))]
        # product_info_new_combined = list(zip(product_info_new[::2], product_info_new[1::2]))
        # product_info = ''
        # for i in product_info_new_combined:
        #     product_info += f"{''.join(i)};"

        # url = 'https://www.dresslily.com/api/borrowHistoryController.php'
        url = 'https://www.dresslily.com/fun/ajax/index.php?_t=1609619581080&lang='
        # url = 'https://www.dresslily.com/rivet-long-sleeve-drawstring-hoodie-product8163410.html'
        yield scrapy.Request(url, callback=self.parse_prices, headers=self.headers)
                             # meta={
                             #     'product_id': product_id,
                             #     'product_url': product_url,
                             #     'name': name,
                             #     'total_reviews': total_reviews,
                             #     'product_info': product_info
                             # }
                             # )

    @staticmethod
    def parse_prices(response):
        # items = DresslilyComProductsItem()

        # data = json.loads(response.body)
        print(response.body.decode('utf-8'))

        # original_price = self.driver.find_element_by_xpath(Locators.DISCOUNTED_PRICE).text.replace('$', '')
        # discounted_price = self.driver.find_element_by_xpath(Locators.DISCOUNTED_PRICE).text.replace('$', '')
        # original_price = self.driver.find_element_by_xpath(Locators.ORIGINAL_PRICE).text.replace('$', '')
        #
        # items['product_id'] = response.meta['product_id']
        # items['product_url'] = response.meta['product_url']
        # items['name'] = response.meta['name']
        # items['discount'] = discount
        # items['discounted_price'] = discounted_price
        # items['original_price'] = original_price
        # items['total_reviews'] = response.meta['total_reviews']
        # items['product_info'] = response.meta['product_info']
        #
        # yield items


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(DresslilyComProductsSpider)
    process.start()
