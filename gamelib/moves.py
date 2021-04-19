class pkmnMove():
    def __init__(self, power, melee, burst, range):
        # power is a numerical value between 1 and 100
        # melee and burst is a boolean
        # range is the range of the move. If Melee = False, range should equal 1
        self.power = power
        self.melee = melee
        self.range = range
        self.burst = burst


m_ForcePalm = pkmnMove(60, True, False, 1)  # Riolu
m_DiamondStorm = pkmnMove(100, False, True, 1)  # Diancie
m_FirePunch = pkmnMove(50, True, False, 1)  # Darumaka
m_None = pkmnMove(0, False, False, 0)  # Training Dummy