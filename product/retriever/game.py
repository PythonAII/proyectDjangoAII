__author__ = 'ismael'

from bs4 import BeautifulSoup
from ..base import ProductRetriever

TAGS = [('code', 'sku'), ('publisher', 'publisher'), ('genero', 'genre'),
        ('date', 'releaseDate'), ('stock', 'availability')]

PRICESTAGS = ['PriceInt', 'NoPrice']


class GameShopRetriever(ProductRetriever):

    def __init__(self):
        self.product_info = {}

    def _parse_detail_url(self, response, url, **kwargs):
        soup = BeautifulSoup(response.body_as_unicode())
        product_info = soup.find('div', 'big-inside-panel ponmeborde_gris')
        self.__parse_price_product(soup.find('div', id='ctl00_CPH_Body_Master_ProductPriceView1_Pnl'))
        self.__parse_product_info(product_info)
        self.__parse_description(soup.find('div', id='ficha-texto-descripcion'))
        self.__parse_imgs(soup.find('div', id='ctl00_CPH_Body_Master_CoverFlow1_tn_list'))
        return product_info, imgs

    def __parse_product_info(self, product_info):
        self.product_info['title'] = product_info.find('span', id='ctl00_CPH_Body_Master_lbl_name')
        self.product_info['img main'] = product_info.find('img', id='ctl00_CPH_Body_Master_img_box')
        platform = product_info.find('div', 'ficha-plataforma-pegi')
        self.product_info['platform'] = platform.img['src'].split('/')[-1].split('_')[-1].split('.')[0]
        product_table = product_info.find('div', 'ficha-producto-table')
        for keyTag, valueTag in TAGS:
            self.product_info[keyTag] = product_table.find('span', id='ctl00_CPH_Body_Master_lbl_%s'
                                                                      % valueTag).getText()

    def __parse_price_product(self, prices):
        list_price = [prices.find('span', id='ctl00_CPH_Body_Master_ProductPriceView1_Lbl_%s' % tag).getText()
                      for tag in PRICESTAGS]
        self.product_info['prices'], self.product_info['price_sale'] = self._parse_price(list_price)

    def __parse_description(self, descriptions):
        span_description = descriptions.find('span', id='ctl00_CPH_Body_Master_lbl_desc')
        self.product_info['description'] = span_description.getText()

    def __parse_imgs(self, imgs):
        list_img = imgs.find_all('a')

