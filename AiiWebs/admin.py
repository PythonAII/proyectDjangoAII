from django.contrib import admin
from product.models import Game, PricesGame, GameCategory, GameImage, GamePegi
from models import GameUser
# Register your models here.


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Juegos', {'fields': ['name', 'description', 'category', 'plataform',
                               'release_date', 'prices', 'pegi', 'imagen', 'imagenes']})
    ]
    list_display = ('__unicode__', 'name')
    list_filter = ['name', 'category__name', 'plataform', 'release_date']


class UsersAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Usuarios', {'fields': ['username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active',
                                 'is_superuser']})
    ]
    list_display = ('__unicode__', 'username', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ['username', 'is_staff', 'is_active', 'is_superuser']


class PricesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tienda', {'fields': ['shop', 'url', 'gift']}),
        ('Precio', {'fields': ['stock', 'price_old', 'price_now']})
    ]

    list_display = ('__unicode__', 'shop', 'stock', 'price_now', 'price_old')
    list_filter = ['shop', 'stock', 'price_now']

admin.site.register(PricesGame, PricesAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameUser, UsersAdmin)
admin.site.register(GameCategory)
admin.site.register(GameImage)
admin.site.register(GamePegi)