"""arena.py has functions to execute combat"""
from dice import roll

def attack_rolls(player, enemy, detailed_tracking):
    """attack_rolls runs a fight to the death between two players"""
    for atk in player.attacks:
        flat_roll = roll(1, 20)
        attack_roll = flat_roll+atk[0]
        damage_range = [atk[1], atk[2]*atk[1]]
        sneak_attack_damage_range = [player.sneakAtkDice, 6*player.sneakAtkDice]
        if attack_roll >= enemy.ac or flat_roll >= player.critRange: #auto hit on crits'
            if flat_roll >= player.critRange:
                if detailed_tracking:
                    print("{} Atk: ({}), total: {} CRITICAL HIT!".format(
                        player.name, flat_roll, attack_roll))
                damage_roll = roll(damage_range[0]*2, damage_range[1]*2)
                player.critCounter += 1
                damage_string = "Crit Dmg: {}d{}+{} (range: {}-{})".format(
                    atk[1]*2, atk[2], atk[3], damage_range[0]*2+atk[3], damage_range[1]*2+atk[3])
                if player.sneakAtkDice > 0:
                    sneak_attack_damage_roll = roll(sneak_attack_damage_range[0]*2,
                                                    sneak_attack_damage_range[1]*2)
                    if detailed_tracking:
                        print("Sneak Attack dice: {}d{}, damage: {}".format(
                            sneak_attack_damage_range[0]*2, 6, sneak_attack_damage_roll))
                    enemy.take_damage(sneak_attack_damage_roll)
            else:
                if detailed_tracking:
                    print("{} Atk: ({}), total: {} HIT!".format(
                        player.name, flat_roll, attack_roll))
                damage_roll = roll(damage_range[0], damage_range[1])
                damage_string = "Dmg: {}+{} (range: {}-{})".format(
                    atk[2], atk[3], damage_range[0]+atk[3], damage_range[1]+atk[3])
                if player.sneakAtkDice > 0:
                    sneak_attack_damage_roll = roll(
                        sneak_attack_damage_range[0], sneak_attack_damage_range[1])
                    if detailed_tracking:
                        print("Sneak Attack dice: {}d{}, damage: {}".format(
                            sneak_attack_damage_range[0], 6, sneak_attack_damage_roll))
                    enemy.take_damage(sneak_attack_damage_roll)
            attack_damage = damage_roll+atk[3]
            if detailed_tracking:
                print(damage_string)
                print("Dealth {} dmg, ({})+{}".format(attack_damage, damage_roll, atk[3]))
            enemy.take_damage(attack_damage)
            player.hitsCounter += 1
        else:
            if detailed_tracking:
                print(player.name+" missed.")
        if detailed_tracking:
            print()
        if enemy.hp <= 0:
            return "death"
    if enemy.hp <= 0:
        return "death"
    return "everybody lives!"
