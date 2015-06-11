from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('AiiWebs.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^create/$', 'admin', name='create'),
    url(r'^create/report/$', 'function_in_view', name='form_create_product'),
    url(r'^loggin/$', 'check_login', name='login'),
    url(r'^loggout/$', 'logout_loggin', name='logout'),
    url(r'^register/$', 'register_user', name='register_user'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('product.views',
    url(r'product/category=(?P<category>(\w+))/', 'get_page_by_category', name='page_category'),
    url(r'product/console=(?P<console>(\w+))', 'get_page_by_console', name='menubar_console'),
    url(r'product/game=(?P<game>(\w+))', 'get_product_game', name='product_game'),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)),)
urlpatterns += staticfiles_urlpatterns()
urlpatterns +=  patterns('',
               (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
              )