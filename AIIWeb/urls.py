from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('AiiWebs.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^create/$', 'admin', name='create'),
    url(r'^create/report/$', 'function_in_view', name='form_create_product'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()