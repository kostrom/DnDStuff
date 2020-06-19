import random
import math

#### PLAYER ####
class Player:
    def __init__(self,name="BLANK",maxhp=0,ac=0,initBonus=0,critRange=20,ham=False,reckless=False,sneakAtkDice=0,init=0,attacks=[],wincount=0,wentFirst=0,wentFirstWon=0,critCounter=0,hitsCounter=0):
        self.name = name
        self.maxhp = maxhp
        self.hp = maxhp
        self.ac = ac
        self.initBonus = initBonus
        self.init = init
        self.critRange = critRange
        self.ham = ham
        self.reckless = reckless
        self.sneakAtkDice = sneakAtkDice
        # attacks is defined later
        self.attacks = attacks
        # below for stat-tracking
        self.wincount = wincount
        self.wentFirst = wentFirst
        self.wentFirstWon = wentFirstWon
        self.critCounter = critCounter
        self.hitsCounter = hitsCounter

    def takeDamage(self,damage):
        if self.ham: # Heavy Armor Master reduces damage by 3
            if detailedTracking:print(str(damage-3)+" damage after HAM reduced by 3")
            damage -= 3
        self.hp -= damage
        if detailedTracking:print(self.name+" "+str(self.hp)+"/"+str(self.maxhp))

#### DICE ####
def roll(dieCount,dieSize):
    result = random.randint(dieCount, dieSize)
    return result

def attackRolls(player,enemy):
    sa_hit = False
    for atk in player.attacks:
        flatRoll = roll(1,20)
        atkRoll = flatRoll+atk[0]
        dmgRange = [atk[1],atk[2]*atk[1]]
        sa_dmgRange = [player.sneakAtkDice,6*player.sneakAtkDice]
        if atkRoll >= enemy.ac or flatRoll >= player.critRange: #auto hit on crits'
            if flatRoll >= player.critRange:
                if detailedTracking:print(player.name+" Atk: ("+str(flatRoll)+"), total: "+str(atkRoll)+" CRITICAL HIT!")
                dmgRoll = roll(dmgRange[0]*2,dmgRange[1]*2)
                player.critCounter +=1
                dmgString = "Crit Dmg: "+str(atk[1]*2)+"d"+str(atk[2])+"+"+str(atk[3])+" (range: "+str((dmgRange[0]*2)+atk[3])+"-"+str((dmgRange[1]*2)+atk[3])+")"
                if player.sneakAtkDice > 0 and sa_hit == False:
                    sa_dmgRoll = roll(sa_dmgRange[0]*2,sa_dmgRange[1]*2)
                    sa_hit = True
                    if detailedTracking:print("Sneak Attack dice: "+str(sa_dmgRange[0]*2)+"d"+str(6)+", damage: "+str(sa_dmgRoll))
                    enemy.takeDamage(sa_dmgRoll)
            else:
                if detailedTracking:print(player.name+" Atk: ("+str(flatRoll)+"), total: "+str(atkRoll)+" HIT!")
                dmgRoll = roll(dmgRange[0],dmgRange[1])
                dmgString = "Dmg: "+str(atk[1])+"d"+str(atk[2])+"+"+str(atk[3])+" (range: "+str(dmgRange[0]+atk[3])+"-"+str(dmgRange[1]+atk[3])+")"
                if player.sneakAtkDice > 0 and sa_hit == False:
                    sa_dmgRoll = roll(sa_dmgRange[0],sa_dmgRange[1])
                    sa_hit = True
                    if detailedTracking:print("Sneak Attack dice: "+str(sa_dmgRange[0])+"d"+str(6)+", damage: "+str(sa_dmgRoll))
                    enemy.takeDamage(sa_dmgRoll)
            atkDmg = dmgRoll+atk[3]
            if detailedTracking:
                print(dmgString)
                print("Dealt "+str(atkDmg)+" dmg, ("+str(dmgRoll)+")+"+str(atk[3]))
            enemy.takeDamage(atkDmg)
            player.hitsCounter +=1
        else:
            if detailedTracking:print(player.name+" missed.")
        if detailedTracking:print()
        if enemy.hp <= 0:
            return "death"
    if enemy.hp <= 0:
        return "death"

def calcHP(level,hitDie,conMod):
    hp = hitDie+conMod # start with max HP at level 1
    hpGain = math.ceil((hitDie+1)/2)+conMod # calc how many HP are gained each level. (hitDie+1)/2 gets us the avg. ceil rounds up.
    if level > 1:
        hp += (hpGain*level)
    return hp

