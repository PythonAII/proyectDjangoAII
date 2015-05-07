from ...base import ProductRetriever

PRICESTAGS = ['anterior_ficha texto_amarillo', 'ficha']


class XtralifeShopRetriever(ProductRetriever):

    def parse_detail_url(self):
        prod_info = self.soup.find('div', 'content')
        blockfiles = prod_info.find('div', 'fichaCabeceraRight')

        self.__parse_price_product(blockfiles)
        self.__parse_product_info(prod_info)
        self.__parse_description(prod_info)
        #self.__parse_imgs(self.soup.find('div', id='ctl00_CPH_Body_Master_CoverFlow1_tn_list'))
        return self.product_info, None

    def __parse_product_info(self, prod_info):
        list_gener = []

        self.product_info['title'] = prod_info.find('h1', 'nombre_ficha').text
        image = prod_info.find('div', 'fichaCabeceraLeft').find_all('img')
        if len(image) is 1:
            self.product_info['src'] = image[0]['src']
        else:
            for values in image:
                if 'portada' in values['src']:
                    self.product_info['src'] = values['src']

        platform = prod_info.find('div', id='tabs_dispo').find_all('li')
        for values in platform:
            self.product_info['platform'] = values.a.getText()

        self.product_info['publisher'] = prod_info.find('div', 'distribuidores_ficha').a.img['title']
        generos = prod_info.find('div', 'subcategoriesList').find_all('a')

        for value in generos:
            list_gener.append(value.getText())
        self.product_info['genero'] = list_gener

        self.product_info['date'] = None
        self.product_info['stock'] = prod_info.find('div', 'openPopupStock').getText().strip().split('\n\t')

    def __parse_price_product(self, prices):
        list_price = [prices.find('p', 'precio_%s' % tag) for tag in PRICESTAGS]
        price = [list_price[index].getText() if list_price[index] else "" for index in xrange(0, 2)]
        self.product_info['prices'], self.product_info['price_sale'] = self._parse_price(price)

    def __parse_description(self, descriptions):
        p_description = descriptions.find('div', 'fichaDescripcion')
        self.product_info['description'] = p_description.p.getText()

    def __parse_imgs(self, imgs):
        if imgs:
            list_img = imgs.find_all('a')