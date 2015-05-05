# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from choice import FORMAT_CHOICE, CONSOLE_CHOICE, CATEGORY_CHOICE
from util import upload_image_game, upload_image_brand


# Create your models here.
class ShopQuerySet(models.query.QuerySet):
    def shops(self):
        return self.exclude(active=False)

    def is_shop(self, name):
        return self.get(name=name).active


class ShopManager(models.Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return ShopQuerySet(self.model)


class Shop(models.Model):

    name = models.CharField(max_length=100, verbose_name=_(u'Nombre'))
    description = models.TextField(max_length=400, verbose_name=_(u'Descipción'))
    url = models.TextField(max_length=700, verbose_name=_(u'Url'))
    active = models.BooleanField(verbose_name=_(u'Activado'))

    objects = ShopManager()

    def __init__(self, *args, **kwargs):
        super(Shop, self).__init__(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Tienda')
        verbose_name_plural = _(u'Tiendas')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % self.name


class PricesGame(models.Model):

    shop = models.ForeignKey(Shop, related_name='prices', verbose_name=_(u'Shop'))
    console = models.CharField(choices=CONSOLE_CHOICE, max_length=200, verbose_name=_(u'Plataforma'))
    price_old = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Antiguo'))
    price_now = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Actual'))

    class Meta:
        verbose_name = _(u'Precio')
        verbose_name_plural = _(u'Precios')
        ordering = ["shop", "price_now", "price_old"]

    def __unicode__(self):
        return u'%s - (%s, %s)' % (self.shop, self.price_old, self.price_now)


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


class Game(models.Model):

    name = models.CharField(max_length=100, verbose_name=_(_(u'Nombre')))
    description = models.TextField(max_length=3000, verbose_name=_(u'Descipción'))
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=400, verbose_name=_(u'Categoria'))
    release_date = models.DateTimeField(verbose_name=_(u'Fecha de lanzamiento'), blank=True, null=True)
    prices = models.ManyToManyField(PricesGame, verbose_name=_(u'recommended Price'), blank=True, null=True)

    objects = GameManager()

    class Meta:
        verbose_name = _(u'Juego')
        verbose_name_plural = _(u'Juegos')
        ordering = ['name', 'category', 'release_date']

    def __unicode__(self):
        return u'%s - %s | %s' % (self.name, self.category, self.release_date)
