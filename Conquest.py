import pygame
from pygame.locals import *
import os
from gamelib import pkmnObject, damageCalc, pygame_textinput, pairs, Pathfinding
import wx
import shelve

shelveSafeFile = shelve.open('dataSaveFile')
cursorX = 780
cursorY = 320

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.font.init()
app = wx.App()
WXFontTest = wx.Font(pointSize=20, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, faceName='InconsolataR')
dc = wx.ScreenDC()
dc.SetFont(WXFontTest)
app = wx.App()

displayWidth = 1280
displayHeight = 720
black = (0, 0, 0)
white = (255, 255, 255)

# Backgrounds

waterBackground = pygame.image.load(os.path.join("graphics", "backgrounds", "water.png"))
fireBackground = pygame.image.load(os.path.join("graphics", "backgrounds", "fire.png"))
grassBackground = pygame.image.load(os.path.join("graphics", "backgrounds", "grass.png"))
normalBackground = pygame.image.load(os.path.join("graphics", "backgrounds", "normal.png"))
skyBackground = pygame.image.load(os.path.join("graphics", "backgrounds", "sky.png"))
nightBackground = pygame.image.load(os.path.join("graphics", "backgrounds", "night.png"))
warriorBackground = pygame.image.load(os.path.join("graphics", "backgrounds", "warrior.jpg"))

# Sound

cursorselectSound = pygame.mixer.Sound(os.path.join("sound", "cursor-select.wav"))

textboxImage = pygame.image.load(os.path.join("graphics", "Textbox.png"))

arrowImage = pygame.image.load(os.path.join("graphics", "arrow.png"))
arrowImage = pygame.transform.scale(arrowImage, (40, 40))


def background_blit(background):
    toBlit = pygame.transform.scale(background, (960,720))
    display.blit(toBlit, (320, 0))


def reconstructTutorialBattlefield():
    display.blit(battleground, (320, 0))
    updateunitposition(pkmnObject.unitRiolu)
    updateunitposition(pkmnObject.trainingDummy)
    blitcursorcoods(cursorstartX, cursorstartY)
    pygame.display.update()

def reconstructFireBattlefield():
    display.blit(battleground, (320, 0))
    updateunitposition(pkmnObject.unitRiolu)
    updateunitposition(pkmnObject.unitDarumaka)
    blitcursorcoods(cursorstartX, cursorstartY)
    pygame.display.update()


def checkposition(pos, target, unit):
    if unit == 0:
        return True
    deltax = abs(pos[0] - target[0])
    deltay = abs(pos[1] - target[1])
    print("X:", deltax, "Y:", deltay)
    print("Original Position:", pos)
    print("Target Position:", target)
    if deltax + deltay > unit.movement:
        return False
    else:
        return True


warriorDisplayImage = pygame.image.load(os.path.join("graphics", "warriorDisplay.png"))
# Defining variables that determine what points the code has reached.
Running = True
intro = True
menu = True
gender = True
characterCreation = True
genderpicked = False
mcgender = "Null"
displaycharactercreation = True
creating_character = True
creating = True
event = pygame.event.wait()
key = pygame.key.get_pressed()
namePicking = False
genderConfirming = True
nameInput = pygame_textinput.TextInput(font_size=40, text_color=(255, 0, 0), font_family="lunchds.ttf")
clock = pygame.time.Clock()
introCutscene = True
tutorialfighting = False
UnitPickedUp = False
textFont = pygame.font.Font(os.path.join("InconsolataR.ttf"), 20)
fighting = True
displayskilltutorial = True
displaymovementtutorial = True
betweenbattlecutscene = True
dirx = 0
diry = 0

# Defining a text initialiser


def initTextbox(background=""):
    initY = 720
    while initY != 480:
        if background != "":
            display.blit(warriorBackground, (0,0))
            display.blit(background, (320,0))
        display.blit(textboxImage, (375, initY))
        pygame.display.update()
        initY = initY - 1

def emptyTextbox():
    display.blit(textboxImage, (375, 480))
    pygame.display.update()

def displaytext(text):
    print(dc.GetTextExtent(text))
    mytext = text
    calculating = True
    returnedlist = []
    while calculating:
        cut = False
        toblit = ""
        if not mytext:
            calculating = False
        for x in mytext:
            if x != " ":
                toblit += x
                #print("Added")
            elif x == " ":
                toblit += x
                #print("Space encountered")
                if dc.GetTextExtent(toblit)[0] > 800:
                    cut = True
                    ' '.join(toblit.split(' ')[:-1])
                if cut:
                    returnedlist.append(toblit)
            if cut == True:
                mytext = mytext.replace(toblit, "")
                break
        if cut == False:
            returnedlist.append(toblit)
            calculating = False

    return returnedlist


