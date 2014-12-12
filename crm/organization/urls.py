
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from organization.views import *
from organization import views

urlpatterns = patterns('',
    #lang
    #url(r'^i18n/', include('django.conf.urls.i18n')),
    # Org
    url(r'^$', login_required(OrgList.as_view()), name='home'),
    url(r'^search/$', OrgCreate.as_view(), name='search'),
    url(r'^(?P<pk>\d+)/$', OrgUpdate.as_view(), name='org_update'),
    url(r'^profile/(?P<pk>\d+)/$', OrgProfileUpdate.as_view(),
            name='orgprofile_update'),
    url(r'^list/$',OrgList.as_view(), name='org_list_all'),

    url(r'^list/(?P<scope>\w+)/$', OrgList.as_view(), name='org_list'),

    url(r'^delete/(?P<pk>\d+)/$', OrgDelete.as_view(), name='org_del'),

    url(r'^add/$', OrgCreate.as_view(success_url="/org/list/all"),
            name='org_add'),
    url(r'^details/(?P<org_id>\d+)$', 'organization.views.org_details', name='org_details'),

    # Org type
    url(r'^orgtype/add/$', OrgTypeCreate.as_view(), name='orgtype_add'),
    url(r'^orgtype/(?P<pk>\d+)/$', OrgTypeUpdate.as_view(), name='orgtype_update'),
    url(r'^orgtype/list/$', OrgTypeList.as_view(), name='orgtype_list'),
    url(r'^orgtype/delete/(?P<pk>\d+)$', OrgTypeDelete.as_view(), name='orgtype_delete'),

    # Designation
    url(r'^designation/add/$', DesignationCreate.as_view(), name='designation_add'),
    url(r'^designation/delete/(?P<pk>\d+)/$', DesignationDelete.as_view(), name='designation_del'),
    url(r'^designation/(?P<pk>\d+)/$', DesignationUpdate.as_view(), name='designation_update'),
    url(r'^designation/list/$', DesignationList.as_view(), name='designation_list'),
    url(r'^designation/list/search/$', 'organization.views.autocompleteModel', name='designation_auto'),
    url(r'^designation/list/(?P<scope>\w+)/$', DesignationList.as_view(), name='designation_list_my'),

    # Admin User
    url(r'^employee/add/(?P<user_id>\d+)/$', "organization.views.employee_add", name='make_employee'),

    # User
    url(r'^user/list/$', PersonList.as_view(), name='user_list'),
    url(r'^user/add/$', UserCreate.as_view(), name='user_add'),
    url(r'^user/delete/(?P<pk>\w+)/$', UserDelete.as_view(), name='user_delete'),
    url(r'^user/details/(?P<user_id>\d+)$', 'organization.views.user_details', name='user_details'),
    url(r'^user/upload/', 'organization.views.user_upload', name='user_upload'),
    url(r'^user/(?P<pk>\d+)/$', UserUpdate.as_view(), name='user_update'),
    #url(r'^user/(?P<pk>\d+)/$', "organization.views.Userupdate", name='user_update'),

   # url(r'^user/profile/)$', my_contact_page, name='profupdate'),
    url(r'^user/profile/$', my_contact_page.as_view(), name='profupdate'),

    # Visiting Cards
    url(r'^vcard/list/$', VCardList.as_view(), name='vcard_list'),
    #url(r'^vcard/add/$', VCardCreate.as_view(), name='vcard_add'),
    url(r'^vcard/(?P<pk>\w+)/$', VCardUpdate.as_view(), name='vcard_update'),
    #url(r'^vcard/(?P<pk>\w+)/$', 'organization.views.VCardUpdate', name='vcard_update'),
    url(r'^vcard/delete/(?P<pk>\w+)/$', VCardDelete.as_view(), name='vcard_delete'),
    )
