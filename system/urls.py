from django.contrib import admin
from django.conf.urls import url
from system.views import *
urlpatterns=[
    url(r'^login/$',login,name='login'),
    url(r'^login/Action/$',loginAction,name='loginAction'),
    url(r'^logout$',logoutAction,name='logout'),
    url(r'^change/$',changePassword,name='changePassword'),
    url(r'^change/Action/$',changeAction,name='changePasswordAction'),
]