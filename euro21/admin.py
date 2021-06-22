from django.contrib import admin

# Register your models here.
from .models import Bet, GroupStagePicks

admin.register(Bet, GroupStagePicks)(admin.ModelAdmin)