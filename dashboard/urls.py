from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('gitdashboard.urls')),
   
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'accounts/logout/$', 'django.contrib.auth.views.logout'),
)
