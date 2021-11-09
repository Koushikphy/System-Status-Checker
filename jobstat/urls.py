from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers


admin.site.site_header = 'Job Status Admin Panel'

urlpatterns = [
    # home page route
    url(r'^$',views.index, name='home'),
    path(r'home/<str:pk>',views.detail, name='detail'),
    path(r'refresh/<str:pk>',views.refresh, name='refresh'),

]
