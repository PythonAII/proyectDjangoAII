import re
from ...base import ProductRetriever
from product.models import GameCategory, GamePegi
from product import DICT_PEGI, DICT_STOCK, DICT_CATEGORY

TAGS = [('publisher', 'publisher'), ('category', 'genre'),
        ('date', 'releaseDate'), ('stock', 'availability')]

PRICESTAGS = ['PriceInt', 'NoPrice']

IMAGEN_RE = re.compile(ur'href="(.*?)"')


class GameShopRetriever(ProductRetriever):

    def parse_detail_url(self):
        product_info = self.soup.find('div', 'big-inside-panel ponmeborde_gris')
        self.__parse_price_product(self.soup.find('div', id='ctl00_CPH_Body_Master_ProductPriceView1_Pnl'))
        self.__parse_product_info(product_info)
        self.__parse_description(self.soup.find('div', 'ficha-texto-descripcion'))
        imgs = self.__parse_imgs()
        return self.product_info, imgs

    def __parse_product_info(self, product_info):
        self.product_info['title'] = product_info.find('span', id='ctl00_CPH_Body_Master_lbl_name').text.lower()
        self.product_info['src'] = product_info.find('img', id='ctl00_CPH_Body_Master_img_box')['src']
        platform = product_info.find('div', 'ficha-plataforma-pegi')
        self.product_info['platform'] = \
            self._get_code_console(platform.img['src'].split('/')[-1].split('_')[-1].split('.')[0].lower())
        product_table = product_info.find('div', 'ficha-producto-table')
        for keyTag, valueTag in TAGS:
            self.product_info[keyTag] = product_table.find('span', id='ctl00_CPH_Body_Master_lbl_%s'
                                                                      % valueTag).getText()

        self.product_info['date'] = self._get_date(self.product_info['date'])
        self.product_info['category'] = self._get_code_by([self.product_info['category'].lower()],
                                                          GameCategory, DICT_CATEGORY)
        self.product_info['stock'] = DICT_STOCK[self.product_info['stock'].lower()]

    def __parse_price_product(self, prices):
        list_price = [prices.find('span', id='ctl00_CPH_Body_Master_ProductPriceView1_Lbl_%s' % tag).getText()
                      for tag in PRICESTAGS]
        dec = prices.find('span', id='ctl00_CPH_Body_Master_ProductPriceView1_Lbl_PriceDec')
        if dec:
            list_price[0] += u'.%s' % dec.getText()
        self.product_info['prices'], self.product_info['price_sale'] = self._parse_price(list_price)

    def __parse_description(self, descriptions):
        span_description = descriptions.find('span', id='ctl00_CPH_Body_Master_lbl_desc')
        self.product_info['description'] = span_description.getText()

    def __parse_imgs(self):
        CHECK = u'http://media.game.es/Screenshots'
        imgs = IMAGEN_RE.findall(self.soup.getText())
        list_imgs = []
        if imgs:
            for img in imgs:
                if img.startswith(CHECK):
                    list_imgs.append(img)
            return list_imgs

