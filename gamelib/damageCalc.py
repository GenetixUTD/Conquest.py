from gamelib import pkmnObject
import random
import math
import os
import pygame.mixer

pygame.mixer.init()

attackhitSound = pygame.mixer.Sound(os.path.join("sound", "attack-hit.wav"))
attackmissSound = pygame.mixer.Sound(os.path.join("sound", "attack-miss.wav"))


superEffective = {
    "Fighting": ("Flying", "Psychic", "Fairy"),
    "Rock": ("Fighting", "Ground", "Steel", "Water", "Grass"),
    "Fire": ("Ground", "Rock", "Water"),
    "Normal": ("Fighting")
}

weaklyEffective = {
    "Fighting": ("Rock", "Bug", "Dark"),
    "Rock": ("Normal", "Flying", "Poison", "Fire"),
    "Fire": ("Bug", "Steel", "Fire", "Grass", "Ice", "Fairy"),
    "Normal": ()
}


def calculateDamage(attackingunit, defendingunit):
    attackStat = attackingunit.stats[1]
    defenseStat = defendingunit.stats[2]
    defendingHP = defendingunit.currentHP
    attackmodifier = 1
    defensemodifier = 1

    # Finding Effectiveness

    superList = superEffective.get(defendingunit.type)
    weakList = weaklyEffective.get(attackingunit.type)
    if defendingunit.buffstat == 3:
        defensemodifier = defendingunit.buffincrease
    if attackingunit.buffstat == 1:
        attackmodifier = attackingunit.buffincrease
    if random.randint(0,20) == 20 or attackingunit.buffstat == 5:
        critical = 2
    else:
        critical = 1

    if attackingunit.type in superList:
        Effectiveness = 2
    elif attackingunit.type in weakList:
        Effectiveness = 0.5
    else:
        Effectiveness = 1

    unitevaisiveness = 1
    if defendingunit.buffstat == 4:
        unitevaisiveness = 5

    if random.randint(0, 100) > 10 * unitevaisiveness:
        damageDealt = ((((((2 * attackingunit.level)/5)+2) * attackingunit.move.power * ((attackStat * attackmodifier) / (defenseStat * defensemodifier))) / 50) + 2) * Effectiveness * critical
        pygame.mixer.Sound.play(attackhitSound)
        pygame.mixer.music.stop
    else:
        damageDealt = 0
        pygame.mixer.Sound.play(attackmissSound)
        pygame.mixer.music.stop

    damageDealt = math.ceil(damageDealt)
    print(damageDealt)

    HPRemaining = defendingHP - damageDealt
    pygame.mixer.Sound.play(attackhitSound)
    pygame.mixer.music.stop
    defendingunit.setHP(HPRemaining)
    print(defendingunit.currentHP)



