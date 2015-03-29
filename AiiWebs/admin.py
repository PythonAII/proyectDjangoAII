from django.contrib import admin
from models import Tienda, Game
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informacion', {'fields': ['name', 'description', 'image', 'format', 'url']})
    ]

    list_display = ('__unicode__', 'name', 'url', 'description')
    list_filter = ['name']


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Juegos', {'fields': ['name', 'description', 'image', 'format_image', 'url',  'console', 'category',
                               'price_now', 'price_old', 'release_date', 'pub_date', 'format_game']})
    ]
    list_display = ('__unicode__', 'console', 'category', 'format_game', 'price_now')
    list_filter = ['console', 'category', 'format_game', 'price_now', 'release_date']


admin.site.register(Tienda, ShopAdmin)
admin.site.register(Game, GameAdmin)
