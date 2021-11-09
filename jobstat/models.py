from django.db import models

# Create your models here.


commands = {
'workstation':'''
free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\\n", $3,$2,$3*100/$2 }'
top -b -n1 -p 1 | fgrep "Cpu(s)" | awk -F'id,' -v prefix="$prefix" '{ split($1, vs, ","); v=vs[length(vs)]; sub("%", "", v); printf "CPU Usage:    %s%.1f%%\\n", prefix, 100 - v }'
echo ---------------------------------------------------------------------------
top -bn1 | grep R 
''',
'cluster':'top_nodes',
'qsubcluster':'qstat'

}


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
        return self.remoteName+'_'+self.remoteType
    
    def save(self, *args, **kwargs):
        if not self.remoteCommand:
            self.remoteCommand = commands[self.remoteType]

        return super(remoteModel, self).save(*args, **kwargs)