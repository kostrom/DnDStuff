from math import ceil

def calcHP(level,hitDie,conMod):
    hp = hitDie+conMod # start with max HP at level 1
    hpGain = ceil((hitDie+1)/2)+conMod # calc how many HP are gained each level. (hitDie+1)/2 gets us the avg. ceil rounds up.
    if level > 1:
        hp += (hpGain*level)
    return hp

class Player():
    def __init__(self,name="BLANK",maxhp=0,ac=0,initBonus=0,critRange=20,ham=False,reckless=False,sneakAtkDice=0,init=0,attacks=[],wincount=0,wentFirst=0,wentFirstWon=0,critCounter=0,hitsCounter=0, detailedTracking=False):
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
        self.detailedTracking = detailedTracking

    def takeDamage(self, damage):
        if self.ham: # Heavy Armor Master reduces damage by 3
            if self.detailedTracking:
                print(str(damage-3)+" damage after HAM reduced by 3")
            damage -= 3
        self.hp -= damage
        if self.detailedTracking:
            print(self.name+" "+str(self.hp)+"/"+str(self.maxhp))

    def calcHP(self, level, hitDie, conMod):
        hp = self.hitDie + self.conMod # start with max HP at level 1
        hpGain = math.ceil((self.hitDie+1)/2)+self.conMod # calc how many HP are gained each level. (hitDie+1)/2 gets us the avg. ceil rounds up.
        if level > 1:
            hp += (self.hpGain*self.level)
        return hp

