from player import Player, calculate_max_hitpoints
from arena import attack_rolls
from dice import roll

##################################################################
# name,maxhp,ac,initBonus,critRange (e.g. 19 for 19-20, 18 for 18-20, 20 for default)
# calcHP(4,10,1) e.g. 4th level, d10's, +1 Con mod
p1 = Player()
p2 = Player()

p1.name = "Player"
p1Level = 10
p1HitDie = 10
p1ConMod = 3
p1.maxhp = calculate_max_hitpoints(p1Level,p1HitDie,p1ConMod)
p1.hp = p1.maxhp
p1.ac = 15
p1.initBonus = 10
p1.critRange = 20

p2.name = "Baddie"
p2Level = 10
p2HitDie = 10
p2ConMod = 3
p2.maxhp = calculate_max_hitpoints(p2Level,p2HitDie,p2ConMod)
p2.hp = p2.maxhp
p2.ac = 15
p2.initBonus = 0
p2.critRange = 20

p1.attacks = [[7,2,6,5],[7,2,6,5]] # e.g. +7,1d12+5 = [7,1,12,5]
p2.attacks = [[7,2,6,5],[7,2,6,5]] # e.g. +5, 2d6+3 = [5,2,6,3]

battles = 1
detailedTracking = (1 == battles)
p1.detailedTracking = detailedTracking
p2.detailedTracking = detailedTracking

# there is a much easier way to do this, but im lazy atm.
for x in range(battles): #rematches
    i = 0

    # init time!
    if detailedTracking:
        print()
        print("~~~~~~~~~~~~~~~~~~~~")
        print("~~~~FRESH INITS!~~~~")
        print("~~~~~~~~~~~~~~~~~~~~")
    p1flatInit = roll(1,20)
    p1.init = p1flatInit+p1.initBonus
    if detailedTracking:print(p1.name+" init: ("+str(p1flatInit)+")+"+str(p1.initBonus)+" total: "+str(p1.init))

    p2flatInit = roll(1,20)
    p2.init = p2flatInit+p2.initBonus
    if detailedTracking:print(p2.name+" init: ("+str(p2flatInit)+")+"+str(p2.initBonus)+" total: "+str(p2.init))

    if p1.init > p2.init:
        if detailedTracking:print(p1.name+" goes first!")
        firstPlayer = "p1"
        p1.wentFirst += 1
    elif p1.init < p2.init:
        if detailedTracking:print(p2.name+" goes first!")
        firstPlayer = "p2"
        p2.wentFirst += 1
    else:
        if p1.initBonus > p2.initBonus:
            if detailedTracking:print("Tied, but "+p1.name+" goes first because of higher dex mod!")
            firstPlayer = "p1"
            p1.wentFirst += 1
        elif p1.initBonus < p2.initBonus:
            if detailedTracking:print("Tied, but "+p2.name+" goes first because of higher dex mod!")
            firstPlayer = "p2"
            p2.wentFirst += 1
        else: # coinflip time!
            if roll(1,2) == 1:
                if detailedTracking:print("Tied, but "+p1.name+" goes first because of coinflip!")
                firstPlayer = "p1"
                p1.wentFirst += 1
            else:
                if detailedTracking:print("Tied, but "+p2.name+" goes first because of coinflip!")
                firstPlayer = "p2"
                p2.wentFirst += 1

    while (True):
        i += 1
        if i > 200: #max rounds. Just to prevent infinte loops
            break
        if detailedTracking:print("\nRound "+str(i)) #spacing for each round
        if firstPlayer == "p1":
            if attack_rolls(p1, p2, detailedTracking) == "death" or attack_rolls(p2, p1, detailedTracking) == "death":
                break;
        else:
            if attack_rolls(p2, p1, detailedTracking) == "death" or attack_rolls(p1, p2, detailedTracking) == "death":
                break;

    if p1.hp <= 0:
        if detailedTracking:print(p2.name+" won!")
        p2.wincount += 1
        if firstPlayer == "p2":
            p2.wentFirstWon += 1
    if p2.hp <= 0:
        if detailedTracking:print(p1.name+" won!")
        p1.wincount += 1
        if firstPlayer == "p1":
            p1.wentFirstWon += 1
    # restore HP
    p1.hp = p1.maxhp
    p2.hp = p2.maxhp
    if detailedTracking:print()

else:
    print("\n~~~~~~~~~~~~~~~~~~~~")
    print("~~~END OF BATTLES~~~")
    print("~~~~~~~~~~~~~~~~~~~~")
    print(p1.name+"'s Max HP: "+str(p1.maxhp)+", AC: "+str(p1.ac))
    print(p2.name+"'s Max HP: "+str(p2.maxhp)+", AC: "+str(p2.ac))
    print()
    print("Battles: "+str(battles))
    winPerc1n = (p1.wincount/battles)*100
    winPerc = "%.2f" % winPerc1n
    print(p1.name+" winrate: "+str(winPerc)+"%")
    print("    Total wins: "+str(p1.wincount))
    print("    "+"Went first: "+str(p1.wentFirst)+" times (went first and won: "+str(p1.wentFirstWon)+" times)")
    print("    Hits: "+str(p1.hitsCounter))
    print("    Critical hits: "+str(p1.critCounter))

    print()
    winPerc2n = (p2.wincount/battles)*100
    winPerc = "%.2f" % winPerc2n
    print(p2.name+" winrate: "+str(winPerc)+"%")
    print("    Total wins: "+str(p2.wincount))
    print("    "+"Went first: "+str(p2.wentFirst)+" times (went first and won: "+str(p2.wentFirstWon)+" times)")
    print("    Hits: "+str(p2.hitsCounter))
    print("    Critical hits: "+str(p2.critCounter))

    print()
    print("Win % difference: "+str("%.2f" % (winPerc1n-winPerc2n)))
