from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django import forms

# Create your models here.

class Bet(models.Model):
    bet_text = models.CharField(max_length=200)
    #bet_A = models.CharField(max_length=50)
    #bet_B = models.CharField(max_length=50)

#class Group(models.Model):
    #title = models.CharField(max_length=20)
    #countries = [models.CharField(max_length=20), models.CharField(max_length=20),models.CharField(max_length=20),models.CharField(max_length=20)]
    #   countries = []
    #first = models.CharField(max_length=20)
    #second = models.CharField(max_length=20)
    #third = models.CharField(max_length=20)
    #fourth = models.CharField(max_length=20)

class GroupStagePicks(models.Model):
    group = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    pick = models.CharField(max_length=20, blank="true")
    position = models.IntegerField(default=0)
    #p2 = models.CharField(max_length=20, blank="true")
    #p3 = models.CharField(max_length=20, blank="true")
    #p4 = models.CharField(max_length=20, blank="true")