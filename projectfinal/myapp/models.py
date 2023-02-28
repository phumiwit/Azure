from django.db import models
from django import forms
from django.contrib.auth.models import User
from jsonfield import JSONField
# Create your models here.

class Userdata(models.Model):
    UserName = models.CharField(max_length = 20)
    FirstName = models.CharField(max_length = 20)
    LastName = models.CharField(max_length = 20)
    age = models.IntegerField()
    email = models.EmailField(max_length=254)
    date = models.DateField(auto_now_add = True)
    
    def __str__(self):
        return self.FirstName + "," + self.LastName

class Audio(models.Model):
    UserName = models.ForeignKey(User, on_delete=models.CASCADE)
    Filename = models.CharField(max_length=254)
    Genre = models.CharField(max_length=100, null=True, blank=True)
    top3_genre = models.CharField(max_length=255, null=True, blank=True)
    Value = Value = JSONField()
    

class Collection(models.Model):
    UserName = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    top3_genre = models.CharField(max_length=255, null=True, blank=True)
    audio_id = models.CharField(max_length=255)
    collectionname = models.CharField(max_length=255, null=True, blank=True)
    
    
class File(models.Model):
    UserName = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=250)
    fileurl = models.FileField(upload_to='uploads/')
    

class Valueforchart(models.Model):
    genre = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)