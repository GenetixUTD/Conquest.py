from gamelib import moves
import random
import os
import pygame


pygame.init()

filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class pkmnClass:
    def __init__(self, species, move, type, stats, level, LevelUpStats, exp, range, image):  # 'stats' and 'LevelUpStats' expects a list (Health, Attack, Defense, Speed) in that order
        self.species = species
        self.move = move
        self.type = type
        self.stats = stats
        self.level = level
        self.exp = exp
        self.movement = range
        self.image = image
        self.maxHP = stats[0]
        self.currentHP = self.maxHP
        self.pos = [0, 0]
        self.moved = False
        self.levelupstats = LevelUpStats
        self.buffduration = 0
        self.buffstat = 0
        self.buffincrease = 0


    def levelUp(self):
        while self.exp >= 100:
            self.stats[0] = self.stats[0] + self.levelupstats[0]
            self.stats[1] = self.stats[1] + self.levelupstats[1]
            self.stats[2] = self.stats[2] + self.levelupstats[2]
            self.stats[3] = self.stats[3] + self.levelupstats[3]
            increase = random.randint(0,3)
            self.stats[increase] = self.stats[increase] + 1
            self.level = self.level + 1
            self.exp = self.exp - 100

    def setHP(self, hp):
        self.currentHP = hp
        if self.currentHP < 0:
            self.currentHP = 0

    def setPos(self, position):
        self.pos[0] = position[0]
        self.pos[1] = position[1]

    def getPos(self):
        return self.pos

    def updatebuff(self):
        if self.buffduration > 0:
            self.buffduration -= 1
        else:
            self.buffduration = 0
        if self.buffduration == 0:
            self.buffstat = 0
            self.buffincrease = 0


unitRiolu = pkmnClass("Riolu", moves.m_ForcePalm, "Fighting", [30, 30, 20, 30], 1, [1, 2, 1, 2], 500, 4, pygame.image.load(os.path.join(filepath, "graphics", "pokemon", "riolu.png")))
unitRiolu.levelUp()
trainingDummy = pkmnClass("Training Dummy", moves.m_None, "Normal", [50, 0, 30, 0], 1, [1, 1, 1, 1], 500, 0, pygame.image.load(os.path.join(filepath, "graphics", "pokemon", "Training Dummy.png")))
trainingDummy.levelUp()
unitDarumaka = pkmnClass("Darumaka", moves.m_FirePunch, "Fire", [30, 30, 30, 20], 1, [2, 2, 1, 1], 500, 3, pygame.image.load(os.path.join(filepath, "graphics", "pokemon", "darumaka.png")))
unitDarumaka.levelUp()



#unitGardevoir = pkmnClass("Gardevoir", moves.m_Psychic, "Psychic", [30, 40, 10, 40], 1, [2, 2, 1, 1], 400, 4, pygame.image.load(os.path.join("graphics", "pokemon", "gardevoir.png")))
#unitGardevoir.levelUp()
#unitDiancie = pkmnClass("Diancie", moves.m_DiamondStorm, "Rock",)

