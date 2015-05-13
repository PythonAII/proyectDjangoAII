# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from product import CONSOLE_CHOICE, CATEGORY_CHOICE, PEGI_CHOICE, STOCK_CHOICE


# Create your models here.
class PricesQuerySet(models.query.QuerySet):
    def is_url(self, url):
        if self.get(url=url):
            return True
        else:
            return False

    def update_precio(self, url, stock, plataform, price_old, price_new, gift):
        price = self.get(url=url)
        price.update(stock=stock, plataform=plataform, price_new=price_new, price_old=price_old, gift=gift)
        return price


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
    plataform = models.CharField(choices=CONSOLE_CHOICE, max_length=200, verbose_name=_(u'Plataforma'))
    price_old = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Antiguo'))
    price_now = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Actual'))
    url = models.URLField(verbose_name=_(u'url'), verify_exists=True, unique=True)
    gift = models.CharField(max_length=2000, verbose_name=_(u'Regalo'), null=True)

    objects = PricesManager()

    class Meta:
        verbose_name = _(u'Precio')
        verbose_name_plural = _(u'Precios')
        ordering = ["shop", "price_now", "price_old"]

    @classmethod
    def add_price(cls, prices_dict):
        url = prices_dict['url']
        gift = prices_dict['gift']
        stock = prices_dict['stock']
        shop = prices_dict['shop']
        plataform = prices_dict['plataform']
        price_old, price_new = prices_dict['prices']
        if cls.objects.is_url(url):
            price = cls.objects.update_price(url, stock, plataform, price_old, price_new, gift)
        else:
            price = cls.create_price(shop, stock, plataform, price_old, price_new, url, gift)
        return price

    @classmethod
    def create_price(cls, shop, stock, plataform, price_old, price_new, url, gift):
        prices = PricesGame(shop, stock, plataform, price_old, price_new, url, gift)
        prices.save()
        return prices

    def __unicode__(self):
        return u'%s - (%s, %s) | %s' % (self.shop, self.price_old, self.price_now, self.url)


def product_image_upload_to(product_id, filename):
    return u'product/imgs/%s-%s' % (product_id, filename[max(0, len(path) + len(filename) - 100):])


def _product_image_upload_to(gameimage, filename):
    return product_image_upload_to(gameimage.product_id, filename)


class GameImage(models.Model):
    image = models.ImageField(_(u'image'), upload_to=_product_image_upload_to,
                              height_field='height', width_field='width')
    height = models.PositiveIntegerField(_(u'height'), editable=False)
    width = models.PositiveIntegerField(_(u'width'), editable=False)

    class Meta:
        verbose_name = _(u'Imagen')
        verbose_name_plural = _(u'Imagenes')

    def __unicode__(self):
        return self.image.name


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
    pegi = models.ManyToManyField(GamePegi, max_length=10000, verbose_name=_(u'Clasificación'), null=True)
    imagen = models.ForeignKey(GameImage, verbose_name=_(u'Principal Imagen'), related_name='imagen_main')
    imagenes = models.ManyToManyField(GameImage, verbose_name=_(u'Imagenes'))

    objects = GameManager()

    class Meta:
        verbose_name = _(u'Juego')
        verbose_name_plural = _(u'Juegos')
        ordering = ['name', 'category__name', 'release_date']

    def __unicode__(self):
        return u'%s - %s | %s' % (self.name, self.category, self.release_date)

    @classmethod
    def add_game(cls, dict_game):
        name = dict_game['title']
        desciption = dict_game['description']
        category = dict_game['category']
        release_date = dict_game['release_date']
        prices = dict_game['prices']
        imagen = dict_game['imagen']
        pegi = dict_game['pegi']
        imagenes = dict_game['imagenes']
        if not cls.objects.exists(name=name):
            Game(name, desciption, category, release_date, prices, pegi, imagen, imagenes)