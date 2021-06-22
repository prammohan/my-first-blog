from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django import forms


# Create your models here.
class Bet(models.Model):
    bet_text = models.CharField(max_length=200)

class GroupStagePicks(models.Model):
    group = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    pick = models.CharField(max_length=20, blank="true")
    position = models.IntegerField(default=0)