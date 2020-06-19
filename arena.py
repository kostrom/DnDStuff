from dice import roll

def attackRolls(player,enemy, detailedTracking):
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


