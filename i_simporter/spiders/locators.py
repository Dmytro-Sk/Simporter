class Locators:

    """Urls"""

    # main locators

    # additional locators
    URLS = '(//div[@class="category-right-part clearfix"]//div[@class="category-list js-category"]/div/div)/a[1]/@href'
    ITEM_PAGES = '//div[@class="category-header"]//div[@class="site-pager-pad-pc site-pager"]/ul/li[position()>2]/a/@href'

    """Products"""

    # main locators
    PRODUCT_ID = '//div[@class="path"]//em[@class="sku-show"]/text()'
    NAME = '//div[@class="good-hgap good-basic-info"]//span[@class="goodtitle"]/text()'
    DISCOUNT = '//div[@class="good-hgap good-basic-info"]//div[@class="goodprice-line-start"]/span[3]/span'
    DISCOUNTED_PRICE = '//div[@class="good-hgap good-basic-info"]//div[@class="goodprice-line-start"]/span[1]/span'
    ORIGINAL_PRICE = '//div[@class="good-hgap good-basic-info"]//div[@class="goodprice-line-start"]/span[2]/span[2]'
    TOTAL_REVIEWS = '//*[@id="js_reviewCountText"]/text()'
    PRODUCT_INFO = '//div[@class="good-hgap good-basic-info"]//div[@class="good-desc-container"]//div[@class="xxkkk20"]//text()'

    # additional locators
    PRODUCT_URLS = '//div[@class="category-list js-category"]//a[@class="js-picture js_logsss_click_delegate_ps twoimgtip category-good-picture-link"]'

    """Reviews"""

    # main locators
    RATING = './/p[@class="starscon_b dib"]/i[@class="icon-star-black"]'
    TIMESTAMP = './/span[@class="reviewtime"]/text()'
    TEXT = './/p[@class="reviewcon"]/text()'
    SIZE = './/p[@class="color-size"]/span[1]/text()'
    COLOR = './/p[@class="color-size"]/span[2]/text()'

    # additional locators
    REVIEWS = '//div[@class="reviewwrap"]/div[@class="reviewlist clearfix"]'
    COMMENT_PAGES = '//*[@id="js_reviewPager"]/ul/li[last()-1]/a'
    NEXT_BUTTON = '//*[@id="js_reviewPager"]/ul/li[last()]/a'
    TIMESTAMP1 = './/span[@class="reviewtime"]'
    TEXT1 = './/p[@class="reviewcon"]'
    SIZE1 = './/p[@class="color-size"]/span[1]'
    COLOR1 = './/p[@class="color-size"]/span[2]'
