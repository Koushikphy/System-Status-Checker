from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers



urlpatterns = [
    # home page route
    url(r'^$',views.index, name='home'),




]