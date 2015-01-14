from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'operation.views.login', name='login'),
    url(r'^operation/', include('operation.urls', namespace='operation', app_name='operation')),
    #url(r'^interface/', include('operation.urls'))
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
