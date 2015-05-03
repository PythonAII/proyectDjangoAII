import threading


def create_product(url):
    from product.retriever import registry
    retrieve = registry.get_for_url(url)
    pass


class ManageUrl():
    def __init__(self, urls=None, thread=False):
        if thread:
            self.threads = list()
            self.manage(urls)
        else:
            create_product(urls[0])

    def manage(self, urls):
        for url in urls:
            thread = threading.Thread(target=create_product, args=(url,))
            self.threads.append(thread)
            thread.setDaemon(True)
            thread.start()
