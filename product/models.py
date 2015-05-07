# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from product.choice import CONSOLE_CHOICE, CATEGORY_CHOICE


# Create your models here.

class PricesGame(models.Model):

    shop = models.CharField(max_length=200, verbose_name=_(u'Tienda'))
    console = models.CharField(choices=CONSOLE_CHOICE, max_length=200, verbose_name=_(u'Plataforma'))
    price_old = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Antiguo'))
    price_now = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Actual'))
    url = models.URLField(verbose_name=_(u'url'), verify_exists=True)
    gift = models.CharField(max_length=2000, verbose_name=_(u'Regalo'), null=True)

    class Meta:
        verbose_name = _(u'Precio')
        verbose_name_plural = _(u'Precios')
        ordering = ["shop", "price_now", "price_old"]

    def __unicode__(self):
        return u'%s - (%s, %s) | %s' % (self.shop, self.price_old, self.price_now, self.url)


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

    name = models.CharField(max_length=100, verbose_name=_(u'Nombre'))
    description = models.TextField(max_length=3000, verbose_name=_(u'Descipción'))
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=400, verbose_name=_(u'Categoria'))
    release_date = models.DateTimeField(verbose_name=_(u'Fecha de lanzamiento'), blank=True, null=True)
    prices = models.ManyToManyField(PricesGame, verbose_name=_(u'recommended Price'), blank=True, null=True)
    pegi = models.TextField(max_length=10000, verbose_name=_(u'Clasificación'), null=True)
    imgs = models.TextField(max_length=10000, verbose_name=_(u'Imagenes'))

    objects = GameManager()

    class Meta:
        verbose_name = _(u'Juego')
        verbose_name_plural = _(u'Juegos')
        ordering = ['name', 'category', 'release_date']

    def __unicode__(self):
        return u'%s - %s | %s' % (self.name, self.category, self.release_date)