# Defining a text organiser


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def blittext(list): # expects the list from the displaytext() function
    z = 490
    for i in list:
        text = ""
        for letter in i:
            #print("blitting")
            text += letter
            textFont = pygame.font.Font(os.path.join("InconsolataR.ttf"), 20)
            textblit = textFont.render(text, True, (255,255,255))
            display.blit(textblit, (400, z))
            pygame.display.update()
        z += 40


def textboxCharacters(Leftlist, Rightlist):
    y = 0
    for i in Leftlist:
        current = i
        i = pygame.transform.scale(i, (166, 220))
        blity = 500 - 240
        blitx = (y * 180) + 375
        display.blit(i, (blitx, blity))
        pygame.display.update()
        y = y + 1
    for i in Rightlist:
        current = i
        i = pygame.transform.scale(i, (166, 220))
        height = current.get_height()
        blity = 720 - (height + 10)
        blitx = 1250 - (y * 166)
        display.blit(i, (blitx, blity))
        pygame.display.update()

# Defining a fade function


def fade(direction, image="", coords=(0,0)):
    if direction == "Out":
        black = (0, 0, 0)
        fade_opacity = 0
        fading = True
        while fading:
            fade_opacity += 1
            fadeshape = pygame.Surface((1280, 720))
            fadeshape.set_alpha(fade_opacity)
            fadeshape.fill(black)
            display.blit(fadeshape, (0,0))
            if image != "":
                display.blit(image, coords)
            pygame.display.update()
            if fade_opacity == 100:
                fading = False
    elif direction == "In":
        black = (0, 0, 0)
        fade_opacity = 100
        fading = True
        while fading:
            fade_opacity -= 1
            fadeshape = pygame.Surface((1280,720))
            fadeshape.set_alpha(fade_opacity)
            fadeshape.fill(black)
            display.blit(fadeshape, (0,0))
            pygame.display.update()
            if fade_opacity == 0:
                fading = False

def blitcursorcoods(x, y):
    x = x - 20
    y = y - 40
    display.blit(arrowImage, (x, y))

def updateunitposition(unit):
    xpos = unit.pos[0]
    ypos = unit.pos[1]
    xplacement = (120 * xpos) + 320
    yplacement = (120 * ypos)
    textblit = textFont.render(str(unit.currentHP), True, (0, 0, 0))
    display.blit(textblit, (xplacement, yplacement))
    display.blit(unit.image, (xplacement, yplacement))

# Creating window and defining images
display = pygame.display.set_mode((displayWidth, displayHeight))


pygame.display.set_caption("Conquest")
clock = pygame.time.Clock()

playButton = pygame.image.load(os.path.join("Graphics", "play button.png"))
mainscreen = pygame.image.load(os.path.join("Graphics","mainmenu.jpg"))
logo = pygame.image.load(os.path.join("Graphics","logo.png"))
backImg = pygame.image.load(os.path.join("Graphics", "Back.png"))
backImg = pygame.transform.scale(backImg, (50,50))


