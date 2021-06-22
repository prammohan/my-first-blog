from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Bet, GroupStagePicks 
from .models import GroupStagePicks
#from .models import Choice 
import re
import calendar
from calendar import HTMLCalendar

def index(request):
    latest_bet_list = Bet.objects.all()
    #template = loader.get_template('euro21/index.html')
    #group_a = Group(title = 'Group A', countries = ['as', 'of'])
    #group_all = Group(countries = [['me', 'you'],['as', 'of']])
    latest_group_picks = GroupStagePicks.objects.all()
    cal = HTMLCalendar().formatmonth(2021, 6)

    picks["Evgueni"] = ["India", "Argentina", "Ghana", "Cyprus"]
    picks["Ram"] = ["Argentina", "India", "Ghana", "Cyprus"]
    picks["Actual"] = ["Argentina", "India", "Ghana", "Cyprus"]
    
    c = GroupStagePicks()
    c.group = "E"
    c.name = "Evgueni"
    c.pick = "Brazil"
    c.position = 1
    c.save
    #d = GroupStagePicks ()
    c.group = "E"
    c.name = "Ram"
    c.pick = "Wales"
    c.position = 2
    c.save()

    
    context = {
        'latest_bet_list': latest_bet_list,
        'latest_group_picks': latest_group_picks,
        #'group_a_title': group_a.title,
        #'group_a_countries': group_a.countries,
    #    'group_countries': group_all.countries,
    #    'group_picks': player_picks
        'cal': cal,
    }
    return render(request, 'euro21/index.html', context)
    #return HttpResponse(template.render(context, request))
    #return HttpResponse(latest_bet_list)

#def list_groups(request):
#    group_a = Group(title = 'Group A', first='as', second='vbf', third='geg', fourth='gth')
#    template = loader.get_template('euro21/index.html')

def detail(request, group_id):
    #latest_choice_list = Choice.objects.all()
    #template = loader.get_template('euro21/detail.html')
    #context = {
    #    'latest_choice_list': latest_choice_list,
    #}
    #return render(request, 'euro21/detail.html', context)
    return HttpResponse("You're looking at group %s." % group_id)

def results(request):
    response = "You're looking at the results of Your picks"
    myname  = table
    return HttpResponse(response)

