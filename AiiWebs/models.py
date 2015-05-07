from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from product.models import Game, GameManager, PricesGame


class GameUser(User):

    visited_games = models.ManyToManyField(Game, verbose_name=_(u'Juegos Visitados'),
                                           related_name=_(u'Juegos Visitados'), null=True)
    visited_links = models.ManyToManyField(PricesGame, verbose_name=_(u'Juegos linkeados'))
    favorite_games = models.ManyToManyField(Game, verbose_name=_(u'Juegos Favoritos'), null=True,
                                            related_name=_(u'Juegos Favoritos'))
    favorite_console = models.CharField(max_length=100, verbose_name=_(u'Consola favorita'))

    objects = GameManager()

    class Meta:
        verbose_name = _(u'Usuario')
        verbose_name_plural = _(u'Usuarios')
        ordering = ['username', 'date_joined', 'favorite_console']

    def __unicode__(self):
        return u'Usuario: %s \nFecha de ingreso: %s' % (self.username, self.date_joined)


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
