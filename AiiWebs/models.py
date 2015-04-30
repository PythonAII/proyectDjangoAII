#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from choice import FORMAT_CHOICE, CONSOLE_CHOICE, CATEGORY_CHOICE
from util import upload_image_game, upload_image_brand
from product.base import ProductRetrieverUrl


# Create your models here.
class Shop(models.Model):

    name = models.CharField(max_length=100, verbose_name=_(u'Nombre'))
    description = models.TextField(max_length=400, verbose_name=_(u'Descipción'))
    url = models.TextField(max_length=700, verbose_name=_(u'Url'))
    activate = models.BooleanField(verbose_name=_(u'Activado'))

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
    price_old = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Antiguo'))
    price_now = models.DecimalField(decimal_places=2, max_digits=5, verbose_name=_(u'Precio Actual'))

    class Meta:
        verbose_name = _(u'Precio')
        verbose_name_plural = _(u'Precios')
        ordering = ["shop", "price_now", "price_old"]

    def __unicode__(self):
        return u'%s - (%s, %s)' % (self.shop, self.price_old, self.price_now)


class Game(models.Model):

    name = models.CharField(max_length=100, verbose_name=_(_(u'Nombre')))
    description = models.TextField(max_length=400, verbose_name=_(u'Descipción'))
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=400, verbose_name=_(u'Categoria'))
    console = models.CharField(choices=CONSOLE_CHOICE, max_length=200, verbose_name=_(u'Plataforma'))
    release_date = models.DateTimeField(verbose_name=_(u'Fecha de lanzamiento'), blank=True, null=True)
    prices = models.ManyToManyField(PricesGame, verbose_name=_(u'recommended Price'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'Juego')
        verbose_name_plural = _(u'Juegos')
        ordering = ['name', 'console', 'category', 'release_date']

    def __unicode__(self):
        return u'%s - %s | %s' % (self.name, self.category, self.console)