##################################################################
# name,maxhp,ac,initBonus,critRange (e.g. 19 for 19-20, 18 for 18-20, 20 for default)
# calcHP(4,10,1) e.g. 4th level, d10's, +1 Con mod
p1 = Player()
p2 = Player()

p1.name = "Player"
p1Level = 10
p1HitDie = 10
p1ConMod = 3
p1.maxhp = calcHP(p1Level,p1HitDie,p1ConMod)
p1.ac = 15
p1.initBonus = 10
p1.critRange = 20

p2.name = "Baddie"
p2Level = 10
p2HitDie = 10
p2ConMod = 3
p2.maxhp = calcHP(p2Level,p2HitDie,p2ConMod)
p2.ac = 15
p2.initBonus = 0
p2.critRange = 20

p1.attacks = [[7,2,6,5],[7,2,6,5]] # e.g. +7,1d12+5 = [7,1,12,5]
p2.attacks = [[7,2,6,5],[7,2,6,5]] # e.g. +5, 2d6+3 = [5,2,6,3]

detailedTracking = False # show full breakdown of combat or not. Recommend False for over 100 battles.
battles = 80000

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
            if attackRolls(p1,p2) == "death" or attackRolls(p2,p1) == "death":
                break;
        else:
            if attackRolls(p2,p1) == "death" or attackRolls(p1,p2) == "death":
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







