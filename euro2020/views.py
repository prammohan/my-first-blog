from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

from .models import Bet
from .models import GroupStagePicks
#from .models import Choice 
import re
import calendar
from calendar import HTMLCalendar

def index(request):
    latest_bet_list = Bet.objects.all()
    
    group_txt = "I am screwed"

    actual_pos = {}
    actual_pos["A"] = ["India", "Argentina", "Cyprus", "DNQ"]
    actual_pos["B"] = ["Australia", "England", "Italy", "DNQ"]
    
    #Update latest standings 
    num_groups = 2
    num_players = 2
    num_teams_per_group = 4
    AllGroups = ["A", "B"]
    for i in range(num_groups):
        for j in range(num_teams_per_group):
            c = GroupStagePicks.objects.filter(name="Actual", group=AllGroups[i], position=j+1)
            c.update(pick = actual_pos[AllGroups[i]][j])

    AllPlayers = ["Evgueni", "Ram"]
    
    gp_points = [0, 0]
    acc_points = [0, 0]
    
    #if not GroupStagePicks.objects.filter(group="A").exists():
    for i in range(num_players): #players
        for j in range(num_groups): #groups
            if GroupStagePicks.objects.filter(name=AllPlayers[i], group=AllGroups[j]).exists():
                for k in range(num_teams_per_group): #picks per group
                    #print (AllPlayers[i])
                    #print (AllGroups[j])
                    #print (k)
                    
                    d = GroupStagePicks.objects.get(name=AllPlayers[i], group=AllGroups[j], position=k+1)
                    e = GroupStagePicks.objects.get(name="Actual", group=AllGroups[j], position=k+1)
                    #f = GroupStagePicks.objects.get(name="Actual", group=AllGroups[j])
                
                    #print (getattr(d, 'pick'))
                    #print (d.pick)
                    #print (e.pick)
        
                    if d.pick == e.pick:
                        #print (AllPlayers[i])
                        #print ("I'm here")

                        acc_points[i] +=2 #1 point for accuracy (position), 1 for the right team
                        gp_points[i] +=1
                    else:
                        for x in range(num_teams_per_group): #go through all the teams that have qualified in a group
                            f = GroupStagePicks.objects.get(name="Actual", group=AllGroups[j], position=x+1)
                            if d.pick == f.pick:
                                acc_points[i] +=1
                                gp_points[i] +=1

    #print ("points as follows")
    #print (gp_points[0], acc_points[0])
    #print (gp_points[1], acc_points[1])

    #creating picks compatible for html viewing -- Group A
    latest_group_picks_A0 = [""]*(num_players+1)
    latest_group_picks_A1 = [""]*(num_players+1)
    latest_group_picks_A2 = [""]*(num_players+1)
    latest_group_picks_A3 = [""]*(num_players+1)
    
    if GroupStagePicks.objects.filter(name=AllPlayers[i], group="A").exists():
        latest_group_picks_A0[0] = GroupStagePicks.objects.get(group="A", position=1, name="Actual")
        latest_group_picks_A1[0] = GroupStagePicks.objects.get(group="A", position=2, name="Actual")
        latest_group_picks_A2[0] = GroupStagePicks.objects.get(group="A", position=3, name="Actual")
        latest_group_picks_A3[0] = GroupStagePicks.objects.get(group="A", position=4, name="Actual")
        
        for i in range(num_players):
            #for j in range(num_teams_per_group):
            latest_group_picks_A0[i+1] = GroupStagePicks.objects.get(group="A", position=1, name=AllPlayers[i])
            latest_group_picks_A1[i+1] = GroupStagePicks.objects.get(group="A", position=2, name=AllPlayers[i])
            latest_group_picks_A2[i+1] = GroupStagePicks.objects.get(group="A", position=3, name=AllPlayers[i])
            latest_group_picks_A3[i+1] = GroupStagePicks.objects.get(group="A", position=4, name=AllPlayers[i])

    #creating picks compatible for html viewing -- Group B
    latest_group_picks_B0 = [""]*(num_players+1)
    latest_group_picks_B1 = [""]*(num_players+1)
    latest_group_picks_B2 = [""]*(num_players+1)
    latest_group_picks_B3 = [""]*(num_players+1)
    
    if GroupStagePicks.objects.filter(name=AllPlayers[i], group="B").exists():
        latest_group_picks_B0[0] = GroupStagePicks.objects.get(group="B", position=1, name="Actual")
        latest_group_picks_B1[0] = GroupStagePicks.objects.get(group="B", position=2, name="Actual")
        latest_group_picks_B2[0] = GroupStagePicks.objects.get(group="B", position=3, name="Actual")
        latest_group_picks_B3[0] = GroupStagePicks.objects.get(group="B", position=4, name="Actual")
        
        for i in range(num_players):
            #for j in range(num_teams_per_group):
            latest_group_picks_B0[i+1] = GroupStagePicks.objects.get(group="B", position=1, name=AllPlayers[i])
            latest_group_picks_B1[i+1] = GroupStagePicks.objects.get(group="B", position=2, name=AllPlayers[i])
            latest_group_picks_B2[i+1] = GroupStagePicks.objects.get(group="B", position=3, name=AllPlayers[i])
            latest_group_picks_B3[i+1] = GroupStagePicks.objects.get(group="B", position=4, name=AllPlayers[i])

    #print (latest_group_picks_A0)
    context = {
        'latest_bet_list': latest_bet_list,
        'latest_group_picks_A0': latest_group_picks_A0,
        'latest_group_picks_A1': latest_group_picks_A1,
        'latest_group_picks_A2': latest_group_picks_A2,
        'latest_group_picks_A3': latest_group_picks_A3,
        'latest_group_picks_B0': latest_group_picks_B0,
        'latest_group_picks_B1': latest_group_picks_B1,
        'latest_group_picks_B2': latest_group_picks_B2,
        'latest_group_picks_B3': latest_group_picks_B3,
        'group_points': gp_points,
    }
    return render(request, 'euro2020/index.html', context)
    #else:
    #    return HttpResponse("Nothing to list")