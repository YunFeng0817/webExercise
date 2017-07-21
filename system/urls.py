from django.contrib import admin
from django.conf.urls import url
from system.views import *
urlpatterns=[
    url(r'^$|^login/$',login,name='login'),
    url(r'^login/Action/$',loginAction,name='loginAction'),
    url(r'^logout$',logoutAction,name='logout'),
    url(r'^change/$',changePassword,name='changePassword'),
    url(r'^change/Action/$',changeAction,name='changePasswordAction'),
    url(r'^change/Action/(\d{1})/$',sorted,name='sortedChange'),
    url(r'^delete/$',delete,name='delete'),
    url(r'^search/$',search,name='search'),
    url(r'^add/$',add,name='add'),
    url(r'^change/(?P<studentID>[0-9]+)/$',change,name='change'),
    url(r'^ACaction/$',ACaction,name='ACaction'),
    url(r'^divided/$',divided,name='divided'),
]