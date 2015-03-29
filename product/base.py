__author__ = 'ismael'

import re
from decimal import Decimal


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

