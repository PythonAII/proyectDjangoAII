import ast
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from product.models import Game, GameCategory
from product import CONSOLE_CHOICE


class GameUserQuerySet(models.query.QuerySet):
    def users(self):
        return self.exclude(is_staff=False)

    def is_staff(self, name):
        return self.get(name=name).is_staff


class GameUserManager(models.Manager):

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)

    def get_query_set(self):
        return GameUserQuerySet(self.model)

class GameUser(User):
    visited_games = models.ManyToManyField(Game, verbose_name=_(u'Juegos Visitados'),
                                           related_name=_(u'Juegos Visitados'), null=True)
    category_visited = models.ManyToManyField(GameCategory, verbose_name=_(u'Categoria visitadas'), null=True)
    favorite_console = models.IntegerField(choices=CONSOLE_CHOICE, max_length=100, verbose_name=_(u'Consola favorita'))
    consoles_visited = models.ManyToManyField(Game, verbose_name=_(u'consola Visitados'),
                                              related_name=_(u'consola Visitados'), null=True)
    objects = GameUserManager()

    class Meta:
        verbose_name = _(u'Usuario')
        verbose_name_plural = _(u'Usuarios')
        ordering = ['username', 'date_joined', 'favorite_console']

    def __unicode__(self):
        return u'Usuario: %s \nFecha de ingreso: %s' % (self.username, self.date_joined)