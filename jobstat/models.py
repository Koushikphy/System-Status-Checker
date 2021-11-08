from django.db import models

# Create your models here.



class remoteModel(models.Model):
    remoteName = models.CharField(max_length=100)
    remoteIP = models.GenericIPAddressField()
    remotePORT = models.IntegerField(default=22)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


    remoteType = models.CharField(max_length=100,choices=[
        ('workstation',"Workstation/PC"),  # 2ns one shows in the list options
        ('cluster',"Cluster"),
        ('qsubcluster',"qsubClsuter"),
    ],default="Workstation")


    remoteCommand= models.TextField(blank=True, null=True)

    remoteStatus = models.TextField(blank=True, null=True)
    lastUpdated = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.remoteName