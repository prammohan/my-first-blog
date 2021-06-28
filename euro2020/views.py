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


    count = 0
    count +=1
    ##print (count)
    #if GroupStagePicks.DoesNotExist:
    #first time hitting run server, create the picks
    #c = GroupStagePicks()
    #c.group = "E"
    #c.name = "Evgueni"
    #c.pick = "Peru"
    #c.position = 1
    #c.save()
    #c = GroupStagePicks()
    #c.group = "E"
    #c.name = "Ram"
    #c.pick = "Argentina"
    #c.position = 2
    #c.save()


    rows, cols = (42, 4)
    picks = [[""]*cols]*rows

    name = ["Actual", "Volkan", "Evgueni", "Ramraj", "Ram", "Peter", "Fadi"]
    #Group A
    picks[0] = ["Italy", "Wales", "Switzerland", "DNQ"] #Turkey
    picks[1] = ["Turkey", "Italy", "Switzerland", "-"]
    picks[2] = ["Italy", "Turkey", "-", "-"]
    picks[3] = ["Italy", "Switzerland", "Turkey", "-"]
    picks[4] = ["Italy", "Turkey", "Switzerland", "-"]
    picks[5] = ["Turkey", "Italy", "-", "-"]
    picks[6] = ["Italy", "Switzerland", "-", "-"]
    

    #Group B
    picks[7] = ["Belgium", "Denmark", "DNQ", "DNQ"] #Finland, Russia
    picks[8] = ["Belgium", "Russia", "Denmark", "-"]
    picks[9] = ["Belgium", "Denmark", "Russia", "-"]
    picks[10] = ["Belgium", "Denmark", "Russia", "-"]
    picks[11] = ["Belgium", "Denmark", "Russia", "-"]
    picks[12] = ["Belgium", "Russia", "Denmark", "-"]
    picks[13] = ["Belgium", "Denmark", "Russia", "-"]

    #Group C
    picks[14] = ["Netherlands", "Austria", "Ukraine", "DNQ"] #North Macedonia
    picks[15] = ["Netherlands", "Ukraine", "Austria", "-"] 
    picks[16] = ["Netherlands", "Ukraine", "Austria", "-"] 
    picks[17] = ["Netherlands", "Ukraine", "Austria", "-"] 
    picks[18] = ["Netherlands", "Ukraine", "-", "-"] 
    picks[19] = ["Netherlands", "Ukraine", "-", "-"] 
    picks[20] = ["Netherlands", "Austria", "-", "-"] 

    #Group D
    picks[21] = ["England", "Croatia", "Czech Republic", "DNQ"] #Scotland
    picks[22] = ["Croatia", "England", "-", "-"]
    picks[23] = ["England", "Croatia", "-", "-"]
    picks[24] = ["England", "Croatia", "-", "-"]
    picks[25] = ["England", "Croatia", "-", "-"]
    picks[26] = ["England", "Croatia", "Czech Republic", "-"]
    picks[27] = ["England", "Croatia", "Czech Republic", "-"]

    #Group E
    picks[28] = ["Sweden", "Spain", "DNQ", "DNQ"] #Slovakia, Poland
    picks[29] = ["Spain", "Poland", "Sweden", "-"]
    picks[30] = ["Spain", "Sweden", "Poland", "-"]
    picks[31] = ["Spain", "Poland", "-", "-"]
    picks[32] = ["Spain", "Poland", "Sweden", "-"]
    picks[33] = ["Spain", "Sweden", "Poland", "-"]
    picks[34] = ["Spain", "Sweden", "Poland", "-"]

    #Group F
    picks[35] = ["France", "Germany", "Portugal", "DNQ"] #Hungary
    picks[36] = ["France", "Portugal", "-", "-"] 
    picks[37] = ["France", "Germany", "Portugal", "-"] 
    picks[38] = ["France", "Portugal", "Germany", "-"] 
    picks[39] = ["France", "Germany", "Portugal", "-"] 
    picks[40] = ["France", "Germany", "Portugal", "-"] 
    picks[41] = ["France", "Germany", "Portugal", "-"] 

    pick_num = 0

    if GroupStagePicks.objects.filter(name="Actual", group="A").exists():
        pass
    else:
        for i in range(len(picks)):
            position = 0
            for j in range(len(picks[i])):
                gsp = GroupStagePicks()
                if i < 7:
                    gsp.group = "A"
                elif i >= 7 and i < 14:
                    gsp.group = "B"
                elif i >= 14 and i < 21:
                    gsp.group = "C"
                elif i >= 21 and i < 28:
                    gsp.group = "D"
                elif i >= 28 and i < 35:
                    gsp.group = "E"
                elif i >= 35 and i < 42:
                    gsp.group = "F"
                gsp.name = name[i%7]
                gsp.pick = picks[i][j]
                gsp.position = position + 1
                position +=1
                gsp.save()
                ##print (pick_num)
                pick_num+=1


    #Updating positions for ACTUAL

    actual_pos = {}
    actual_pos["A"] = ["Italy", "Wales", "Switzerland", "DNQ"]
    actual_pos["B"] = ["Belgium", "Denmark", "DNQ", "DNQ"]
    actual_pos["C"] = ["Netherlands", "Austria", "Ukraine", "DNQ"]
    actual_pos["D"] = ["England", "Croatia", "Czech Republic", "DNQ"]
    actual_pos["E"] = ["Sweden", "Spain", "DNQ", "DNQ"]
    actual_pos["F"] = ["France", "Germany", "Portugal", "DNQ"]
    
    #Update latest standings 
    num_groups = 6
    num_players = 6
    num_teams_per_group = 4
    AllGroups = ["A", "B", "C", "D", "E", "F"]
    for i in range(num_groups):
        for j in range(num_teams_per_group):
            c = GroupStagePicks.objects.filter(name="Actual", group=AllGroups[i], position=j+1)
            c.update(pick = actual_pos[AllGroups[i]][j])

    AllPlayers = ["Volkan", "Evgueni", "Ramraj", "Ram", "Peter", "Fadi"]
    
    gp_points = [0, 0, 0, 0, 0, 0]
    acc_points = [0, 0, 0, 0, 0, 0]
    bonus_points = [0, 0, 0, 1, 0, 2]
    total_points = [0, 0, 0, 0, 0, 0]
    acc_percentage = [99.99,99.99,99.99,99.99,99.99,99.99]
    
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
                                print (AllPlayers[i])
                                print (d.pick)
                                print ("")
                                acc_points[i] +=1
                                gp_points[i] +=1

    for i in range(num_players): #players
        acc_percentage[i] = (acc_points[i]/32)*100
        total_points[i] = gp_points[i] + bonus_points[i]

    print ("points as follows")
    print (gp_points[0], acc_points[0], acc_percentage[0])
    print (gp_points[1], acc_points[1], acc_percentage[1])
    print (gp_points[2], acc_points[2], acc_percentage[2])
    print (gp_points[3], acc_points[3], acc_percentage[3])
    print (gp_points[4], acc_points[4], acc_percentage[4])
    print (gp_points[5], acc_points[5], acc_percentage[5])

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
    
    #creating picks compatible for html viewing -- Group C
    latest_group_picks_C0 = [""]*(num_players+1)
    latest_group_picks_C1 = [""]*(num_players+1)
    latest_group_picks_C2 = [""]*(num_players+1)
    latest_group_picks_C3 = [""]*(num_players+1)

    if GroupStagePicks.objects.filter(name=AllPlayers[i], group="C").exists():
        latest_group_picks_C0[0] = GroupStagePicks.objects.get(group="C", position=1, name="Actual")
        latest_group_picks_C1[0] = GroupStagePicks.objects.get(group="C", position=2, name="Actual")
        latest_group_picks_C2[0] = GroupStagePicks.objects.get(group="C", position=3, name="Actual")
        latest_group_picks_C3[0] = GroupStagePicks.objects.get(group="C", position=4, name="Actual")
        
        for i in range(num_players):
            #for j in range(num_teams_per_group):
            latest_group_picks_C0[i+1] = GroupStagePicks.objects.get(group="C", position=1, name=AllPlayers[i])
            latest_group_picks_C1[i+1] = GroupStagePicks.objects.get(group="C", position=2, name=AllPlayers[i])
            latest_group_picks_C2[i+1] = GroupStagePicks.objects.get(group="C", position=3, name=AllPlayers[i])
            latest_group_picks_C3[i+1] = GroupStagePicks.objects.get(group="C", position=4, name=AllPlayers[i])

    #creating picks compatible for html viewing -- Group D
    latest_group_picks_D0 = [""]*(num_players+1)
    latest_group_picks_D1 = [""]*(num_players+1)
    latest_group_picks_D2 = [""]*(num_players+1)
    latest_group_picks_D3 = [""]*(num_players+1)

    if GroupStagePicks.objects.filter(name=AllPlayers[i], group="D").exists():
        latest_group_picks_D0[0] = GroupStagePicks.objects.get(group="D", position=1, name="Actual")
        latest_group_picks_D1[0] = GroupStagePicks.objects.get(group="D", position=2, name="Actual")
        latest_group_picks_D2[0] = GroupStagePicks.objects.get(group="D", position=3, name="Actual")
        latest_group_picks_D3[0] = GroupStagePicks.objects.get(group="D", position=4, name="Actual")
        
        for i in range(num_players):
            #for j in range(num_teams_per_group):
            latest_group_picks_D0[i+1] = GroupStagePicks.objects.get(group="D", position=1, name=AllPlayers[i])
            latest_group_picks_D1[i+1] = GroupStagePicks.objects.get(group="D", position=2, name=AllPlayers[i])
            latest_group_picks_D2[i+1] = GroupStagePicks.objects.get(group="D", position=3, name=AllPlayers[i])
            latest_group_picks_D3[i+1] = GroupStagePicks.objects.get(group="D", position=4, name=AllPlayers[i])

    #creating picks compatible for html viewing -- Group E
    latest_group_picks_E0 = [""]*(num_players+1)
    latest_group_picks_E1 = [""]*(num_players+1)
    latest_group_picks_E2 = [""]*(num_players+1)
    latest_group_picks_E3 = [""]*(num_players+1)

    if GroupStagePicks.objects.filter(name=AllPlayers[i], group="E").exists():
        latest_group_picks_E0[0] = GroupStagePicks.objects.get(group="E", position=1, name="Actual")
        latest_group_picks_E1[0] = GroupStagePicks.objects.get(group="E", position=2, name="Actual")
        latest_group_picks_E2[0] = GroupStagePicks.objects.get(group="E", position=3, name="Actual")
        latest_group_picks_E3[0] = GroupStagePicks.objects.get(group="E", position=4, name="Actual")
        
        for i in range(num_players):
            #for j in range(num_teams_per_group):
            latest_group_picks_E0[i+1] = GroupStagePicks.objects.get(group="E", position=1, name=AllPlayers[i])
            latest_group_picks_E1[i+1] = GroupStagePicks.objects.get(group="E", position=2, name=AllPlayers[i])
            latest_group_picks_E2[i+1] = GroupStagePicks.objects.get(group="E", position=3, name=AllPlayers[i])
            latest_group_picks_E3[i+1] = GroupStagePicks.objects.get(group="E", position=4, name=AllPlayers[i])

    #creating picks compatible for html viewing -- Group F
    latest_group_picks_F0 = [""]*(num_players+1)
    latest_group_picks_F1 = [""]*(num_players+1)
    latest_group_picks_F2 = [""]*(num_players+1)
    latest_group_picks_F3 = [""]*(num_players+1)

    if GroupStagePicks.objects.filter(name=AllPlayers[i], group="F").exists():
        latest_group_picks_F0[0] = GroupStagePicks.objects.get(group="F", position=1, name="Actual")
        latest_group_picks_F1[0] = GroupStagePicks.objects.get(group="F", position=2, name="Actual")
        latest_group_picks_F2[0] = GroupStagePicks.objects.get(group="F", position=3, name="Actual")
        latest_group_picks_F3[0] = GroupStagePicks.objects.get(group="F", position=4, name="Actual")
        
        for i in range(num_players):
            #for j in range(num_teams_per_group):
            latest_group_picks_F0[i+1] = GroupStagePicks.objects.get(group="F", position=1, name=AllPlayers[i])
            latest_group_picks_F1[i+1] = GroupStagePicks.objects.get(group="F", position=2, name=AllPlayers[i])
            latest_group_picks_F2[i+1] = GroupStagePicks.objects.get(group="F", position=3, name=AllPlayers[i])
            latest_group_picks_F3[i+1] = GroupStagePicks.objects.get(group="F", position=4, name=AllPlayers[i])


    #Round of 16
    #creating picks compatible for html viewing -- Round of 16
    num_ro16_games = 8
    latest_ro16_picks_0 = ["Denmark"]*(num_players)
    latest_ro16_picks_1 = ["Italy"]*(num_players)
    latest_ro16_picks_2 = ["Netherlands"]*(num_players)
    latest_ro16_picks_3 = ["Belgium"]*(num_players)
    latest_ro16_picks_3[5] = "Portugal"
    latest_ro16_picks_4 = ["Spain"]*(num_players)
    latest_ro16_picks_4[1] = "Croatia"
    latest_ro16_picks_5 = ["France"]*(num_players)
    latest_ro16_picks_6 = ["England"]*(num_players)
    latest_ro16_picks_6[4] = "Germany"
    latest_ro16_picks_6[5] = "Germany"
    latest_ro16_picks_7 = ["Sweden"]*(num_players)
    latest_ro16_picks_7[4] = "Ukraine"

    print (latest_ro16_picks_0)

    latest_ro16_loyalty_0 = ["Denmark"]*(num_players)
    latest_ro16_loyalty_1 = ["Italy"]*(num_players)
    latest_ro16_loyalty_1[0] = "Both"
    latest_ro16_loyalty_1[1] = "Both"
    latest_ro16_loyalty_1[2] = "Both"
    latest_ro16_loyalty_1[5] = "Both"

    latest_ro16_loyalty_2 = ["Netherlands"]*(num_players)
    latest_ro16_loyalty_2[4] = "Both"
    latest_ro16_loyalty_2[5] = "Both"

    latest_ro16_loyalty_3 = ["Both"]*(num_players)

    latest_ro16_loyalty_4 = ["Both"]*(num_players)

    latest_ro16_loyalty_5 = ["France"]*(num_players)
    latest_ro16_loyalty_5[0] = "Both"
    latest_ro16_loyalty_5[2] = "Both"
    latest_ro16_loyalty_5[3] = "Both"
    latest_ro16_loyalty_5[5] = "Both"

    latest_ro16_loyalty_6 = ["Both"]*(num_players)
    latest_ro16_loyalty_6[0] = "England"

    latest_ro16_loyalty_7 = ["Both"]*(num_players)
    latest_ro16_loyalty_7[2] = "Ukraine"
    latest_ro16_loyalty_7[5] = "Sweden"
    
    ro16_games_0 = "Wales vs Denmark"
    ro16_games_1 = "Italy vs Austria"
    ro16_games_2 = "Netherlands vs Czech Republic" 
    ro16_games_3 = "Belgium vs Portugal" 
    ro16_games_4 = "Croatia vs Spain"
    ro16_games_5 = "France vs Switzerland" 
    ro16_games_6 = "England vs Germany"
    ro16_games_7 = "Sweden vs Ukraine"
    
    

    overall_total_points = [0]*num_players
    finals_total_points = [0]*num_players
    semifinals_total_points = [0]*num_players
    quarterfinals_total_points = [0]*num_players
    ro16_total_points = [0]*num_players

    #Ro16 point calculations
    ro16_total_points[0] = 2 + 2 + 0 + 2 + 0 + 0 + 0 + 0
    ro16_total_points[1] = 2 + 2 + 0 + 2 + 0 + 0 + 0 + 0
    ro16_total_points[2] = 2 + 2 + 0 + 2 + 0 + 0 + 0 + 0
    ro16_total_points[3] = 2 + 2 + 0 + 2 + 0 + 0 + 0 + 0
    ro16_total_points[4] = 2 + 2 + 0 + 2 + 0 + 0 + 0 + 0
    ro16_total_points[5] = 2 + 2 + 0 + 0 + 0 + 0 + 0 + 0

    for i in range(num_players):
        overall_total_points[i] = finals_total_points[i] + semifinals_total_points[i] + quarterfinals_total_points[i] + ro16_total_points[i] + total_points[i]

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
        'latest_group_picks_C0': latest_group_picks_C0,
        'latest_group_picks_C1': latest_group_picks_C1,
        'latest_group_picks_C2': latest_group_picks_C2,
        'latest_group_picks_C3': latest_group_picks_C3,
        'latest_group_picks_D0': latest_group_picks_D0,
        'latest_group_picks_D1': latest_group_picks_D1,
        'latest_group_picks_D2': latest_group_picks_D2,
        'latest_group_picks_D3': latest_group_picks_D3,
        'latest_group_picks_E0': latest_group_picks_E0,
        'latest_group_picks_E1': latest_group_picks_E1,
        'latest_group_picks_E2': latest_group_picks_E2,
        'latest_group_picks_E3': latest_group_picks_E3,
        'latest_group_picks_F0': latest_group_picks_F0,
        'latest_group_picks_F1': latest_group_picks_F1,
        'latest_group_picks_F2': latest_group_picks_F2,
        'latest_group_picks_F3': latest_group_picks_F3,
        'group_points': gp_points,
        'acc_percentage': acc_percentage,
        'bonus_points': bonus_points,
        'total_points': total_points,
        'latest_ro16_picks_0': latest_ro16_picks_0,
        'latest_ro16_picks_1': latest_ro16_picks_1,
        'latest_ro16_picks_2': latest_ro16_picks_2,
        'latest_ro16_picks_3': latest_ro16_picks_3,
        'latest_ro16_picks_4': latest_ro16_picks_4,
        'latest_ro16_picks_5': latest_ro16_picks_5,
        'latest_ro16_picks_6': latest_ro16_picks_6,
        'latest_ro16_picks_7': latest_ro16_picks_7,
        'latest_ro16_loyalty_0': latest_ro16_loyalty_0,
        'latest_ro16_loyalty_1': latest_ro16_loyalty_1,
        'latest_ro16_loyalty_2': latest_ro16_loyalty_2,
        'latest_ro16_loyalty_3': latest_ro16_loyalty_3,
        'latest_ro16_loyalty_4': latest_ro16_loyalty_4,
        'latest_ro16_loyalty_5': latest_ro16_loyalty_5,
        'latest_ro16_loyalty_6': latest_ro16_loyalty_6,
        'latest_ro16_loyalty_7': latest_ro16_loyalty_7,
        'ro16_games_0': ro16_games_0,
        'ro16_games_1': ro16_games_1,
        'ro16_games_2': ro16_games_2,
        'ro16_games_3': ro16_games_3,
        'ro16_games_4': ro16_games_4,
        'ro16_games_5': ro16_games_5,
        'ro16_games_6': ro16_games_6,
        'ro16_games_7': ro16_games_7,
        'overall_total_points': overall_total_points,
        'finals_total_points': finals_total_points,
        'semifinals_total_points': semifinals_total_points,
        'quarterfinals_total_points': quarterfinals_total_points,
        'ro16_total_points': ro16_total_points,
    }
    return render(request, 'euro2020/index.html', context)
    #else:
    #    return HttpResponse("Nothing to list")