while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        print(event)

    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    # Main menu follows ----------------
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        display.fill(white)
        largeText = pygame.font.Font("lunchds.ttf", 60)
        TextSurf, TextRect = text_objects("Tech Demo", largeText, black)
        TextSurf = pygame.transform.rotate(TextSurf, 15)
        TextRect.center = ((displayWidth*0.68), (displayHeight*0.4))
        playpos = (((displayWidth/2)-100), (displayHeight)*0.7)
        display.blit(mainscreen, (0,0))
        display.blit(playButton, playpos)
        display.blit(logo, ((displayWidth*0.2), (displayHeight*0.35)))
        display.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        print(click)
        print(mouse)

        if 580 < mouse[0] < 710 and 532 < mouse[1] < 674:
            if click[0] == 1:
                pygame.mixer.Sound.play(cursorselectSound)
                pygame.mixer.music.stop()
                print("Start Game")
                fade(direction="Out")
                menu = False
        pygame.display.update()
        clock.tick(500)

    while characterCreation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gender_symbols = pygame.image.load(os.path.join("graphics", "Gender Symbols.png"))
        creation_background = pygame.image.load(os.path.join("graphics", "creationbackground.jpg"))
        TextSurf, TextRect = text_objects("Choose your gender", pygame.font.Font("lunchds.ttf", 60), white)

        display.blit(creation_background, (0, 0))
        display.blit(TextSurf, (((1280 / 2) - 500), displayHeight * 0.1))
        display.blit(gender_symbols, (340, (displayHeight * 0.6)))
        pygame.display.update()
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        characterCreation = False
        genderpicked = False

    print("I have broken out of the character creation loop.")

    while genderpicked == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            print(event)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 365 < mouse[0] < 602 and 457 < mouse[1] < 702 and click[0] == 1:
            mcgender = "Female"
            print(mcgender)
            pygame.mixer.Sound.play(cursorselectSound)
            pygame.mixer.music.stop()
            fade(direction="Out")
            genderpicked = True
            genderConfirming = True

        elif 457 < mouse[1] < 702 and 677 < mouse[0] < 916 and click[0] == 1:
            mcgender = "Male"
            print(mcgender)
            pygame.mixer.Sound.play(cursorselectSound)
            pygame.mixer.music.stop()
            fade(direction="Out")
            genderpicked = True
            genderConfirming = True

    if mcgender == "Male":
        characterImage = pygame.image.load(os.path.join("graphics", "maleWarlord.png"))
        characterImage = pygame.transform.scale(characterImage, (560, 800))
    elif mcgender == "Female":
        characterImage = pygame.image.load(os.path.join("Graphics", "femaleWarlord.png"))
    else:
        genderpicked = False

    display.blit(creation_background,(0,0))
    display.blit(backImg, (0,0))
    display.blit(characterImage,(322,0))
    pygame.display.update()

    while genderConfirming:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            print(event)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if 0 < mouse[0] < 50 and 0 < mouse[1] < 50 and click[0] == 1:
            characterCreation = True
            genderConfirming = False
        if keys[pygame.K_RETURN]:
            fade("Out", image=characterImage, coords=(322,0))
            fade("Out")
            TextSurf, TextRect = text_objects("What is their name? ", pygame.font.Font("lunchds.ttf", 40), white)
            display.blit(TextSurf, (50,100))
            pygame.display.update()
            genderConfirming = False
            namePicking = True

    while namePicking:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            print(event)

        display.fill((0,0,0))
        TextSurf, TextRect = text_objects("What is their name? ", pygame.font.Font("lunchds.ttf", 40), white)
        display.blit(characterImage, (500, 0))
        display.blit(TextSurf, (50, 100))
        nameInput.update(events)
        display.blit(nameInput.get_surface(), (100,130))
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            playerCharacterName = str(nameInput.get_text())
            pygame.mixer.Sound.play(cursorselectSound)
            pygame.mixer.music.stop()
            if mcgender == "Male":
                characterSprite = pygame.image.load(os.path.join("graphics", "maleWarlordSprite.png"))
            elif mcgender == "Female":
                characterSprite = pygame.image.load(os.path.join("graphics", "femaleWarlordSprite.png"))
            fade(direction="out")
            introCutscene = False
            namePicking = False
    cutscenePart = 1
    while not introCutscene:
        while cutscenePart == 1:
            display.blit(warriorBackground, (0,0))
            background_blit(normalBackground)
            display.blit(warriorDisplayImage, (0,0))
            initTextbox()
            pygame.display.update()
            cutscenePart = 2
        while cutscenePart == 2:
            cutsceneText = displaytext("Welcome to Aurora, representing kingdom behind the force that once united the region of Ransei. Blah, blah, blah, blah, blah, blah, blah") # (400, 490)
            print(cutsceneText)
            blittext(cutsceneText)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        emptyTextbox()
                        cutscenePart = 3
                        waiting = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
        while cutscenePart == 3:
            cutsceneText = displaytext("<<Aurora Training Halls>>")
            print(cutsceneText)
            blittext(cutsceneText)
            leftsideblit = [characterSprite]
            textboxCharacters(leftsideblit, ())
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        emptyTextbox()
                        cutscenePart = 4
                        waiting = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    print(event)
        while cutscenePart == 4:
            cutsceneText = displaytext(('This story follows a Aurorian Knight named '+ playerCharacterName + ', training alone within the Aurora Training Halls. Guards are on high alert, as the following day marks the princess\'s coronation.'))
            print(cutsceneText)
            blittext(cutsceneText)
            leftsideblit = [characterSprite]
            textboxCharacters(leftsideblit, ())
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        emptyTextbox()
                        cutscenePart = 5
                        waiting = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
        while cutscenePart == 5:
            cutsceneText = displaytext(('As the day drew closer ' + playerCharacterName + ' only thought of improving themselves to the point of perfection, along with their partner, Riolu.'))
            print(cutsceneText)
            blittext(cutsceneText)
            leftsideblit = [characterSprite]
            textboxCharacters(leftsideblit, ())
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        emptyTextbox()
                        introCutscene = True
                        cutscenePart = 6
                        waiting = False
                        tutorialfighting = True
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

    while tutorialfighting: # Defining the point at which the tutorial begins to get set up
        print("Tutorial")
        battleground = pygame.image.load(os.path.join("graphics", "battlegrounds", "tutorialmap.png"))
        battleground = pygame.transform.scale(battleground, (960, 720))
        display.blit(battleground, (320, 0))
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        pkmnObject.unitRiolu.setPos([4, 1])
        pkmnObject.trainingDummy.setPos([1, 4])
        pickedUpUnit = 0
        cursorstartX = 860
        cursorstartY = 150
        cursorcoodX = 4
        cursorcoodY = 1
        blitcursorcoods(cursorstartX, cursorstartY)
        updateunitposition(pkmnObject.unitRiolu)
        updateunitposition(pkmnObject.trainingDummy)
        pygame.display.update()
        change = False
        originalpos = [pkmnObject.unitRiolu.pos[0], pkmnObject.unitRiolu.pos[1]]
        targetposition = [pkmnObject.unitRiolu.pos[0], pkmnObject.unitRiolu.pos[1]]
        print(originalpos)
        while fighting: # Beginning the fight
            key = pygame.key.get_pressed()
            for event in pygame.event.get(): # Checking user inputs against allowed ones
                if event.type == KEYDOWN and event.key == pygame.K_w:
                    collateral = targetposition
                    targetposition = [targetposition[0], targetposition[1] - 1]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartY = cursorstartY - 120
                        cursorcoodY = cursorcoodY - 1
                        change = True
                        if cursorstartY < 30:
                            cursorstartY = 30
                            cursorcoodY = 0
                        if cursorcoodY == pkmnObject.trainingDummy.pos[1] and cursorcoodX == pkmnObject.trainingDummy.pos[0]:
                            cursorstartY += 120
                            cursorcoodY += 1
                    else:
                        targetposition = collateral
                elif event.type == KEYDOWN and event.key == pygame.K_a:
                    collateral = targetposition
                    targetposition = [targetposition[0] - 1, targetposition[1]]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartX = cursorstartX - 120
                        cursorcoodX = cursorcoodX - 1
                        change = True
                        if cursorstartX < 380:
                            cursorstartX = 380
                            cursorcoodX = 0
                        if cursorcoodY == pkmnObject.trainingDummy.pos[1] and cursorcoodX == pkmnObject.trainingDummy.pos[0]:
                            cursorstartX += 120
                            cursorcoodX += 1
                    else:
                        targetposition = collateral
                elif event.type == KEYDOWN and event.key == pygame.K_s:
                    collateral = targetposition
                    targetposition = [targetposition[0], targetposition[1] + 1]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartY = cursorstartY + 120
                        cursorcoodY = cursorcoodY + 1
                        change = True
                        if cursorstartY > 630:
                            cursorstartY = 630
                            cursorcoodY = 5
                        if cursorcoodY == pkmnObject.trainingDummy.pos[1] and cursorcoodX == pkmnObject.trainingDummy.pos[0]:
                            cursorstartY -= 120
                            cursorcoodY -= 1
                    else:
                        targetposition = collateral
                elif event.type == KEYDOWN and event.key == pygame.K_d:
                    collateral = targetposition
                    targetposition = [targetposition[0] + 1, targetposition[1]]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartX = cursorstartX + 120
                        cursorcoodX = cursorcoodX + 1
                        change = True
                        if cursorstartX > 1220:
                            cursorstartX = 1220
                            cursorcoodX = 7
                        if cursorcoodY == pkmnObject.trainingDummy.pos[1] and cursorcoodX == pkmnObject.trainingDummy.pos[0]:
                            cursorstartX -= 120
                            cursorcoodX -= 1
                    else:
                        targetposition = collateral
                blitcursorcoods(cursorstartX, cursorstartY)
                if change:
                    display.blit(battleground, (320, 0))
                    updateunitposition(pkmnObject.unitRiolu)
                    updateunitposition(pkmnObject.trainingDummy)
                    change = False
                pygame.display.update()
                if displaymovementtutorial:
                    initTextbox()
                    text = displaytext("Navigate to your unit and use the Enter key to interact, then use WASD to move, and finally Enter once more to confirm its position.")
                    blittext(text)
                    pygame.time.delay(3000)
                    reconstructTutorialBattlefield()
                    displaymovementtutorial = False
                if pkmnObject.trainingDummy.currentHP != 50 and displayskilltutorial:
                    initTextbox()
                    text = displaytext("Remember your training! Critical Call is a skill that will guarantee your next attack will be a critical hit! Be careful though! You can only use each warrior skill once per battle!")
                    blittext(text)
                    pygame.time.delay(3000)
                    reconstructTutorialBattlefield()
                    displayskilltutorial = False
                if event.type == KEYDOWN and event.key == pygame.K_RETURN:
                    if cursorcoodX == pkmnObject.unitRiolu.pos[0] and cursorcoodY == pkmnObject.unitRiolu.pos[1] and pkmnObject.unitRiolu.moved != True: # Checking to see if the unit is able to be moved again
                        if not UnitPickedUp:
                            pickedUpUnit = pkmnObject.unitRiolu
                            originalpos = [pkmnObject.unitRiolu.pos[0], pkmnObject.unitRiolu.pos[1]]
                            targetposition = originalpos
                            dirx = 0
                            diry = 0
                            UnitPickedUp = True
                        elif UnitPickedUp:
                            pickedUpUnit.moved = True
                            if pickedUpUnit.moved:
                                if pkmnObject.trainingDummy.currentHP == 50:
                                    textblit = textFont.render("Wait: X\nFight: Z\nReturn: C", True, (0, 0, 0))
                                else:
                                    textblit = textFont.render("Wait: X\nFight: Z\nReturn: C\nSkill:V", True, (0, 0, 0)) # Opening menu upon player placing down unit
                                display.blit(textblit, (cursorstartX + 100, cursorstartY))
                                pygame.display.update()#
                                waiting = True
                                while waiting: # Awaiting a menu input
                                    key = pygame.key.get_pressed()
                                    for event in pygame.event.get():
                                        if event.type == KEYDOWN and event.key == pygame.K_c:
                                            pickedUpUnit.moved = False
                                            waiting = False
                                        if event.type == KEYDOWN and event.key == pygame.K_x:
                                            pickedUpUnit = 0
                                            UnitPickedUp = False
                                            waiting = False
                                        if event.type == KEYDOWN and event.key == pygame.K_v and pkmnObject.trainingDummy.currentHP != 50:
                                            reconstructTutorialBattlefield()
                                            searching = True
                                            while searching:
                                                print("Searching")
                                                for i in range(0, len(pairs.allpairs)):
                                                    print("Found")
                                                    if pairs.allpairs[i].PairPokemon == pickedUpUnit and pairs.allpairs[i].UntappedSkill == True:
                                                        skill = pairs.allpairs[i].WarriorSkill
                                                        skill.activate(pickedUpUnit)
                                                        reconstructTutorialBattlefield()
                                                        print(skill.name)
                                                        textblit = textFont.render(str(skill.name)+ " activated!", True, (0, 0, 0))
                                                        display.blit(textblit, (400, 0))
                                                        pygame.display.update()
                                                        pygame.time.delay(2000)
                                                        reconstructTutorialBattlefield()
                                                        textblit = textFont.render("Wait: X\nFight: Z\nReturn: C\nSkill:V", True, (0, 0, 0))
                                                        display.blit(textblit, (cursorstartX + 100, cursorstartY))
                                                        pygame.display.update()
                                                        searching = False
                                        if event.type == KEYDOWN and event.key == pygame.K_z:
                                            reconstructTutorialBattlefield()
                                            textblit = textFont.render("Select Direction to attack in: W A S D", True, (0, 0, 0))
                                            display.blit(textblit, (cursorstartX + 100, cursorstartY))
                                            pygame.display.update()
                                            waiting = True
                                            while waiting: # Checking if an opponent is in the adjacent direction
                                                key = pygame.key.get_pressed()
                                                for event in pygame.event.get():
                                                    if event.type == KEYDOWN:
                                                        if event.key == pygame.K_w:
                                                            if pkmnObject.unitRiolu.pos[1] == (pkmnObject.trainingDummy.pos[1] + pkmnObject.unitRiolu.move.range): # Is the defending unit in range?
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.trainingDummy) # Damage function that will edit the unit's attributes.
                                                                reconstructTutorialBattlefield() # Will remove menu text
                                                            pkmnObject.unitRiolu.moved = True # The unit has been moved and can no longer perform an action this turn.
                                                            waiting = False # No longer waiting for user input; Free to exit the for loop.
                                                        if event.key == pygame.K_a:
                                                            if pkmnObject.unitRiolu.pos[0] == (pkmnObject.trainingDummy.pos[0] + pkmnObject.unitRiolu.move.range):
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.trainingDummy)
                                                                reconstructTutorialBattlefield()
                                                            pkmnObject.unitRiolu.moved = True
                                                            waiting = False
                                                        if event.key == pygame.K_s:
                                                            if pkmnObject.unitRiolu.pos[1] == (pkmnObject.trainingDummy.pos[1] - pkmnObject.unitRiolu.move.range):
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.trainingDummy)
                                                                reconstructTutorialBattlefield()
                                                            pkmnObject.unitRiolu.moved = True
                                                            waiting = False
                                                        if event.key == pygame.K_d:
                                                            if pkmnObject.unitRiolu.pos[0] == (pkmnObject.trainingDummy.pos[0] - pkmnObject.unitRiolu.move.range):
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.trainingDummy)
                                                                reconstructTutorialBattlefield()
                                                            pkmnObject.unitRiolu.moved = True
                                                            waiting = False

            if pickedUpUnit != 0:  # Comparison statement that makes edits the pickedupunit's current position.
                pickedUpUnit.setPos([cursorcoodX, cursorcoodY]) # Sets the unit's position to the cursor's.
                display.blit(battleground, (320, 0))
                updateunitposition(pkmnObject.unitRiolu) # Updates the position on the screen after altering attribute within the class.
                updateunitposition(pkmnObject.trainingDummy)
                blitcursorcoods(cursorstartX, cursorstartY)
            pygame.display.update()

            if pkmnObject.unitRiolu.moved:  # Comparison that automatically ends the turn if all units have been moved.
                pkmnObject.unitRiolu.updatebuff()
                print(pkmnObject.trainingDummy.currentHP)
                if pkmnObject.trainingDummy.currentHP == 0: # Condition to end the battle
                    tutorialfighting = False
                    fighting = False
                    break
                textblit = textFont.render("Enemy Turn", True, (0, 0, 0))
                display.blit(textblit, (750, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                reconstructTutorialBattlefield()
                textblit = textFont.render("Player Turn", True, (0, 0, 0))
                display.blit(textblit, (750, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                reconstructTutorialBattlefield()
                pickedUpUnit = 0
                UnitPickedUp = False
                pkmnObject.unitRiolu.moved = False

    cutscenePart = 1
    while betweenbattlecutscene:
        while cutscenePart == 1:
            background_blit(normalBackground)
            pygame.display.update()
            initTextbox()
            cutsceneText = displaytext(("Their training was done."))
            print(cutsceneText)
            blittext(cutsceneText)
            leftsideblit = [characterSprite]
            textboxCharacters(leftsideblit, ())
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        emptyTextbox()
                        fighting = True
                        betweenbattlecutscene = False
                        cutscenePart = 2
                        waiting = False
                        firekingdomfighting = True
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

    while firekingdomfighting:
        display.blit(battleground, (320, 0))
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        pkmnObject.unitRiolu.setPos([5, 1])
        pkmnObject.unitDarumaka.setPos([1, 5])
        pickedUpUnit = 0
        cursorstartX = 980
        cursorstartY = 150
        cursorcoodX = 5
        cursorcoodY = 1
        blitcursorcoods(cursorstartX, cursorstartY)
        updateunitposition(pkmnObject.unitRiolu)
        updateunitposition(pkmnObject.unitDarumaka)
        pygame.display.update()
        change = False
        originalpos = [pkmnObject.unitRiolu.pos[0], pkmnObject.unitRiolu.pos[1]]
        targetposition = [pkmnObject.unitRiolu.pos[0], pkmnObject.unitRiolu.pos[1]]
        print(originalpos)
        while fighting:
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_w:
                    collateral = targetposition
                    targetposition = [targetposition[0], targetposition[1] - 1]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartY = cursorstartY - 120
                        cursorcoodY = cursorcoodY - 1
                        change = True
                        if cursorstartY < 30:
                            cursorstartY = 30
                            cursorcoodY = 0
                        if cursorcoodY == pkmnObject.unitDarumaka.pos[1] and cursorcoodX == pkmnObject.unitDarumaka.pos[0]:
                            cursorstartY += 120
                            cursorcoodY += 1
                    else:
                        targetposition = collateral
                elif event.type == KEYDOWN and event.key == pygame.K_a:
                    collateral = targetposition
                    targetposition = [targetposition[0] - 1, targetposition[1]]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartX = cursorstartX - 120
                        cursorcoodX = cursorcoodX - 1
                        change = True
                        if cursorstartX < 380:
                            cursorstartX = 380
                            cursorcoodX = 0
                        if cursorcoodY == pkmnObject.unitDarumaka.pos[1] and cursorcoodX == pkmnObject.unitDarumaka.pos[0]:
                            cursorstartX += 120
                            cursorcoodX += 1
                    else:
                        targetposition = collateral
                elif event.type == KEYDOWN and event.key == pygame.K_s:
                    collateral = targetposition
                    targetposition = [targetposition[0], targetposition[1] + 1]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartY = cursorstartY + 120
                        cursorcoodY = cursorcoodY + 1
                        change = True
                        if cursorstartY > 630:
                            cursorstartY = 630
                            cursorcoodY = 5
                        if cursorcoodY == pkmnObject.unitDarumaka.pos[1] and cursorcoodX == pkmnObject.unitDarumaka.pos[0]:
                            cursorstartY -= 120
                            cursorcoodY -= 1
                    else:
                        targetposition = collateral
                elif event.type == KEYDOWN and event.key == pygame.K_d:
                    collateral = targetposition
                    targetposition = [targetposition[0] + 1, targetposition[1]]
                    check = checkposition(originalpos, targetposition, pickedUpUnit)
                    if check:
                        cursorstartX = cursorstartX + 120
                        cursorcoodX = cursorcoodX + 1
                        change = True
                        if cursorstartX > 1220:
                            cursorstartX = 1220
                            cursorcoodX = 7
                        if cursorcoodY == pkmnObject.unitDarumaka.pos[1] and cursorcoodX == pkmnObject.unitDarumaka.pos[0]:
                            cursorstartX -= 120
                            cursorcoodX -= 1
                    else:
                        targetposition = collateral
                blitcursorcoods(cursorstartX, cursorstartY)
                if change:
                    display.blit(battleground, (320, 0))
                    updateunitposition(pkmnObject.unitRiolu)
                    updateunitposition(pkmnObject.unitDarumaka)
                    change = False
                pygame.display.update()
                if event.type == KEYDOWN and event.key == pygame.K_RETURN:
                    if cursorcoodX == pkmnObject.unitRiolu.pos[0] and cursorcoodY == pkmnObject.unitRiolu.pos[1] and pkmnObject.unitRiolu.moved != True:  # Checking to see if the unit is able to be moved again
                        if not UnitPickedUp:
                            pickedUpUnit = pkmnObject.unitRiolu
                            originalpos = [pkmnObject.unitRiolu.pos[0], pkmnObject.unitRiolu.pos[1]]
                            targetposition = originalpos
                            dirx = 0
                            diry = 0
                            UnitPickedUp = True
                        elif UnitPickedUp:
                            pickedUpUnit.moved = True
                            if pickedUpUnit.moved:
                                textblit = textFont.render("Wait: X\nFight: Z\nReturn: C\nSkill:V", True, (0, 0, 0))  # Opening menu upon player placing down unit
                                display.blit(textblit, (cursorstartX + 100, cursorstartY))
                                pygame.display.update()
                                waiting = True
                                while waiting:  # Awaiting a menu input
                                    key = pygame.key.get_pressed()
                                    for event in pygame.event.get():
                                        if event.type == KEYDOWN and event.key == pygame.K_c:
                                            pickedUpUnit.moved = False
                                            waiting = False
                                        if event.type == KEYDOWN and event.key == pygame.K_x:
                                            pickedUpUnit = 0
                                            UnitPickedUp = False
                                            waiting = False
                                        if event.type == KEYDOWN and event.key == pygame.K_v:
                                            reconstructFireBattlefield()
                                            searching = True
                                            while searching:
                                                print("Searching")
                                                for i in range(0, len(pairs.allpairs)):
                                                    print("Found")
                                                    if pairs.allpairs[i].PairPokemon == pickedUpUnit and pairs.allpairs[
                                                        i].UntappedSkill == True:
                                                        skill = pairs.allpairs[i].WarriorSkill
                                                        skill.activate(pickedUpUnit)
                                                        reconstructFireBattlefield()
                                                        print(skill.name)
                                                        textblit = textFont.render(str(skill.name) + " activated!", True, (0, 0, 0))
                                                        display.blit(textblit, (400, 0))
                                                        pygame.display.update()
                                                        pygame.time.delay(2000)
                                                        reconstructFireBattlefield()
                                                        textblit = textFont.render("Wait: X\nFight: Z\nReturn: C\nSkill:V", True, (0, 0, 0))
                                                        display.blit(textblit, (cursorstartX + 100, cursorstartY))
                                                        pygame.display.update()
                                                        searching = False
                                        if event.type == KEYDOWN and event.key == pygame.K_z:
                                            reconstructFireBattlefield()
                                            textblit = textFont.render("Select Direction to attack in: W A S D", True, (0, 0, 0))
                                            display.blit(textblit, (cursorstartX + 100, cursorstartY))
                                            pygame.display.update()
                                            waiting = True
                                            while waiting:  # Checking if an opponent is in the adjacent direction
                                                key = pygame.key.get_pressed()
                                                for event in pygame.event.get():
                                                    if event.type == KEYDOWN:
                                                        if event.key == pygame.K_w:
                                                            if pkmnObject.unitRiolu.pos[1] == (pkmnObject.unitDarumaka.pos[1] + pkmnObject.unitRiolu.move.range):  # Is the defending unit in range?
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.unitDarumaka)  # Damage function that will edit the unit's attributes.
                                                                reconstructFireBattlefield()  # Will remove menu text
                                                            pkmnObject.unitRiolu.moved = True  # The unit has been moved and can no longer perform an action this turn.
                                                            waiting = False  # No longer waiting for user input; Free to exit the for loop.
                                                        if event.key == pygame.K_a:
                                                            if pkmnObject.unitRiolu.pos[0] == (pkmnObject.unitDarumaka.pos[0] + pkmnObject.unitRiolu.move.range):
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.unitDarumaka)
                                                                reconstructFireBattlefield()
                                                            pkmnObject.unitRiolu.moved = True
                                                            waiting = False
                                                        if event.key == pygame.K_s:
                                                            if pkmnObject.unitRiolu.pos[1] == (pkmnObject.unitDarumaka.pos[1] - pkmnObject.unitRiolu.move.range):
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.unitDarumaka)
                                                                reconstructFireBattlefield()
                                                            pkmnObject.unitRiolu.moved = True
                                                            waiting = False
                                                        if event.key == pygame.K_d:
                                                            if pkmnObject.unitRiolu.pos[0] == (pkmnObject.unitDarumaka.pos[0] - pkmnObject.unitRiolu.move.range):
                                                                damageCalc.calculateDamage(pkmnObject.unitRiolu, pkmnObject.unitDarumaka)
                                                                reconstructFireBattlefield()
                                                            pkmnObject.unitRiolu.moved = True
                                                            waiting = False

            if pickedUpUnit != 0:  # Comparison statement that makes edits the pickedupunit's current position.
                pickedUpUnit.setPos([cursorcoodX, cursorcoodY])  # Sets the unit's position to the cursor's.
                display.blit(battleground, (320, 0))
                updateunitposition(pkmnObject.unitRiolu)  # Updates the position on the screen after altering attribute within the class.
                updateunitposition(pkmnObject.unitDarumaka)
                blitcursorcoods(cursorstartX, cursorstartY)
            pygame.display.update()

            if pkmnObject.unitRiolu.moved:  # Comparison that automatically ends the turn if all units have been moved.
                pkmnObject.unitRiolu.updatebuff()
                print(pkmnObject.unitDarumaka.currentHP)
                if pkmnObject.unitDarumaka.currentHP == 0:  # Condition to end the battle
                    firekingdomfighting = False
                    fighting = False
                    break
                textblit = textFont.render("Enemy Turn", True, (0, 0, 0))
                display.blit(textblit, (750, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                temp = pkmnObject.unitDarumaka.movement
                lost = False
                fight = False
                while temp != 0 and not fight: # Movement loop for enemy unit. Checks if the enemy has moved a number of spaces equal to range
                    fight = Pathfinding.pathfinding(pkmnObject.unitDarumaka, pkmnObject.unitRiolu) # Find then next position whilst in range.
                    if fight:
                        damageCalc.calculateDamage(pkmnObject.unitDarumaka, pkmnObject.unitRiolu) # If the units are adjacent, attack and stop pathfinding
                    temp = temp - 1 # Decreases temp value by one for every space moved
                reconstructFireBattlefield()
                if pkmnObject.unitRiolu.currentHP == 0:
                    lost = True
                    firekingdomfighting = False
                    fighting = False
                    break
                textblit = textFont.render("Player Turn", True, (0, 0, 0))
                display.blit(textblit, (750, 0))
                pygame.display.update()
                pygame.time.delay(2000)
                reconstructFireBattlefield()
                originalpos = [pkmnObject.unitRiolu.pos[0], pkmnObject.unitRiolu.pos[1]]
                difx = 0
                dify = 0
                pickedUpUnit = 0
                UnitPickedUp = False
                pkmnObject.unitRiolu.moved = False

    Running = False