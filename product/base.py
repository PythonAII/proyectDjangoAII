import re
from decimal import Decimal
from bs4 import BeautifulSoup
from util import get_filename

class ProductRetriever(object):

    def __init__(self, url, response):
        self.url = url
        self.product_info = {
            'url': url,
        }
        self.soup = BeautifulSoup(response)

    def _parse_price(self, texts):
        s = set()
        price_re = re.compile(r'(\d+(?:([,.])\d+)*)')
        for text in texts:
            if hasattr(text, 'text'):
                text = text.text
            for match in price_re.finditer(text):
                decimal_separator = match.groups()[-1]
                if decimal_separator == u',':
                    price = match.group()
                    price = price.replace(u'.', u'')
                    price = price.replace(u',', u'.')
                elif decimal_separator == u'.':
                    price = match.group()
                    price = price.replace(u',', u'')
                else:
                    price = match.groups()[0]
                price = Decimal(price)
                if price > 0:
                    s.add(Decimal(price))
        if len(s) < 1:
            pass #Error escribirlo mas tarde
        elif len(s) > 2:
            pass #Error escribirlo mas tarde
        return max(s), min(s) if len(s) == 2 else None

    def parse_detail_url(self):
        pass


def save_product(product_info, imgs_no_downloand):
    from models import GameImage, PricesGame, Game
    import requests
    imgs_downloand = []
    if imgs_no_downloand:
        for img in imgs_no_downloand:
            filename = get_filename(img)
            request_imagen = requests.get(img)
            if request_imagen.status_code is 200:
                imgs_downloand.append(GameImage(filename, request_imagen.content))
    if 'gift' is not product_info:
        product_info['gift'] = None
    if 'stock' is not product_info:
        from product import STOCK_CHOICE
        product_info['stock'] = STOCK_CHOICE.get('reserva')
    product_info['imagenes'] = imgs_downloand if imgs_downloand else None
    if product_info['main']:
        img = product_info['main']
        filename = get_filename(img)
        request = requests.get(img)
        if request.status_code is 200:
            product_info['imagen'] = GameImage(filename, request.content )
        else:
            product_info['imagen'] = None
    prices = PricesGame.add_price(product_info)
    product_info['prices'] = prices
    game = Game.add_game(product_info)