'''
### Observations and notes ###
# Based on 80,000 matches per #
# The main principle of these tests is: "all things being equal" #
# This helps with a direct comparison without adding other complications #

Level 10 Fighters, Greatswords, Extra Attack, 103HP, 15AC
    +1 init, 51.5%-48.5% (+3%)
    +2 init, 52.4%-47.6% (+4.8%)
    +3 init, 53.1%-46.9% (+6.3%)
    +4 init, 53.6%-46.4% (+7.2%)
    +5 init, 54.6%-45.4% (+9.2%)
    ...
    +10 init, 57.2%-42.8% (+14.4%)

19AC vs. 18AC resulted in 60%-40% winrate. (+20%)
20AC vs. 18AC resulted in 70%-30% winrate. (+30%)
21AC vs. 18AC resulted in 78%-22% winrate in favor. (+56%)
22AC vs. 18AC resulted in 86%-14% winrate in favor. (+72%)
23AC vs. 18AC resulted in 92%-8% winrate in favor. (+84%)
24AC vs. 18AC resulted in 96%-4% winrate in favor. (+92%)

18AC vs. 17AC resulted in 60%-40% winrate. (+20%)
18AC vs. 16AC resulted in 68%-32% winrate. (+36%)
18AC vs. 15AC resulted in 75%-25% winrate. (+50%)
18AC vs. 14AC resulted in 81%-19% winrate. (+62%)
18AC vs. 13AC resulted in 87%-13% winrate. (+74%)
18AC vs. 12AC resulted in 90%-10% winrate. (+80%)

Crits on 19 resulted in 52.5%-47.5% winrate. (+5%)
Crits on 18 resulted in 55%-45% winrate. (+10%)

Greatsword vs. Greataxe resulted in 53%-47% in favor of Greatsword. (+6%)

All things being equal, having Extra Attack vs. not resulted in 89%-11% in favor. (+78%)

Without extra attack:
    Greatsword vs. dual Shortswords (no ability mod on offhand)
        49.7%-50.3% in favor of Shortswords
    Greatsword vs. dual Shortswords with Two-Weapon Fighting
        20.3%-79.7% in favor of Shortswords
    Greatsword with Defense Style (+1AC) vs. dual Shortswords with Two-Weapon Fighting
        28.2%-71.8% in favor of Shortswords
With extra attack:
    Greatsword vs. dual Shortswords (no ability mod on offhand)
        65.6%-34.4% in favor of Greatsword
    Greatsword vs. dual Shortswords with Two-Weapon Fighting
        45.2%-54.8% in favor of Shortswords
    Greatsword with Defense Style (+1AC) vs. dual Shortswords with Two-Weapon Fighting
        55%-45% in favor of Greatsword
With extra attack (x2):
    Greatsword vs. dual Shortswords (no ability mod on offhand)
        70.6%-29.4% in favor of Greatsword
    Greatsword vs. dual Shortswords with Two-Weapon Fighting
        56.7-43.3% in favor of Greatsword
    Greatsword with Defense Style (+1AC) vs. dual Shortswords with Two-Weapon Fighting
        65.8%-34.2% in favor of Greatsword

Dual-Wielder Feat (two Rapiers and +1AC) vs. not:
    71.8%-28.2% in favor of Dual-Wielder Feat (no extra attack, 19vs18 AC)
    71.6%-28.4% in favor of Dual-Wielder feat (extra attack, 17vs16 AC)

Dual-Wielder Feat (two Rapiers and +1AC) vs. +2 Dex:
    40.9%-59.1% in favor of +2 Dex, not counting the ability to draw two weapons at once. (+18%)

Dual-Wielder Feat (two Rapiers and +1AC) vs. Heavy Armor Master:
    29%-71% in favor of Heavy Armor Master. (Level 8, 20 Str/Dex, 2x Extra Attack (4 attacks total), TWF style) (+42%)

Heavy Armor Master vs. not:
    72%-28% in favor of HAM. (level 8, Extra Attack, Greatswords, 20 Str) (+44%)
    87%-13% in favor of HAM. (level 8, Extra Attack, dual Shortswords, 20 Str) (+74%)

GWM/SS vs. not:
    Level 10 Fighters, Extra Attacks, Greataxes, 18 Strength (+8 to attack bonus)
         9AC: 82%-18% (+64%)
        10AC: 79%-21% (+58%)
        11AC: 77%-23% (+54%)
        12AC: 74%-26% (+48%)
        13AC: 71%-29% (+42%)
        14AC: 68%-32% (+36%)
        15AC: 65%-35% (+30%)
        16AC: 61%-39% (+22%)
        17AC: 57%-43% (+14%)
        18AC: 52%-48% (+4%)
        19AC: 46%-54% (-8%) //// @19AC it's better to not use GWM/SS
        20AC: 40%-60% (-20%)
        21AC: 32%-68% (-36%)
        22AC: 22%-78% (-56%)
        23AC: 10%-90% (-80%)

GWM/SS vs. +2 Strength:
    Level 10 Fighters, Extra Attacks, Greataxes, 18/20 Strength
        9AC: 75%-25% (+50%)
        10AC: 68%-32% (+36%)
        11AC: 66%-34% (+32%)
        12AC: 62%-38% (+24%)
        13AC: 60%-40% (+20%)
        14AC: 57%-43% (+14%)
        15AC: 53%-47% (+6%)
        16AC: 49%-51% (-1%) //// @16AC +2 str becomes better.
        17AC: 45%-55% (-10%)
        18AC: 41%-59% (-18%)
        19AC: 35%-65% (-30%)
        20AC: 29%-71% (-42%)
        21AC: 22%-78% (-56%)
        22AC: 14%-86% (-72%)
        23AC: 06%-94% (-88%)

GWM/SS vs. +2 Strength:
    Level 5 Fighters, Extra Attacks, Greatswords, 18/20 Strength
        ...
        14AC: 50.5%-49.5% (+1%)
        15AC: 48%-52% (-4%) //// @15AC +2 str becomes better.
        ...

155HP vs. 150HP resulted in 54%-46% winrate in favor. (+8%)
105HP vs. 100HP resulted in 55%-45% winrate in favor. (+10%)
55HP vs. 50HP resulted in 57%-43% winrate in favor. (+14%)
25HP vs. 20HP resulted in 60%-40% winrate in favor. (+20%)
15HP vs. 10HP resulted in 65%-35% winrate in favor. (+30%)

### Constitution>HP tests ###

Level 1 Barbarian
    +1 Conmod: 53%-47% (+6%)
    +2 Conmod: 56%-44% (+12%)
    +3 Conmod: 59%-41% (+18%)
    +4 Conmod: 62%-38% (+24%)
    +5 Conmod: 66%-34% (+32%)

Level 2 Barbarian
    +1 Conmod: 56%-43%
    +2 Conmod: 63%-37%
    +3 Conmod: 68%-31%
    +4 Conmod: 73%-27%
    +5 Conmod: 78%-22%

Level 5 Barbarian
    +1 Conmod: 59.5%-40.5% (+19%)
    ...
    +5 Conmod: 87%-13% (+74%)

Level 10 Barbarian
    +1 Conmod: 64%-36% (+28%)
    ...
    +5 Conmod: 94%-6% (+88%)

Level 20 Barbarian
    +1 Conmod: 69%-31% (+38%)
    ...
    +5 Conmod: 98.8%-1.2% (+97.6%)

'''
