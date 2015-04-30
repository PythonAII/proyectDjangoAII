__author__ = 'ismael'

import re
from urlparse import urlparse
from decimal import Decimal

SHOPS = {
    'pk1': {
        'shop': 'game',
        'url': 'http://www.game.es',
        'active': True,
    },

    'pk0': {
        'shop': '',
        'url': '',
        'active': False,
    }
}


class ProductRetriever(object):
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


class ProductRetrieverUrl(object):

    def __init__(self, url):
        self.parse_url = urlparse(url)
        hostname = self.parse_url.hostname
        if hostname:
            if self.parser_url():
                self.generate_product()
        else:
            pass #Error escribirlo mas tarde

    def parser_url(self):
        check_hostname = self.parse_url.hostname
        hostname = check_hostname.split[1] if check_hostname.startswith('www') else check_hostname.split[0]
        for key, value in SHOPS.iteritems():
            if value[key].get('shop') is hostname:
                return value[key].get('active'), hostname
        return False




