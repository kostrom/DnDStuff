""" player """
from math import ceil

def calculate_max_hitpoints(level, hit_dice, con_mod):
    """ calculate maximum hitpoints """
    hp = hit_dice+con_mod # start with max HP at level 1
    hpGain = ceil((hit_dice+1)/2)+con_mod # use average for each level
    if level > 1:
        hp += (hpGain*level)
    return hp

class Player():
    """ player statistics for battle simulator """
    def __init__(self, name="BLANK", maxhp=0, ac=0, initBonus=0, critRange=20, ham=False,
                 reckless=False, sneakAtkDice=0, init=0, attacks=(), wincount=0, wentFirst=0,
                 wentFirstWon=0, critCounter=0, hitsCounter=0, detailedTracking=False):
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

    def take_damage(self, damage):
        if self.ham: # Heavy Armor Master reduces damage by 3
            if self.detailedTracking:
                print(str(damage-3)+" damage after HAM reduced by 3")
            damage -= 3
        self.hp -= damage
        if self.detailedTracking:
            print(self.name+" "+str(self.hp)+"/"+str(self.maxhp))
