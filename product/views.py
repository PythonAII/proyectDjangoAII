from product.models import PricesGame, Game, GameImage
from AiiWebs.views import home

# Create your views here.


def get_page_by_category(request, category):
    games = Game.objects.filter(category__name=category).values('id', 'name', 'imagen')
    add_game_to_user(request.user, category=category)
    product = []
    for game in games:
        game['imagen'] = '/'.join(GameImage.objects.get(id=game['imagen']).image.url.split('/')[-4:])
        game['name'] = ' '.join([name.capitalize() for name in game['name'].split(' ')])
        product.append(game)
    return home(request, 'simple_product.html', product_simple=product)


def add_game_to_user(user, category=None, console=None, game=None):
    if not user.is_anonymous() and not user.is_staff:
        from AiiWebs.models import GameUser
        usergame = GameUser.objects.get(pk=user.pk)
        if category:
            from product.models import GameCategory
            usergame.category_visited.add(GameCategory.objects.get(pk=category))
        if console:
            from product.models import Game
            game_console = Game.objects.filter(plataform=console)
            usergame.consoles_visited.add(game_console[0])
        if game:
            from product.models import Game
            usergame.visited_games.add(Game.objects.get(pk=game))


def get_page_by_console(request, console):
    games = Game.objects.filter(plataform=console).values('id', 'name', 'imagen')
    add_game_to_user(request.user, console=console)
    product = []
    for game in games:
        game['imagen'] = '/'.join(GameImage.objects.get(id=game['imagen']).image.url.split('/')[-4:])
        game['name'] = ' '.join([name.capitalize() for name in game['name'].split(' ')])
        product.append(game)
    return home(request, 'simple_product.html', product_simple=product)


def get_product_game(request, game):
    game_product = Game.objects.get(id=game)
    add_game_to_user(request.user, game=game)
    products = Game.objects.values('name', 'description', 'release_date').get(id=game)
    products['name'] = ''.join([name.capitalize() for name in products['name'].split(' ')])
    products['description'] = products['description'].replace('.', '.<br><br>')
    products['main'] = '/'.join(game_product.imagen.image.url.split('/')[-4:])
    list_Aux = []
    for imagen in game_product.imagenes.all():
        list_Aux.append('/'.join(imagen.image.url.split('/')[-4:]))
    products['imagenes'] = list_Aux
    list_Aux = []
    for imagen in game_product.category.all():
        list_Aux.append(imagen.__unicode__())
    products['category'] = list_Aux
    list_Aux = []
    for price in game_product.prices.all():
        list_Aux.append({
            'brand': 'brand/%s.png' % price.shop,
            'name': price.shop,
            'url': price.url,
            'old': price.price_old,
            'now': price.price_now,
        })
    products['prices'] = list_Aux
    return home(request, url='game_info.html', game_info=products)
