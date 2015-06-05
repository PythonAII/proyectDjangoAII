from django.shortcuts import render
from product.form import Multiurls, LoginForm
from product.retriever.base import ManageUrl

# Create your views here.

Error_Form = ur'Debe escribir al menos una URL'


def home(request, ):
    context['get_login'] = LoginForm()
    return render(request, 'home.html')


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