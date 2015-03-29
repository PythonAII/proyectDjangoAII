#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from choice import FORMAT_CHOICE, CONSOLE_CHOICE, CATEGORY_CHOICE
from util import upload_image_game, upload_image_brand


# Create your models here.
class Tienda(models.Model):

    name = models.CharField(max_length=100, verbose_name=_(_(u'Nombre')))
    description = models.TextField(max_length=400, verbose_name=_(u'Descipción'))
    image = models.ImageField(upload_to=upload_image_brand, null=True, blank=True)
    format = models.CharField(choices=FORMAT_CHOICE, max_length=100, verbose_name=_(u'Extensión'))
    url = models.TextField(max_length=700, verbose_name=_(u'Url'))

    def __init__(self, *args, **kwargs):
        super(Tienda, self).__init__(*args, **kwargs)


    class Meta:
        verbose_name = _(u'Tienda')
        verbose_name_plural = _(u'Tiendas')
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % name


class Game(models.Model):

    name = models.CharField(max_length=100, verbose_name=_(_(u'Nombre')))
    description = models.TextField(max_length=400, verbose_name=_(u'Descipción'))
    image = models.ImageField(upload_to=upload_image_game, null=True, blank=True)
    format_image = models.CharField(choices=FORMAT_CHOICE, max_length=100, verbose_name=_(u'Extensión'))
    url = models.TextField(max_length=700, verbose_name=_(u'Url'))
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=400, verbose_name=_(u'Categoria'))
    console = models.CharField(choices=CONSOLE_CHOICE, max_length=200, verbose_name=_(u'Plataforma'))
    price_now = models.IntegerField(verbose_name=_(u'Precio Actual'))
    price_old = models.IntegerField(verbose_name=_(u'Precio Antiguo'))
    release_date = models.DateTimeField(verbose_name=_(u'Fecha de lanzamiento'))
    pub_date = models.DateTimeField(verbose_name=_(u'Fecha de publicación'))
    format_game = models.BooleanField(verbose_name=_(u'Digital/Fisico'))

    class Meta:
        verbose_name = _(u'Juego')
        verbose_name_plural = _(u'Juegos')
        ordering = ['name', 'console', 'category', 'release_date']

    def __unicode__(self):
        return u'%s - %s | %s' % (self.name, self.category, self.console)