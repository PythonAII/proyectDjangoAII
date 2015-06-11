from ...base import ProductRetriever
from product.models import GameCategory
from product import DICT_STOCK, DICT_CATEGORY


class XtralifeShopRetriever(ProductRetriever):

    def parse_detail_url(self):
        prod_info = self.soup.find('div', 'content')
        blockfiles = prod_info.find('div', 'fichaCabeceraRight')

        self.__parse_price_product(blockfiles)
        self.__parse_product_info(prod_info)
        self.product_info['description'] = prod_info.find('div', 'fichaDescripcion').getText()
        return self.product_info, self.__parse_imgs(prod_info)

    def __parse_product_info(self, prod_info):
        self.product_info['title'] = prod_info.find('h1', 'nombre_ficha').text.replace(':', '').lower()
        image = prod_info.find('div', 'fichaCabeceraLeft').find_all('img')
        if len(image) is 1:
            self.product_info['src'] = image[0]['src']
        else:
            for values in image:
                if 'portada' in values['src']:
                    self.product_info['src'] = values['src']

        self.product_info['platform'] = self._get_code_console(prod_info('li', 'ui-state-active')[0].text.lower())

        self.product_info['date'] = self._get_date(prod_info.find('div', 'lanz_ficha')
                                                   .text.replace('\t', '').replace('\n', ''))
        categories = [category.text.lower() for category in
                      prod_info.find('span', 'subcategories').find_all('a')]
        self.product_info['category'] = self._get_code_by(categories, GameCategory, DICT_CATEGORY)
        self.product_info['stock'] = 3

    def __parse_price_product(self, prices):
        self.product_info['prices'], self.product_info['price_sale'] = \
            self._parse_price([prices.find('script').text, prices.find('p', 'precio_ficha').text])

    def __parse_imgs(self, imgs):
        list_img = imgs.find('div', 'foto_petites')
        if list_img:
            return [img['href'] for img in list_img.find_all('a')]
        return None
