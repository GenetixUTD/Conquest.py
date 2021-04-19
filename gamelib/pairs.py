from gamelib import moves, pkmnObject


class WarriorPair:
    def __init__(self, wName, wGender, pkmn, skill):
        self.WarriorName = wName
        self.WarriorGender = wGender
        self.PairPokemon = pkmn
        self.WarriorSkill = skill
        self.UntappedSkill = True


class WarriorSkill:
    def __init__(self, name, stat, increase, duration): # Stat: 1: Health 2: Attack, 3: Defense 4:Evasiveness 5: Critical Strike
        self.name = name
        self.stat = stat
        self.increase = increase
        self.duration = duration

    def activate(self, target):
        if self.stat == 1:
            target.currentHP += self.increase
        else:
            target.buffstat = self.stat
            target.buffincrease = self.increase
            target.buffduration = self.duration


# --- Warrior Skills --- #
criticalcall = WarriorSkill("Critical Call", 5, 0, 1)
flashspeed = WarriorSkill("Flash Speed", 4, 0, 1)

# --- Warrior Pairs --- #
MainCharacterPair = WarriorPair("X", "ambiguous", pkmnObject.unitRiolu, criticalcall)
AlecDarumakaPair = WarriorPair("Alec", "Male", pkmnObject.unitDarumaka, flashspeed)
allpairs = [MainCharacterPair, AlecDarumakaPair]


# --- Password Pairs --- #
#JacobPair = WarriorPair("Jacob", "Male", pkmnObject.unitGardevoir)