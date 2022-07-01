import imp
from django.shortcuts import render, redirect#, HttpResponse, get_object_or_404
from django.forms.models import model_to_dict
from .models import remoteModel
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.timezone import make_aware, datetime
import pytz
from time import sleep
import paramiko
import threading
from threading import Timer

class remoteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = remoteModel
        fields = '__all__'


class remoteModelViewSets(viewsets.ModelViewSet):
    queryset = remoteModel.objects.all()
    serializer_class = remoteModelSerializer


@api_view(["GET"])
def getDeatils(request):
    servers = remoteModel.objects.all()
    serilaizer = remoteModelSerializer(servers, many=True)
    return Response(serilaizer.data)


@api_view(["GET"])
def updateStatus(request, rName):
    print(f'Update for {rName} requested....')
    serilaizer = remoteModelSerializer(refreshServerStatus(rName))
    return Response(serilaizer.data)



class sshClient():
    def __init__(self) -> None:
        self.client = paramiko.SSHClient()
        self.client._policy = paramiko.WarningPolicy()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    def checkStatus(self, remoteDetails:remoteModel)-> str:
        # print(remoteDetails)
        self.client.connect(
            remoteDetails.remoteIP,
            remoteDetails.remotePORT,
            remoteDetails.username,
            remoteDetails.password,
        )   
        a,b,c = self.client.exec_command(remoteDetails.remoteCommand)
        
        b.channel.recv_exit_status()

        # for i in b.readlines(): print(i,end='')
        # for now don't handle the error
        for i in c.readlines(): print(i,end='')
        output = b.read().decode('ascii')
        self.client.close()

        return output#.strip()

mySSHclient = sshClient()


def refreshServerStatus(rName)-> None:
    print(f'[{datetime.now():%d-%b-%Y %I:%M:%S %p}] Updating info for {rName}')
    obj = remoteModel.objects.get(remoteName=rName)

    stat  = mySSHclient.checkStatus(obj)
    obj.remoteStatus = stat

    # WARNING: be carefull about the datetime timezone issue
    # obj.lastUpdated = datetime.now(pytz.timezone('Asia/Kolkata') )
    # obj.lastUpdated = datetime.now() + timedelta(minutes=330)
    obj.lastUpdated = make_aware(datetime.now(), pytz.timezone('Asia/Kolkata'))
    obj.save()

def getServersNames():
    return [[n.remoteName,n.remoteType=='workstation'] for n in remoteModel.objects.all()]



def detail(request, rName):
    # get details for a single server 
    # print(request.META.get('REMOTE_ADDR'))
    return render(request, 'index.html',{
        'server':getServersNames(),
        'data':remoteModel.objects.get(remoteName=rName),
        'selected':rName
    }) 


def refresh(request,rName):
    refreshServerStatus(rName)
    return redirect('detail',rName=rName)



def index(request):
    # handle index if no server name is availabale, for now just return frst index
    return redirect('detail',rName=getServersNames()[0][0])


# def sampleJob():
#     # running the job periodically
#     # NOTE: one should use djang channels/websockets to run background periodic tasks, but for this 
#     # simple job here, we can just a thread
#     # WARNING: this thread approach won't work with most production server e.g. gunicorn etc.
#     while True:
#         sleep(60*60*5) 

#         # run all the ssh queryies  # experimental
#         for ser in remoteModel.objects.all():
#             try:
#                 refreshServerStatus(ser.remoteName)
#             except Exception as e:
#                 print(ser,e)
# threading.Thread(target=sampleJob,daemon=True).start()


def refreshJob():
    # run all the ssh queryies  # experimental
    for ser in remoteModel.objects.all():
        try:
            refreshServerStatus(ser.remoteName)
        except Exception as e:
            print(ser,e)


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


RepeatTimer(60*60*5, refreshJob).start()