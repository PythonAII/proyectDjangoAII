from product import SHOPS
from product.util import get_domain
from django.utils.importlib import import_module

COMPLEMENT_RETRIEVER = 'ShopRetriever'


class ProductRetrieverRegistry(object):

    def __init__(self):
        self.registry = {}

    def modules(self):
        """Force load of all registered entries."""
        return import_module('.sites', 'product.retriever')

    def get_for_url(self, url):
        """Return an appropiate ProductRetriever instance for the given URL."""
        domain = get_domain(url).capitalize()
        if domain is None:
            pass #Error
        self.registry['shop'] = None
        for key, shop in SHOPS.iteritems():
            if shop['name'] == domain and shop['active']:
                self.registry['shop'] = shop
                self.get_retriever(shop['name'])
                break
        self.registry['url'] = url
        return self.registry

    def get_retriever(self, shop_name):
        from ..base import ProductRetriever
        retriever = getattr(self.modules(), '%s%s' % (shop_name, COMPLEMENT_RETRIEVER))
        assert(issubclass(retriever, ProductRetriever))
        self.registry['retriever'] = retriever

registry = ProductRetrieverRegistry()
