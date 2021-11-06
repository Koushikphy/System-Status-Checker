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


servers = [
    'bijit',
    'netweb'
]

details =[
    {
        'name': 'bijit',
        'username':'bijit',
        'ip':'192.168.31.83',
        'password':'abc123',
        'lastrefreshed': 'bibibibibib',
        'status':'''
Memory Usage: 9804/64039MB (15.31%)
CPU Usage:    41.4%
---------------------------------------------------------------------------
   PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
215140 koushik   20   0   18.3g   4.5g  11732 R  1189  7.1   3267:59 abc.exe
152261 koushik   20   0   16.0g   2.1g  11688 R 100.0  3.4  19163:04 abc.exe
227551 saikat    20   0 1802964 441748   9300 R 100.0  0.7  21:50.33 molpro.exe
227287 saikat    20   0 1802976 452060   9300 R  94.4  0.7  21:54.05 molpro.exe
227378 saikat    20   0 1802968 460088   9296 R  94.4  0.7  21:48.07 molpro.exe
227466 saikat    20   0 1802968 445276   9296 R  94.4  0.7  21:51.23 molpro.exe
215140 koushik   20   0   18.3g   4.5g  11732 R  1189  7.1   3267:59 abc.exe
152261 koushik   20   0   16.0g   2.1g  11688 R 100.0  3.4  19163:04 abc.exe
227551 saikat    20   0 1802964 441748   9300 R 100.0  0.7  21:50.33 molpro.exe
227287 saikat    20   0 1802976 452060   9300 R  94.4  0.7  21:54.05 molpro.exe
227378 saikat    20   0 1802968 460088   9296 R  94.4  0.7  21:48.07 molpro.exe
227466 saikat    20   0 1802968 445276   9296 R  94.4  0.7  21:51.23 molpro.exe
215140 koushik   20   0   18.3g   4.5g  11732 R  1189  7.1   3267:59 abc.exe
152261 koushik   20   0   16.0g   2.1g  11688 R 100.0  3.4  19163:04 abc.exe
227551 saikat    20   0 1802964 441748   9300 R 100.0  0.7  21:50.33 molpro.exe
227287 saikat    20   0 1802976 452060   9300 R  94.4  0.7  21:54.05 molpro.exe
227378 saikat    20   0 1802968 460088   9296 R  94.4  0.7  21:48.07 molpro.exe
227466 saikat    20   0 1802968 445276   9296 R  94.4  0.7  21:51.23 molpro.exe
215140 koushik   20   0   18.3g   4.5g  11732 R  1189  7.1   3267:59 abc.exe
152261 koushik   20   0   16.0g   2.1g  11688 R 100.0  3.4  19163:04 abc.exe
227551 saikat    20   0 1802964 441748   9300 R 100.0  0.7  21:50.33 molpro.exe
227287 saikat    20   0 1802976 452060   9300 R  94.4  0.7  21:54.05 molpro.exe
227378 saikat    20   0 1802968 460088   9296 R  94.4  0.7  21:48.07 molpro.exe
227466 saikat    20   0 1802968 445276   9296 R  94.4  0.7  21:51.23 molpro.exe
        '''
        
    },
    {
        'name': 'netweb',
        'username':'satrajit',
        'ip':'192.168.31.88',
        'password':'abc123',
        'lastrefreshed': 'fhqiofhqw',
        'status':'''
Memory Usage: 4427/64039MB (6.91%)
CPU Usage:    30.7%
---------------------------------------------------------------------------
   PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
180980 koushik   20   0   16.8g   3.1g  11836 R 835.3  4.9   4456:13 abc.exe
        '''
    }
]

# Create your views here.
def detail(request, pk):
    # print(pk)
    return render(request, 'index.html',{
        'server':servers,
        'data':details[pk],
        'selected':pk
    }) 


def refresh(request,pk):
    # do the update
    # print('redirect',pk)
    return redirect('detail',pk=pk)

def index(request):
    return redirect('detail',pk=0)
    # return render(request, 'index.html',{
    #     'server':servers,
    #     'data':details[0],
    #     'selected':0
    # })
