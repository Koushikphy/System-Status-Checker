from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.utils.regex_helper import contains
from rest_framework import fields, serializers, viewsets

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view
from django.forms import ModelForm
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from knox.models import AuthToken
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
from rest_framework import filters


# Create your views here.

def index(request):
    return render(request, 'index.html')

