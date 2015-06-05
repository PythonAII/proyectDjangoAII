import re
from ...base import ProductRetriever
from product.models import GameCategory, GamePegi
from product import DICT_PEGI, DICT_STOCK, DICT_CATEGORY

TAGS = [('publisher', 'publisher'), ('category', 'genre'),
        ('date', 'releaseDate'), ('stock', 'availability')]

DELETE = ['envio digital']

PRICESTAGS = ['PriceInt', 'NoPrice']

DATE_RE = re.compile(ur'(\d+)/(\d+)/(\d+)')


class TutiendadevideojuegosShopRetriever(ProductRetriever):
    def parse_detail_url(self):
        product_info = self.soup.find('div', id='pb-left-column')
        self.product_info['src'] = product_info.find('img', id='ctl00_CPH_Body_Master_img_box')['src']
        self.__parse_price_product(self.soup.find('span', 'our_price_display'))
        self.__parse_product_info(product_info)
        self.product_info['description'] = self.soup.find('div', 'yotpo')['data-description']
        return self.product_info, None

    def __parse_product_info(self, product_info):
        title = ' '.join(product_info.find('h1').text.split()[1:])
        for text in DELETE:
            if DELETE in title:
                title = title.replace(text, u'')[:-1]
        self.product_info['title'] = title
        platform = product_info.find('p', 'category_name').text.split()[-1]
        self.product_info['platform'] = self._get_code_console(platform.lower())
        date = product_info.find('div', id='short_description_content')
        self.product_info['date'] = None
        if date:
            self.product_info['date'] = self._get_date('/'.join(DATE_RE.findall(date.text)[0]))
        self.product_info['category'] = [12]
        self.product_info['stock'] = DICT_STOCK[self.product_info['stock'].lower()]

    def __parse_price_product(self, prices):
        list_price = [prices.find('span', id='ctl00_CPH_Body_Master_ProductPriceView1_Lbl_%s' % tag).getText()
                      for tag in PRICESTAGS]
        dec = prices.find('span', id='ctl00_CPH_Body_Master_ProductPriceView1_Lbl_PriceDec')
        if dec:
            list_price[0] += u'.%s' % dec.getText()
        self.product_info['prices'], self.product_info['price_sale'] = self._parse_price(list_price)

