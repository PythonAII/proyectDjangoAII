from urlparse import urlparse
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
        from AiiWebs.models import Shop
        parsed_url = urlparse(url)
        domain = parsed_url.hostname
        domain = domain.split('.')[1] if domain.startswith('www') else domain.split('.')[0]
        if domain is None:
            pass #Error
        #shop = Shop.objects.get_shop(domain.lower())
        #if not shop:
            pass #Error
        self.get_retriever(domain.lower())
        #self.registry['shop'] = shop
        self.registry['url'] = url
        return self.registry

    def get_retriever(self, shop_name):
        from ..base import ProductRetriever
        retriever = getattr(self.modules(), '%s%s' % (shop_name.capitalize(), COMPLEMENT_RETRIEVER))
        assert(issubclass(retriever, ProductRetriever))
        self.registry['retriever'] = retriever

registry = ProductRetrieverRegistry()
