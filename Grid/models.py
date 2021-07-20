from django.db import models

class Response(models.Model):
    AssetName = models.CharField(max_length=100, primary_key=True)
    ##
    Password = models.CharField(max_length=50) #Secret
    Username = models.CharField(max_length=50) #Secret
    Server = models.CharField(max_length=20)
    Port = models.IntegerField(blank=True, null=True)
    ##
    IP = models.CharField(max_length=100)
    Hostname = models.CharField(max_length=100)
    MAC = models.CharField(max_length=100)
    OS = models.CharField(max_length=100)
    #Domaininfo
    Status = models.BoolField
    LastUpdated = models.TimeField