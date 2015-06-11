import itertools, random
from django.shortcuts import render
from product.form import Multiurls, LoginForm, UserRegisterForm
from product.retriever.base import ManageUrl
from product import DICT_CATEGORY_MODEL, DICT_CONSOLE_MODEL
from product.models import Game
from AiiWebs.models import GameUser
from django.contrib.auth.decorators import permission_required
# Create your views here.

Error_Form = ur'Debe escribir al menos una URL'


def home(request, url='home.html', **kwargs):
    context = {}
    if kwargs:
        context = kwargs
    if not request.user.is_authenticated():
        context['get_login'] = LoginForm()
    else:
        context['loggin'] = request.user.username
    list_console = []
    for console in Game.objects.all().values_list('plataform'):
        if console != (None,) and (DICT_CONSOLE_MODEL[console[0]], console[0]) not in list_console:
            list_console.append((DICT_CONSOLE_MODEL[console[0]], console[0]))
    list_category = []
    for category in Game.objects.all().values_list('category__name'):
        if category != (None,) and (DICT_CATEGORY_MODEL[category[0]], category[0]) not in list_category:
            list_category.append((DICT_CATEGORY_MODEL[category[0]], category[0]))
    context['consoles'] = sorted(list_console)
    context['categories'] = sorted(list_category)
    context['product_release'] = get_products_release()
    context['recomendation'] = get_recomendation(request.user)
    return render(request, url, context)


def get_recomendation(user):
    if not user.is_anonymous() and not user.is_staff:
        user = GameUser.objects.get(pk=user.pk)
        consoles_visited = list(itertools.chain(*[Game.objects.filter(plataform=game.plataform) for game in user.consoles_visited.all()]))
        games_visited = user.visited_games.all()
        category_visited = user.category_visited.all()
        consoles_visited.extend(games_visited)
        recomendation_game = []
        if category_visited:
            for category in category_visited:
                for game in consoles_visited:
                    if category in game.category.all():
                        recomendation_game.append(game)
            recomendation_game = set(recomendation_game)
        else:
            recomendation_game = set(consoles_visited)
    else:
        recomendation_game = set(Game.objects.all().order_by('?'))[:7]
    games = [{'name': game.name.capitalize(), 'id': game.pk,
                  'url': '/'.join(game.imagen.image.url.split('/')[-4:])}
                 for game in recomendation_game]
    return random.sample(games, min(len(games), 7))


def logout_loggin(request):
    from django.contrib import auth
    auth.logout(request)
    return home(request)


def check_login(request, **kwargs):
    from django.contrib import auth
    from django.contrib.auth import authenticate
    username = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user:
        auth.login(request, user)
        return home(request)
    else:
        return home(request, error_loggin='Fallo en la auntentificacion')

@permission_required('is_staff')
def admin(request, **kwargs):
    context = kwargs
    context['get_urls_products'] = Multiurls()
    return render(request, 'create/home.html', context)


def function_in_view(request):

    urls_form = Multiurls(request.GET)
    if not urls_form.is_valid():
        return admin(request, errors={'errors': Error_Form})
    urls = urls_form.data['urls'].split('\r\n')
    manage_url = ManageUrl(urls=urls, thread=len(urls) > 1)
    return admin(request, products=manage_url.context)


def register_user(request):
    if request.POST:
        from django.contrib import auth
        from django.contrib.auth import authenticate
        from AiiWebs.models import GameUser
        create_user = UserRegisterForm(request.POST)
        if create_user.is_valid() and not GameUser.objects.filter(username=request.POST['username']).exists():
            user = GameUser()
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.set_password(request.POST['password'])
            user.email = request.POST['email']
            user.favorite_console = request.POST['favorite_console']
            user.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, user)
            return home(request)
    user_form = UserRegisterForm()
    return home(request, url='register_user.html', user_form=user_form)


def get_products_release():
    games = Game.objects.all().order_by('-release_date')
    products = []
    for game in games:
        product = {
            'name': ' '.join([name.capitalize() for name in game.name.split(' ')]),
            'id': game.pk,
            'main': '/'.join(game.imagen.image.url.split('/')[-4:]),
            'prices': []
        }

        for price in game.prices.all():
            product['prices'].append({
                'brand': 'brand/%s.png' % price.shop,
                'name': price.shop.capitalize(),
                'old': price.price_old,
                'new': price.price_now,
                'id': price.pk
            })
        products.append(product)
    return products
