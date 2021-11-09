from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers


admin.site.site_header = 'System Status Admin Panel'

urlpatterns = [
    # home page route
    url(r'^$',views.index, name='home'),
    path(r'home/<str:rName>',views.detail, name='detail'),
    path(r'refresh/<str:rName>',views.refresh, name='refresh'),

]
