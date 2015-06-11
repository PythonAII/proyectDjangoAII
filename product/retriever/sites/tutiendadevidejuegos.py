import re
from ...base import ProductRetriever
from product.models import GameCategory, GamePegi
from product import DICT_PEGI, DICT_STOCK, DICT_CATEGORY

TAGS = [('publisher', 'publisher'), ('category', 'genre'),
        ('date', 'releaseDate'), ('stock', 'availability')]

DELETE = ['envio digital']

PRICESTAGS = ['our_price_display', 'old_price_display']

DATE_RE = re.compile(ur'(\d+)/(\d+)/(\d+)')


class TutiendadevideojuegosShopRetriever(ProductRetriever):
    def parse_detail_url(self):
        product_info = self.soup.find('div', id='primary_block')
        self.product_info['src'] = product_info.find('img', id='bigpic')['src']
        self.__parse_price_product(product_info.find('div', 'price'))
        self.__parse_product_info(product_info)
        self.product_info['description'] = self.soup.find('div', id='idTab1').p.getText()
        return self.product_info, None

    def __parse_product_info(self, product_info):
        pb_left_column = product_info.find('div', id='pb-left-column')
        title = ' '.join(pb_left_column.find('h1').text.lower().split()[1:])
        self.product_info['title'] = title
        platform = pb_left_column.find('h1').text.lower().split()[0]
        self.product_info['platform'] = self._get_code_console(platform.lower())
        date = product_info.find('div', id='short_description_content')
        self.product_info['date'] = None
        if date:
            date = DATE_RE.findall(date.text)
            if date:
                self.product_info['date'] = self._get_date('/'.join(date[0]))
        self.product_info['category'] = [12]
        self.product_info['stock'] = 3

    def __parse_price_product(self, prices):
        list_price = []
        for tag in PRICESTAGS:
            price = prices.find('span', id='%s' % tag)
            if price:
                list_price.append(price.text)

        self.product_info['prices'], self.product_info['price_sale'] = self._parse_price(list_price)

