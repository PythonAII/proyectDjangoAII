__author__ = 'ismael'

import re
import requests
from decimal import Decimal
from urlparse import urlparse
from AiiWebs.models import Shop


class ProductRetriever(object):

    def __init__(self, url):
        self.parse_url = urlparse(url)
        self.product_info = {}

        hostname = self.parse_url.hostname
        if hostname and self.parser_url():
            self.generate_product()
        else:
            pass #Error escribirlo mas tarde

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

    def parser_url(self):
        check_hostname = self.parse_url.hostname
        hostname = check_hostname.split[1] if check_hostname.startswith('www') else check_hostname.split[0]
        if Shop.objects.shop(hostname.lower()):
            return True
        return False

    def generate_product(self):
        retriever = eval(self.parse_url.hostname.lower())
        retrieverInfo, img = retriever._parse_detail_url(self)

    def get_request(self):
        request = requests.get(self.parse_url.geturl())
        if request.status_code is 200:
            self.request = request
        else:
            pass #Error


