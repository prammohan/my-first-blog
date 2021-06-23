from django.contrib import admin

# Register your models here.
from .models import Bet, GroupStagePicks

admin.register(Bet, GroupStagePicks)(admin.ModelAdmin)


count = 0
count +=1
print (count)
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


rows, cols = (6, 4)
picks = [[""]*cols]*rows

name = ["Actual", "Evgueni", "Ram"]
#Group A
picks[0] = ["India", "Argentina", "Ghana", "DNQ"]
picks[1] = ["Argentina", "India", "Ghana", "-"]
picks[2] = ["Argentina", "India", "Ghana", "-"]

#Group B
picks[3] = ["England", "Australia", "Italy", "DNQ"]
picks[4] = ["England", "Australia", "Italy", "-"]
picks[5] = ["England", "Australia", "Italy", "-"]

pick_num = 0
for i in range(len(picks)):
    position = 0
    for j in range(len(picks[i])):
        gsp = GroupStagePicks()
        if (i < 3):
            gsp.group = "A"
        else:
            gsp.group = "B"
        gsp.name = name[i%3]
        gsp.pick = picks[i][j]
        gsp.position = position + 1
        position +=1
        if GroupStagePicks.objects.filter(name=gsp.name, group=gsp.group, position=gsp.position).exists():
            pass
        else:
            gsp.save()
        print (pick_num)
        pick_num+=1