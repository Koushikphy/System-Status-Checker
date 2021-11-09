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
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.utils import timezone
from rest_framework import filters
from .models import remoteModel
import paramiko

from django.forms.models import model_to_dict
import pytz



class sshClient():
    
    def __init__(self) -> None:
        self.client = paramiko.SSHClient()
        self.client._policy = paramiko.WarningPolicy()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def runCommand(self, remoteDetails):
        # print(remoteDetails)
        self.client.connect(
            remoteDetails['remoteIP'],
            remoteDetails['remotePORT'],
            remoteDetails['username'],
            remoteDetails['password'],
        )   

        a,b,c = self.client.exec_command(remoteDetails['remoteCommand'])
        
        b.channel.recv_exit_status()

        # for i in b.readlines(): print(i,end='')
        # for now don't handle the error
        for i in c.readlines(): print(i,end='')
        output = b.read().decode('ascii')
        self.client.close()

        return output.strip()

mySSHclient = sshClient()
    

def getServersNames():
    return [n for n, in remoteModel.objects.values_list('remoteName')]



# Create your views here.
def detail(request, rName):
    print(request.META.get('REMOTE_ADDR'))
    return render(request, 'index.html',{
        'server':getServersNames(),
        'data':remoteModel.objects.get(remoteName=rName),
        'selected':rName
    }) 



def refresh(request,rName):
    obj = remoteModel.objects.get(remoteName=rName)
    stat  = mySSHclient.runCommand(
        model_to_dict(obj)
    )
    obj.remoteStatus = stat

    # be carefull about the datetime timezone issue
    # obj.lastUpdated = datetime.now(pytz.timezone('Asia/Kolkata') )
    obj.lastUpdated = datetime.now() + timedelta(minutes=330)
    # print()
    # print(datetime.now(pytz.timezone('Asia/Kolkata') ))
    # print(obj.lastUpdated)
    # print()

    obj.save()
    return redirect('detail',rName=rName)



def index(request):
    # handle index if no server name is availabale, for now just return frst index

    return redirect('detail',rName=getServersNames()[0])
