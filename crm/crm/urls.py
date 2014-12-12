from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from organization.views import *



from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.contrib.auth.views',
    # Examples:
    # url(r'^$', 'crm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/logout/$', 'logout_then_login', name="logout"),
    url(r'^accounts/password/change/$', 'password_change', {'template_name': 'change_password.html', 'post_change_redirect': '/org/list'}, name="changepwd"),
)

urlpatterns += patterns('',
    url(r'^(?:accounts/login/?$)?$', 'organization.views.custom_login',{'template_name': 'login.html'}, name="login"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^org/', include('organization.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#r'^(?:login/?$)?$'
