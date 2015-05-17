# -*- coding: utf-8 -*-

from django.db import models
from AIIWeb.settings import MEDIA_ROOT
from django.utils.translation import ugettext_lazy as _

from product import CONSOLE_CHOICE, CATEGORY_CHOICE, PEGI_CHOICE, STOCK_CHOICE, DICT_CATEGORY_MODEL


# Create your models here.
class PricesQuerySet(models.query.QuerySet):
    def is_url(self, url):
        if self.get(url=url):
            return True
        else:
            return False

    def update_price(self, prices_dict):
        url = prices_dict['url']
        gift = prices_dict['gift']
        stock = prices_dict['stock']
        platform = prices_dict['platform']
        price_old, price_new = prices_dict['prices'], prices_dict['price_sale']
        price = self.get(url=url)
        price.update(stock=stock, plataform=platform, price_new=price_new, price_old=price_old, gift=gift)


class PricesManager(models.Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return PricesQuerySet(self.model)


class PricesGame(models.Model):

    shop = models.CharField(max_length=200, verbose_name=_(u'Tienda'))
    stock = models.IntegerField(choices=STOCK_CHOICE, verbose_name=_(u'Stock'))
    plataform = models.IntegerField(choices=CONSOLE_CHOICE, max_length=200, verbose_name=_(u'Plataforma'))
    price_old = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Antiguo'))
    price_now = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Actual'))
    url = models.URLField(verbose_name=_(u'url'), verify_exists=True, unique=True)
    gift = models.CharField(max_length=2000, verbose_name=_(u'Regalo'), null=True)

    objects = PricesManager()

    class Meta:
        verbose_name = _(u'Precio')
        verbose_name_plural = _(u'Precios')
        ordering = ["shop", "price_now", "price_old"]

    def add_price(self, prices_dict):
        url = prices_dict['url']
        gift = prices_dict['gift']
        stock = prices_dict['stock']
        shop = prices_dict['shop']['name'].lower()
        platform = prices_dict['platform']
        price_old, price_new = prices_dict['prices'], prices_dict['price_sale']
        self.create_price(shop, stock, platform, price_old, price_new, url, gift)

    def create_price(self, shop, stock, platform, price_old, price_new, url, gift):
        self.shop = shop
        self.stock = stock
        self.plataform = platform
        self.price_old = price_old
        self.price_now = price_new
        self.url = url
        self.gift = gift
        self.save()

    def __unicode__(self):
        return u'%s - (%s, %s) | %s' % (self.shop, self.price_old, self.price_now, self.url)


def product_image_upload_to(gameimage, filename):
    path = MEDIA_ROOT + gameimage.name.lower() + u'/'
    return path + filename[max(0, len(path) + len(filename) - 100):]


def _product_image_upload_to(gameimage, filename):
    return product_image_upload_to(gameimage, filename)


class GameImage(models.Model):
    name = models.CharField(max_length=40, verbose_name=_(u'Nombre'))
    image = models.ImageField(_(u'image'), upload_to=_product_image_upload_to,
                              height_field='height', width_field='width')
    height = models.PositiveIntegerField(_(u'height'), editable=False)
    width = models.PositiveIntegerField(_(u'width'), editable=False)

    class Meta:
        verbose_name = _(u'Imagen')
        verbose_name_plural = _(u'Imagenes')

    def save_image(self, filename, image):
        from django.core.files.base import ContentFile
        self.image.save(filename, ContentFile(image))
        self.name += u' - %s' % self.id
        self.save()

    def __unicode__(self):
        return self.name


class GameQuerySet(models.query.QuerySet):
    def get_game(self, game):
        return self.get(name=game)

    def get_prices(self, game):
        return self.get_game(game).prices

    def get_by_category(self, category):
        return self.filter(category)

    def is_game(self, game):
        return True if self.get_game(game) else False


class GameManager(models.Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return GameQuerySet(self.model)


class GameCategory(models.Model):
    name = models.IntegerField(choices=CATEGORY_CHOICE, max_length=400, verbose_name=_(u'Categoria'))

    class Meta:
        verbose_name = _(u'Categoria')
        verbose_name_plural = _(u'Categorias')
        ordering = ["name"]

    def __unicode__(self):
        return u'%s' % DICT_CATEGORY_MODEL[self.name]


class GamePegi(models.Model):
    name = models.IntegerField(choices=PEGI_CHOICE, max_length=10000, verbose_name=_(u'Clasificación'), null=True)

    class Meta:
        verbose_name = _(u'Pegi')
        verbose_name_plural = _(u'Pegi')


class Game(models.Model):

    name = models.CharField(max_length=100, verbose_name=_(u'Nombre'))
    description = models.TextField(max_length=3000, verbose_name=_(u'Descipción'))
    category = models.ManyToManyField(GameCategory, max_length=400, verbose_name=_(u'Categoria'))
    release_date = models.DateTimeField(verbose_name=_(u'Fecha de lanzamiento'), blank=True, null=True)
    prices = models.ManyToManyField(PricesGame, verbose_name=_(u'recommended Price'), blank=True, null=True)
    pegi = models.ManyToManyField(GamePegi, max_length=10000, verbose_name=_(u'Clasificación'), blank=True, null=True)
    imagen = models.ForeignKey(GameImage, verbose_name=_(u'Principal Imagen'), related_name='imagen_main',  blank=True,
                               null=True)
    imagenes = models.ManyToManyField(GameImage, verbose_name=_(u'Imagenes'), null=True)

    objects = GameManager()

    class Meta:
        verbose_name = _(u'Juego')
        verbose_name_plural = _(u'Juegos')
        ordering = ['name', 'category__name', 'release_date']

    def __unicode__(self):
        return u'%s | %s' % (self.name, self.release_date)

    def add_game(self, dict_game):
        name = dict_game['title']
        desciption = dict_game['description']
        category = dict_game['category']
        release_date = dict_game['date']
        prices = dict_game['prices']
        imagen = dict_game['imagen']
        pegi = dict_game['pegi']
        imagenes = dict_game['imagenes']
        self.name = name
        self.description = desciption
        self.release_date = release_date
        self.imagen = imagen
        self.save()
        if category:
            self.category.add(*category)
        if prices:
            self.prices.add(prices)
        if imagenes:
            self.imagenes.add(*imagenes)
        if pegi:
            self.pegi = pegi

