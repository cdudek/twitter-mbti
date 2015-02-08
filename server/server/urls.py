from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'server.views.home', name='home'),
    url(r'^getfollowerpersonality/', 'server.views.handleProcess', name='home'),
    url(r'^results/', 'server.views.results', name='home'),
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
