
def pathfinding(computerunit, goalunit):
    differenceX = computerunit.pos[0] - goalunit.pos[0]
    differenceY = computerunit.pos[1] - goalunit.pos[1]
    negX = False
    negY = False
    if differenceX < 0:
        negX = True
    if differenceY < 0:
        negY = True
    if differenceX == 0:
        differenceX = 9999
    if differenceY == 0:
        differenceY = 9999

    #-=== Next movement find ===-#
    if (differenceX == 9999 and (computerunit.pos[1] == (goalunit.pos[1] + 1) or computerunit.pos[1] == (goalunit.pos[1] - 1))) or (differenceY == 9999 and (computerunit.pos[0] == (goalunit.pos[0] + 1) or computerunit.pos[0] == (goalunit.pos[0] - 1))):
        return True # Tells the main algorithm that the two units are adjacent and can commit to an attack.
    else:
        if differenceX <= differenceY and differenceX != 9999:
            if negX: # Is the unit to the left or right
                computerunit.pos[0] += 1
            else:
                computerunit.pos[0] -= 1
        elif differenceX > differenceY and differenceY != 9999:
            if negY: # Is the unit above or below
                computerunit.pos[1] += 1
            else:
                computerunit.pos[1] -= 1
        print(computerunit.pos[0], computerunit.pos[1]) # Returns position for debugging
        return False # The units are not adjacent and cannot attack.

