from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from .models import remoteModel

import pytz
import paramiko
import threading
from time import sleep

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
    return [[n.remoteName,n.remoteType=='workstation'] for n in remoteModel.objects.all()]



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
    return redirect('detail',rName=getServersNames()[0][0])


# running the job periodically
# NOTE: one should use djang channels/websockets to run background periodic tasks, but for this 
# simple job here, we can just a thread
# WARNING: this thread approach won't work with most production server e.g. gunicorn etc.
def sampleJob():
    while True:
        sleep(60*30)
        print('Update triggered-----')
        print('-'*50)

        # run all the ssh queryies  # experimental
        for ser in remoteModel.objects.all():
            print('Updating %s'%ser.remoteName)
            try:
                stat  = mySSHclient.runCommand(
                    model_to_dict(ser)
                )
                ser.remoteStatus = stat

                # be carefull about the datetime timezone issue
                # obj.lastUpdated = datetime.now(pytz.timezone('Asia/Kolkata') )
                ser.lastUpdated = datetime.now() + timedelta(minutes=330)
                # print()
                # print(datetime.now(pytz.timezone('Asia/Kolkata') ))
                # print(obj.lastUpdated)
                # print()

                ser.save()
            except Exception as e:
                print(ser,e)
threading.Thread(target=sampleJob,daemon=True).start()
