import re
from decimal import Decimal
from bs4 import BeautifulSoup
from util import get_filename


class ProductRetriever(object):

    PLATAFORM = {
        u'ps4': 1,
        u'ps3': 2,
        u'ps2': 3,
        u'ps1': 4,
        u'xbox360': 5,
        u'xbox one': 6,
        u'wii': 7,
        u'pc': 8,
        u'ps vita': 9,
        u'psp': 10,
        u'wiiu': 11,
        u'nitendo ds': 12,
    }

    def __init__(self, url, response):
        self.url = url
        self.product_info = {
            'url': url,
        }
        self.soup = BeautifulSoup(response)

    def _get_date(self, date_string):
        from datetime import datetime
        try:
            date = datetime.strptime(date_string, u'%d/%m/%Y')
            return date
        except Exception:
            return None

    def _get_code_console(self, console):
        if console in self.PLATAFORM:
            return self.PLATAFORM[console]
        # Error

    def _get_code_by(self, list_name, model, DICT):
        list_code = []
        error = []
        for name in list_name:
            if name in DICT:
                code = model.objects.get(name=DICT[name])
                list_code.append(code)
            else:
                error.append(name)
        if error:
            pass
            # error
        return list_code

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
    prices = None
    imgs_downloand = None
    game = None
    try:
        if not Game.objects.filter(name=product_info['title']).exists():
            imgs_downloand = []
            if imgs_no_downloand:
                for img in imgs_no_downloand:
                    filename = get_filename(img)
                    request_imagen = requests.get(img)
                    if request_imagen.status_code is 200:
                        image = GameImage(name=product_info['title'])
                        image.save_image(filename, request_imagen.content)
                        imgs_downloand.append(image)
            if 'gift' not in product_info:
                product_info['gift'] = None
            if 'stock' not in product_info:
                from product import STOCK_CHOICE
                product_info['stock'] = STOCK_CHOICE.get('reserva')
            if 'pegi' not in product_info:
                product_info['pegi'] = None
            product_info['imagenes'] = imgs_downloand if imgs_downloand else None
            img = product_info['src']
            filename = get_filename(img)
            request = requests.get(img)
            if request.status_code is 200:
                image = GameImage(name=product_info['title'][:15])
                image.save_image("main." + filename.split('.')[1], request.content)
                product_info['imagen'] = image
            else:
                product_info['imagen'] = None
            prices = PricesGame()
            prices.add_price(product_info)
            product_info['prices'] = prices
            game = Game()
            game.add_game(product_info)
        else:
            prices = PricesGame()
            prices.add_price(product_info)
            game = Game.objects.get(name=product_info)
            game.prices.add(prices)
    except Exception:
        if prices:
            prices.delete()
        if 'imagen' in product_info:
            product_info['imagen'].delete()
        for imagen in imgs_downloand:
            imagen.delete()
        if game:
            game.delete()
