import requests
import threading
from product.base import save_product


class ManageUrl():
    def __init__(self, urls, thread=False):
        self.finish = [False for _ in xrange(0, len(urls))]
        self.context = []
        if thread:
            self.threads = list()
            self.manage(urls)
        else:
            self.check_product(urls[0])
        self.working()

    def working(self):
        while True:
            if all(self.finish):
                break

    def check_product(self, url, index=None):
        from product.retriever import registry
        context = {}
        dict_retriever = registry.get_for_url(url)
        shop = dict_retriever['shop']
        if not shop:
            pass #error
        Retriever = dict_retriever['retriever']
        request = requests.get(url)
        if request.status_code is not 200:
            pass # Error
        response = request.text
        retriever = Retriever(url, response)
        product_info, imgs = retriever.parse_detail_url()
        product_info['shop'] = shop
        context['product'], context['imgs'] = product_info, imgs
        save_product(context['product'], context['imgs'])
        self.context.append(context)
        if index:
            self.finish[index] = True
        else:
            self.finish[0] = True

    def manage(self, urls):
        for index, url in enumerate(urls):
            thread = threading.Thread(target=self.check_product, args=(url, index))
            self.threads.append(thread)
            thread.setDaemon(True)
            thread.start()
