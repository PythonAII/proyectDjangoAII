import requests
import threading


class ManageUrl():
    def __init__(self, urls=None, thread=False):
        self.finish = []
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
        if not shop or not shop.active:
            pass #error
        Retriever = dict_retriever['retriever']
        request = requests.get(url)
        if request.status_code is not 200:
            pass # Error
        response = request.text
        retriever = Retriever(url, response)
        context['product'], context['imgs'] = retriever.parse_detail_url()
        self.context.append(context)
        if index:
            self.finish.insert(index, True)
        else:
            self.finish.append(True)

    def manage(self, urls):
        for index, url in enumerate(urls):
            thread = threading.Thread(target=self.check_product, args=(url, index))
            self.threads.append(thread)
            thread.setDaemon(True)
            thread.start()
