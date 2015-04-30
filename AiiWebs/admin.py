from django.contrib import admin
from models import Shop, Game, PricesGame
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Informacion', {'fields': ['name', 'description', 'url', 'activate']})
    ]

    list_display = ('__unicode__', 'name', 'activate')
    list_filter = ['name', 'activate']


class GameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Juegos', {'fields': ['name', 'console', 'category', 'description',
                               'release_date', 'prices']})
    ]
    list_display = ('__unicode__', 'name', 'console', 'category')
    list_filter = ['name', 'console', 'category', 'release_date']


class PricesAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tienda', {'fields': ['shop']}),
        ('Precio', {'fields': ['price_old', 'price_now']})
    ]

    list_display = ('__unicode__', 'shop', 'price_now', 'price_old')
    list_filter = ['shop', 'price_now']

admin.site.register(PricesGame, PricesAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Game, GameAdmin)
