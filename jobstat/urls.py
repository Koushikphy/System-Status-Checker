from django.contrib import admin
from django.urls import path, re_path
from . import views
# from django.conf.urls import url, include
from django.views.static import serve
from django.conf import settings


admin.site.site_header = 'System Status Admin Panel'


urlpatterns = [
    # home page route
    re_path(r'^$',views.index, name='home'),
    path(r'home/<str:rName>',views.detail, name='detail'),
    path(r'refresh/<str:rName>',views.refresh, name='refresh'),
    
    # API endpoints
    # get all details api
    path('api/details', views.getDeatils), 
    # request update for a particular server
    path('api/update/<str:rName>', views.updateStatus, name='updateAPI'),


]
