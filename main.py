from pygame import *
from random import *
import copy
import os
# Starting up pygame and necessary components
os.environ['SDL_VIDEO_CENTERED'] = '1'
init()
size = width, height = 800, 600
screen = display.set_mode(size)
display.set_caption("Super Mario Bros!")
display.set_icon(transform.scale(image.load("assets/sprites/mario/smallMarioJump.png"),(32,32)))

# Declaring colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKYBLUE = (107, 140, 255)

# Declaring Variables
page = "menu"
fpsCounter = time.Clock()
marioPos = [40, 496, 0, 0, "Right", 0]  # X, Y, VX, VY, direction, state
# X, Y: Variables to keep track of mario's position on screen
# VX, VY:  Variables to keep track of mario's X and Y velocity
# direction: Variable to keep track of the direction mario is facing
# state: 0 for small mario, 1 for big mario
marioStats = [True, 0, False, False, False, False, False, 0] # onGround, jumpFrames, inGround, isCrouch, onPlatform, isFalling, isAnimating, invulFrames
# onGround: Boolean to see if mario is on a solid ground
# jumpFrames: Variable to keep track of frames user has held space for
# inGround: Boolean to see if mario has fallen through the floor
# isCrouch: Boolean to see if mario is crouching
# onPlatform: Boolean to see if mario's last position was on a platform
# isFalling: Boolean to see if mario has stopped jumping and should fall
# isAnimating: Boolean to see if we need to pause the game and change mario's state
# invulFrames: Variable to keep track of the frames where mario is invulnerable
marioScore = [0, 0, 3] # Points, Coins, Lives
marioFrame = [0, 0, 0] # List to keep track of mario's sprites and his changing animation
marioAccelerate = 0.2 # The value at which mario can speed up and slow down
backPos = 0  # Position of the background
levelNum = 0  # Using 0 as level 1 since indexes start at 0

RECTFINDER = [0,0] #DELETE THIS LATER
    
# Loading Pictures
titleLogo = transform.scale(image.load("assets/sprites/title/logo.png"), (480,220))
titleSelect = transform.scale(image.load("assets/sprites/title/select.png"), (24,24))
mutePic = transform.scale(image.load("assets/sprites/title/muted.png"), (45,45))

backgroundPics = [image.load("assets/backgrounds/level_"+str(i)+".png").convert() for i in range(1,2)]

marioSpriteNames = ["smallmariojump" , "bigmariojump" , "bigmariocrouch" , "smallmariodead" , "bigmariochange", "smallmariochange"]

marioSprites = [[image.load("assets/sprites/mario/smallmario"+str(i)+".png").convert_alpha() for i in range(1,5)],
             [image.load("assets/sprites/mario/bigmario"+str(i)+".png").convert_alpha() for i in range(1,5)],
                [image.load("assets/sprites/mario/"+str(i)+".png").convert_alpha() for i in marioSpriteNames]]

brickSprites=[[image.load("assets/sprites/bricks/question"+str(i)+".png").convert_alpha() for i in range(3,0,-1)],
              [image.load("assets/sprites/bricks/brick.png").convert_alpha(),
               image.load("assets/sprites/bricks/blockidle.png").convert_alpha()]]
brickPiece = transform.scale(image.load("assets/sprites/bricks/brickpiece.png").convert_alpha(), (21,21))

statCoin = [image.load("assets/sprites/title/coin"+str(i)+".png").convert_alpha() for i in range(3,0,-1)]

coinsPic = [[image.load("assets/sprites/coins/coinidle"+str(i)+".png").convert_alpha() for i in range(3,0,-1)],
            [image.load("assets/sprites/coins/coinmove"+str(i)+".png").convert_alpha() for i in range(1,5)]]

itemsPic = [image.load("assets/sprites/items/mushroom.png").convert_alpha()]

enemiesPic = [[image.load("assets/sprites/enemies/goomba"+str(i)+'.png').convert_alpha() for i in range(1,4)]]

# Resizing, Flipping, and Reordering Pictures
backgroundPics = [transform.scale(pic,(9086,600)) for pic in backgroundPics]
statCoin = [transform.scale(pic, (15,24)) for pic in statCoin]
statCoin = statCoin + statCoin[::-1]
for subList in range(len(marioSprites)):
    for pic in range(len(marioSprites[subList])):
        if marioSprites[subList][pic].get_height() == 16:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 42))
        else:
            marioSprites[subList][pic] = transform.scale(marioSprites[subList][pic], (42, 84))

for subList in range(len(brickSprites)):
    for pic in range(len(brickSprites[subList])):
        brickSprites[subList][pic] = transform.scale(brickSprites[subList][pic], (42,42))
brickSprites[0] = brickSprites[0] + brickSprites[0][::-1]
brickPiece = [transform.flip(brickPiece, False, True),
              brickPiece,
              transform.flip(brickPiece, True, True),
              transform.flip(brickPiece, True, False)]
for subList in range(len(coinsPic)):
    for pic in range(len(coinsPic[subList])):
        coinsPic[subList][pic] = transform.scale(coinsPic[subList][pic], (30,36))
for pic in range(len(itemsPic)):
    itemsPic[pic] = transform.scale(itemsPic[pic], (42,42))
coinsPic[0] = coinsPic[0] + coinsPic[0][::-1]
for subList in range(len(enemiesPic)):
    for pic in range(len(enemiesPic[subList])):
        enemiesPic[subList][pic] = transform.scale(enemiesPic[subList][pic], (42,42))


# Declaring all fonts

marioFont = font.Font("assets/fonts/marioFont.ttf", 18)
marioFontBig = font.Font("assets/fonts/marioFont.ttf", 22)
marioFontSuperBig = font.Font("assets/fonts/marioFont.ttf", 30)

# Creating text

playText = marioFont.render("play", False, WHITE)
instructText = marioFont.render("instructions", False, WHITE)
creditText = marioFont.render("credits", False, WHITE)
quitText = marioFont.render("quit", False, WHITE)
pauseText = marioFont.render("paused", False, WHITE)
helpText = marioFont.render("press esc to exit game", False, WHITE)
marioText = marioFontBig.render("mario", False, WHITE)
timeText = marioFontBig.render("time", False, WHITE)
worldText = marioFontBig.render("world", False, WHITE)

instructHelp = marioFontSuperBig.render("Instructions", False, WHITE)
moveRightHelp = marioFont.render("Move Right  -  D", False, WHITE)
moveLeftHelp = marioFont.render("Move Left  -  A", False, WHITE)
jumpHelp = marioFont.render("Jump  -  Space", False, WHITE)
crouchHelp = marioFont.render("Crouch/Fast Fall  -  S", False, WHITE)
pauseHelp = marioFont.render("Pause  -  P", False, WHITE)
musicPauseHelp = marioFont.render("Mute/Unmute Music  -  M", False, WHITE)
backTextHelp = marioFont.render("Back",False,WHITE)

creditTitleHelp = marioFontSuperBig.render("Game Created By: ",False,WHITE)
creditTextHelp1 = marioFont.render("Armaan Randhawa",False,WHITE)
creditTextHelp2 = marioFont.render("Kevin Cui",False,WHITE)
creditTextHelp3 = marioFont.render("Henry Zhang",False,WHITE)


# Loading all sound files

pauseSound = mixer.Sound("assets/music/effects/pause.wav")
backgroundSound = mixer.Sound("assets/music/songs/mainSong.ogg")
backgroundFastSound = mixer.Sound("assets/music/songs/mainSongFast.ogg")
timeLowSound = mixer.Sound("assets/music/effects/timeLow.wav")
smallJumpSound = mixer.Sound("assets/music/effects/smallJump.ogg")
bigJumpSound = mixer.Sound("assets/music/effects/bigJump.ogg")
bumpSound = mixer.Sound("assets/music/effects/bump.ogg")
breakSound = mixer.Sound("assets/music/effects/brickBreak.ogg")
coinSound = mixer.Sound("assets/music/effects/coin.ogg")
appearSound = mixer.Sound("assets/music/effects/itemAppear.ogg")
stompSound = mixer.Sound("assets/music/effects/stomp.ogg")
growSound = mixer.Sound("assets/music/effects/grow.ogg")
shrinkSound = mixer.Sound("assets/music/effects/shrink.ogg")


# Declaring game functions
def drawScene(background, backX, mario, marioPic, marioFrame, rectList, breakingBrick, brickPic, coins, moveCoins, coinsPic, mushrooms, itemsPic, enemiesList, enemiesPic, spriteCount, isMuted):
    """Function to draw the background, mario, enemies, and all objects"""
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    BRICKVY, IDLE, TYPE = 4, 5, 6
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    screen.fill(BLACK) # Clearing screen
    screen.blit(background, (backX, 0))  # Blitting background
    marioShow = marioPic[marioFrame[0]][int(marioFrame[1])]
    if mario[DIR] == "Left":
        marioShow = transform.flip(marioShow, True, False)  # Flipping mario's sprite if he's facing left
    for coin in moveCoins:
        coinRect = coin[0], coin[1], coin[2], coin[3]
        screen.blit(coinsPic[1][int(spriteCount // 0.4 % 4)], coinRect)
    for mushroom in mushrooms:
        mushRect = Rect(mushroom[0], mushroom[1], mushroom[2], mushroom[3])
        if mushroom[4] == 0:
            screen.blit(itemsPic[0], mushRect)
    for list in enemiesList:
        for enemy in list:
            enmyRect = Rect(enemy[0], enemy[1], enemy[2], enemy[3])
            if list == goombas:
                if enemy[ENMYIDLE] == 2:
                    screen.blit(enemiesPic[0][2], enmyRect)
                else:
                    screen.blit(enemiesPic[0][int(spriteCount//6)], enmyRect)
    for list in rectList:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            if list == interactBricks:
                screen.blit(brickPic[1][0],brickRect)
            elif list == questionBricks:
                if brick[IDLE] == 1:
                    screen.blit(brickPic[1][1], brickRect)
                else:
                    screen.blit(brickPic[0][int(spriteCount//2)],brickRect)
    for brick in breakingBrick:
        drawDebris(brick)
    for coin in coins:
        coinRect = coin[0], coin[1], coin[2], coin[3]
        screen.blit(coinsPic[0][int(spriteCount // 2)], coinRect)
    if marioStats[INVULFRAMES]%2 == 0:
        screen.blit(marioShow, (mario[0], mario[1]))  # Blitting mario's sprite
    if isMuted:
        screen.blit(mutePic, (735,25))


def drawDebris(brick):
    screen.blit(brickPiece[0], (brick[0] - brick[5],brick[1]))
    screen.blit(brickPiece[1], (brick[0] + 21 + brick[5],brick[1]))
    screen.blit(brickPiece[2], (brick[0] - brick[5]/2,brick[1] + 21))
    screen.blit(brickPiece[3], (brick[0] + 21 + brick[5]/2,brick[1] + 21))
    brick[1] += brick[4]
    brick[4] += 0.8
    brick[5] += 3

def moveBricks(questionBricks, interactBricks):
    BRICKVY, IDLE, TYPE = 4, 5, 6
    for brick in questionBricks:
        if brick[BRICKVY] != 3.5 and brick[IDLE] == 1:
            brick[BRICKVY] += 0.5
            brick[1] += brick[BRICKVY]

    for brick in interactBricks:
        if brick[BRICKVY] != 3.5 and brick[IDLE] == 1:
            brick[BRICKVY] += 0.5
            brick[1] += brick[BRICKVY]
        else:
            brick[BRICKVY] = 0
            brick[IDLE] = 0


def spinCoins(moveCoins, uniSprite):
    Y, COINVY = 1, 4
    deleteList = []
    for coin in range(len(moveCoins)):
        if moveCoins[coin][COINVY] != 5:
            moveCoins[coin][COINVY] += 0.5
            moveCoins[coin][Y] += moveCoins[coin][COINVY]
        else:
            deleteList.append(coin)
    for index in deleteList:
        del moveCoins[index]

def moveItems(rectList, enemiesList, mushrooms, goombas):
    X, Y, DELAY, MOVEUP, MUSHVX, MUSHVY, INFLOOR = 0, 1, 4, 5, 6, 7, 8
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    # Making sure all mushrooms are activated
    for mushroom in mushrooms:
        if mushroom[DELAY] > 0:
            mushroom[DELAY] -= 1
        elif mushroom[MOVEUP] > 0:
            mushroom[MOVEUP] -= 1
            mushroom[1] -= 1
        else:
            itemCollide(mushroom, rectList, [X, Y, MUSHVX, MUSHVY, INFLOOR])
    for goomba in goombas:
        if goomba[ENMYIDLE] == 1:
            itemCollide(goomba, rectList, [X, Y, ENMYVX, ENMYVY, ENMYINFLOOR], enemiesList)
        if goomba[ENMYIDLE] == 2:
            goomba[ENMYINFLOOR] -=1


def itemCollide(item, rectList, indexList, extraCollideIn = []):
    X, Y, VX, VY, INFLOOR = indexList[0], indexList[1], indexList[2], indexList[3], indexList[4]
    extraCollide = copy.deepcopy(extraCollideIn)
    if extraCollide != []:
        for list in range(len(extraCollide)):
            if item in extraCollide[list]:
                del extraCollide[list][extraCollide[list].index(item)]
    rectList = rectList + extraCollide
    item[X] += item[VX]
    item[VY] += 0.6
    item[Y] += item[VY]
    if item[Y] > 496 and not item[INFLOOR]:
        item[Y] = 496
        item[VY] = 0
        itemRect = Rect(item[0] + 3, item[1], item[2] - 3, item[3])
        try:
            if itemRect.x > 0 and screen.get_at((itemRect.x, itemRect.bottom)) == SKYBLUE and screen.get_at((itemRect.right, itemRect.bottom)) == SKYBLUE:
                item[INFLOOR] = True
        except IndexError:
            pass
    itemRect = Rect(item[0], item[1], item[2], item[3])
    for list in rectList:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            if itemRect.colliderect(brickRect) and itemRect != brickRect:
                if int(item[Y]) < brickRect.y:
                    item[Y] = brickRect.y - 42
                    item[VY] = 0
                else:
                    item[VX] *= -1


def drawStats(mario, marioInfo, points, coins, startTime, level, fastMode, timesUp, coinPic, spriteCount):
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    if not fastMode:
        nowFast = False
    else:
        nowFast = True
    if not timesUp:
        timesUpCheck = False
    else:
        timesUpCheck = True
    currentTime = 200 - int((time.get_ticks() - startTime) / 1000)
    if currentTime < 100 and not fastMode:
        playSound(timeLowSound, "music")
        playSound(backgroundFastSound, "music", True)
        nowFast = True
    if currentTime == 0 and not timesUp:
        currentTime = 0
        marioInfo[ISANIMATING] = True
        mario[STATE] = -1
        timesUpCheck = True
    points = marioFontBig.render("%06i" %int(points), False, (255,255,255))
    coins =  marioFontBig.render("x%02i" %int(coins), False, (255,255,255))
    world = marioFontBig.render("1-%i" %int(level), False, (255,255,255))
    timer = marioFontBig.render("%03i" %int(currentTime), False, (255,255,255))
    screen.blit(points, (75,50))
    screen.blit(marioText, (75,25))
    screen.blit(coins, (300,50))
    screen.blit(worldText, (450,25))
    screen.blit(world, (470,50))
    screen.blit(timeText, (625,25))
    screen.blit(timer, (640, 50))
    screen.blit(coinPic[int(spriteCount//2)], (275,48))
    return nowFast, timesUpCheck

def drawPause():
    alphaSurface = Surface((800, 600))  # Making a surface
    alphaSurface.set_alpha(128)  # Giving it alpha functionality
    alphaSurface.fill((0, 0, 0))  # Fill the surface with a black background
    screen.blit(alphaSurface, (0, 0))  # Blit it into the actual screen
    # Blitting text
    screen.blit(pauseText, (345,290))
    screen.blit(helpText, (210, 330))

def moveSprites(mario, marioInfo, marioPic, frame):
    """ Function to cycle through Mario's sprites """
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    changingSprites = [[2,5], [2,4], [2,5], [2,4], [2,5], [1,0]]
    if marioInfo[ISANIMATING]:
        if frame[2] == 47:
            marioInfo[ISANIMATING] = False
            frame[2] = 0
            if mario[STATE] == 0:
                mario[Y] +=42
        if mario[STATE] == -1:  # If mario is dying, skip the moveSprites function
            frame[0], frame[1] = 2, 3
        elif mario[STATE] == 0:
            changingSprites = changingSprites[::-1]
            frame[2] += 1
            frame[0], frame[1] = changingSprites[(frame[2]//8)][0], changingSprites[(frame[2]//8)][1]
        elif mario[STATE] == 1:
            frame[2] += 1
            frame[0], frame[1] = changingSprites[(frame[2]//8)][0], changingSprites[(frame[2]//8)][1]
        return
    if marioInfo[ONGROUND]:
        frame[0] = 0 + mario[STATE] # Adjusting for sprite for = big mario
        # Mario's running sprite counter
        if frame[1] < 3.8:
            frame[1] += mario[VX]**2/100 + 0.2
        else:
            frame[1] = 1
        if frame[1] > 3.9:  # Sprite counter upper limit
            frame[1] = 3.9
        if mario[VX] == 0:  # If mario isn't moving, stay on his standing sprite
            frame[1] = 0
    else:
        frame[0],frame[1] = 2, 0 + mario[STATE]  # If mario is midair, stay on his jumping sprite
    if marioInfo[ISCROUCH]:
        frame[0],frame[1] = 2, 2  # If mario is crouching, stay on his crouching sprite
    if marioInfo[INVULFRAMES] != 0:
        marioInfo[INVULFRAMES] -= 1


def checkMovement(mario, marioInfo, acclerate, rectLists, pressSpace, clearRectList):
    """Function to accept inputs and apply the appropriate physics """
    keys = key.get_pressed()
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    moving = False
    # Walking logic
    if keys[K_a] and keys[K_d]:  # If both keys are pressed, don't move
        mario[VX] = 0
    elif keys[K_a] and not marioInfo[ISCROUCH]:  # Checking if mario is hitting left side of window
        if mario[DIR] != "Left":
            mario[VX] = 0  # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Left", clearRectList)
        moving = True
        mario[DIR] = "Left"
    elif keys[K_d] and not marioInfo[ISCROUCH]:
        if mario[DIR] != "Right":
            mario[VX] = 0  # Stop acceleration if changing direction
        walkMario(mario, rectLists, "Right", clearRectList)
        moving = True
        mario[DIR] = "Right"
    if keys[K_s] and mario[STATE]==1:  # Allow crouching if big mario is active
        marioInfo[ISCROUCH]=True
    if mario[STATE]==0 and marioInfo[ISCROUCH]:  # Don't allow small mario to be in crouching position
        marioInfo[ISCROUCH]=False
    if moving:  # Accelerate if there is input
        if marioInfo[ONGROUND]:
            mario[VX] += acclerate
        else:
            mario[VX] += acclerate/4  # Slow down movement when midair
    elif mario[VX] != 0:  # Move and decelerate if there is no input
        if mario[DIR] == "Right":
            walkMario(mario, rectLists, "Right", clearRectList)
        if mario[DIR] == "Left":
            walkMario(mario, rectLists, "Left", clearRectList)
        if marioInfo[ONGROUND]:  # Don't decelerate mid air
            mario[VX] -= acclerate

    # Max and min acceleration
    if mario[VX] > 5:
        mario[VX] = 5
    elif mario[VX] < 0:
        mario[VX] = 0
    # Jumping logic
    gravity = 0.6
    floor=496
    marioOffset = 42
    if mario[STATE]==1:  # Change values if mario is big
        floor=452
        marioOffset = 88
    if marioInfo[ISCROUCH]:  # If mario is crouching, give him more gravity
        gravity = 0.9
    if marioInfo[ONPLATFORM] and mario[VY] <= gravity*2 and pressSpace:  # If mario is on a platform and pressing space, let him jump
        marioInfo[ISFALLING] = False
        marioInfo[ONPLATFORM] = False
    if keys[K_SPACE] and not marioInfo[ISCROUCH] and not marioInfo[ONPLATFORM]:
        if marioInfo[ONGROUND] and pressSpace:  # Checking if jumping is true
            mario[VY] -= 9.5  # Jumping power
            marioInfo[ONGROUND] = False
            marioInfo[JUMPFRAMES] = 0
            # Playing jumping sounds
            if mario[STATE] == 0:
                playSound(smallJumpSound, "effect")
            else:
                playSound(bigJumpSound, "effect")
        elif marioInfo[JUMPFRAMES] < 41 and not marioInfo[ISFALLING] and not marioInfo[ONPLATFORM]: # Simulating higher jump with less gravity
            gravity = 0.2
            marioInfo[JUMPFRAMES] += 1
    mario[Y] += mario[VY]  # Add the y movement value
    if not marioInfo[INGROUND] and mario[Y]>=floor and screen.get_at((int(mario[X]+4),int(mario[Y]+marioOffset)))==SKYBLUE and \
       screen.get_at((int(mario[X]+38),int(mario[Y]+marioOffset)))==SKYBLUE:
        # Using colour collision to fall through holes
        marioInfo[INGROUND] = True
        marioInfo[ONGROUND] = False
    elif mario[Y] >= floor and not marioInfo[INGROUND]:  # Checking floor collision
        mario[Y] = floor  # stay on the ground
        mario[VY] = 0  # stop falling
        marioInfo[ONGROUND] = True
        marioInfo[ONPLATFORM] = False
        marioInfo[ISFALLING] = False
    marioPos[VY] += gravity  # apply gravity


def walkMario(mario, rectLists, direction, clearRectList):
    """ Function to move the player, background, and all rectangles """
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    global backPos
    if direction == "Left" and mario[X] != 1:
        mario[X] -= mario[VX]  # Subtracting the VX
    elif direction == "Right":
        if mario[X] < 368: # Checking if mario is in the middle of the screen
            mario[X] += mario[VX] # Adding the VX
        else:
            mario[X] = 368
            backPos -= mario[VX] # Subtracting the VX from the background
            # Moving all rectangles
            for subList in range(len(rectLists)):
                for rect in range(len(rectLists[subList])):
                    rectLists[subList][rect][0] -= mario[VX]
            for subList in range(len(clearRectList)):
                for rect in range(len(clearRectList[subList])):
                    clearRectList[subList][rect][0] -= mario[VX]
    if mario[X] < 0:
        mario[X] = 0


def checkCollide(mario, marioInfo, marioScore, rectLists, breakingBrick, moveCoins, mushrooms):
    """ Function to check mario's collision with Rects"""
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING = 0, 1, 2, 3, 4, 5
    BRICKVY, IDLE, TYPE = 4, 5, 6
    PTS, COIN, LIVES = 0, 1, 2
    height = 42
    if mario[STATE] == 1:
        height = 84
    originalMarioRect = Rect(mario[X] + 2, mario[Y], 38 - 2, height)
    originalX, originalY, originalVY = mario[X], mario[Y], mario[VY]
    hitBrick = []
    for list in rectLists:
        for brick in list:
            brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
            marioRect = Rect(mario[X] + 2, mario[Y], 38 - 2, height) # Mario's hit box (and making it a little smaller)
            if brickRect.colliderect(marioRect):
                if int(mario[Y]) + height - int(mario[VY]) <= brickRect.y:  # Hitting top collision
                    marioInfo[ONGROUND] = True
                    marioInfo[ONPLATFORM] = True
                    marioInfo[ISFALLING] = True
                    mario[VY] = 0
                    mario[Y] = brickRect.y - height
                elif int(mario[Y] - mario[VY]) >= int(brickRect.y + brickRect.height):  # Hitting bottom collision
                    mario[Y] -= mario[VY]
                    mario[VY] = 1
                    mario[Y] = brickRect.y + brickRect.height
                    marioInfo[JUMPFRAMES] = 41
                elif int(mario[X]) >= int(brickRect[X]):  # Right side collision
                    mario[X] = brickRect.x + brickRect.width - 2  # Move mario to the right of the rect
                    mario[VX] = 0
                elif int(mario[X]) <= int(brickRect[X]):  # Left side collision
                    mario[X] = brickRect.x - 38  # Move mario to the left of the rect
                    mario[VX] = 0
            if list != brickList and brickRect.colliderect(originalMarioRect) and originalY - originalVY >= brickRect.y + brickRect.height:
                hitBrick.append([brick, list])
    for list in hitBrick:
        brick, type = list[0], list[1]
        brickRect = Rect(brick[0], brick[1], brick[2], brick[3])
        # Handling collision wigh multiple bricks
        if len(hitBrick) != 1:
            if abs(brickRect.x - originalX) > 21:
                continue
            else:
                del hitBrick[-1]
        # Manipulating bricks appropriately
        if type == interactBricks and brick[IDLE] == 0:
            indexBrick = interactBricks.index(brick)
            if brick[TYPE] > 0 or mario[STATE] == 0:
                interactBricks[indexBrick][BRICKVY] = -4
                interactBricks[indexBrick][IDLE] = 1
                playSound(bumpSound, "effect")
                if brick[TYPE] > 0:
                    brick[TYPE] -= 1
                    moveCoins.append([interactBricks[indexBrick][0] + 6, interactBricks[indexBrick][1], 30, 32, -12])
                    playSound(coinSound, "block")
                    marioScore[COIN] += 1
                    marioScore[PTS] += 200
                    if brick[TYPE] == 0:
                        questionBricks.append([brick[0], brick[1], brick[2], brick[3], brick[4], brick[5], 0])
                        del interactBricks[indexBrick]
            else:
                interactBricks[indexBrick][BRICKVY] = -9
                breakingBrick.append(interactBricks[indexBrick])
                del interactBricks[indexBrick]
                playSound(breakSound, "block")  # Play bumping sound
        elif type == questionBricks:
            playSound(bumpSound, "effect")  # Play bumping sound
            if brick[IDLE] == 0:
                indexBrick = questionBricks.index(brick)
                questionBricks[indexBrick][IDLE] = 1
                questionBricks[indexBrick][BRICKVY] = -4
                if questionBricks[indexBrick][TYPE] == 1:
                    moveCoins.append([questionBricks[indexBrick][0] + 6, questionBricks[indexBrick][1], 30, 32, -12])
                    playSound(coinSound, "block")
                    marioScore[COIN] += 1
                    marioScore[PTS] += 200
                elif questionBricks[indexBrick][TYPE] == 2:
                    mushrooms.append([questionBricks[indexBrick][0], questionBricks[indexBrick][1], 42, 42, 15, 42, 3, 0, False])
                    playSound(appearSound, "block")


def checkClearCollide(mario, marioStats, marioScore, coins, mushrooms, enemiesList, frame):
    PTS, COIN, LIVES = 0, 1, 2
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING, INVULFRAMES = 0, 1, 2, 3, 4, 5, 6, 7
    X, Y, DELAY, MOVEUP, MUSHVX, MUSHVY = 0, 1, 4, 5, 6, 7
    ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 4, 5, 6, 7
    height = 42
    if mario[STATE] == 1:
        height = 84
    marioRect = Rect(mario[X], mario[Y], 38 - 2, height)
    for coin in range(len(coins) - 1, -1, -1):
        coinRect = Rect(coins[coin][0], coins[coin][1], coins[coin][2], coins[coin][3])
        if marioRect.colliderect(coinRect):
            del coins[coin]
            playSound(coinSound, "block")
            marioScore[PTS] += 200
            marioScore[COIN] += 1
    for index in range(len(mushrooms) - 1, -1, -1):
        mushRect = Rect(mushrooms[index][0], mushrooms[index][1], mushrooms[index][2], mushrooms[index][3])
        if marioRect.colliderect(mushRect) and mushrooms[index][DELAY] == 0 and mushrooms[index][MOVEUP] == 0:
            if mario[STATE] == 0:
                mario[Y] -= 42
                mario[STATE] = 1
                marioStats[ISANIMATING] = True
                playSound(growSound, "effect")
            marioScore[PTS] += 2000
            del mushrooms[index]
    for list in range(len(enemiesList)):
        for enemy in range(len(enemiesList[list]) - 1, -1, -1):
            enmyRect = Rect(enemiesList[list][enemy][0], enemiesList[list][enemy][1], enemiesList[list][enemy][2], enemiesList[list][enemy][3])
            if enemiesList[list][enemy][ENMYIDLE] != 2 and marioStats[INVULFRAMES] == 0 and marioRect.colliderect(enmyRect):
                if int(mario[Y]) + height - int(mario[VY]) <= enmyRect.y:
                    mario[VY] = -7.5
                    marioStats[ISFALLING] = True
                    marioStats[ONGROUND] = False
                    marioScore[PTS] += 100
                    playSound(stompSound, "effect")
                    enemiesList[list][enemy][ENMYIDLE] = 2
                    enemiesList[list][enemy][ENMYINFLOOR] = 32  # Turning the infloor value into a counter for removing dead goombas
                else:
                    mario[STATE] -=1
                    marioStats[ISANIMATING] = True
                    if mario[STATE] == 0:
                        marioStats[INVULFRAMES] = 60
                        playSound(shrinkSound, "effect")


def playSound(soundFile, soundChannel, queue = False):
    """ Function to load in sounds and play them on a channel """
    channelList = [["music", 0], ["effect", 1], ["block", 2], ["extra", 3]]  # List to keep track of mixer channels
    for subList in channelList:  # For loop to identify the input
        if subList[0] == soundChannel:
            channelNumber = subList[1]
    if queue:
        mixer.Channel(channelNumber).queue(soundFile)  # Add the sound to the queue
    else:
        mixer.Channel(channelNumber).stop()  # Stopping any previous sound
        mixer.Channel(channelNumber).play(soundFile)  # Playing new sound

def globalSound(command):
    """ Function to apply commands to all mixer channels """
    for id in range(mixer.get_num_channels()):
        if command == "stop":
            mixer.Channel(id).stop()
        elif command == "pause":
            mixer.Channel(id).pause()
        elif command == "unpause":
            mixer.Channel(id).unpause()
        elif command == "toggleVol":
            if mixer.Channel(id).get_volume() == 0:
                mixer.Channel(id).set_volume(1)
            else:
                mixer.Channel(id).set_volume(0)


def spriteCounter(counter):
    """ Function to progress the universal sprite counter"""
    counter += 0.2
    if counter > 10:
        counter = 0
    return counter

def rotateRect(rectList, breakingBrick, itemsList, enemiesList):
    X, Y, ENMYVX, ENMYVY, ENMYIDLE, ENMYINFLOOR = 0, 1, 4, 5, 6, 7
    # Deleting any offscreen Rects
    for index in range(len(breakingBrick) - 1, -1, -1):
        if breakingBrick[index][1] > 600:
            del breakingBrick[index]
    for list in range(len(itemsList)):
        for item in range(len(itemsList[list]) - 1, -1, -1):
            if itemsList[list][item][0] < -300 or itemsList[list][item][1] > 650:
                del itemsList[list][item]
    for list in range(len(rectList)):
        for rect in range(len(rectList[list]) - 1, -1, -1):
            if rectList[list][rect][0] < -300:
                del rectList[list][rect]
    for list in range(len(enemiesList)):
        for rect in range(len(enemiesList[list]) - 1, -1, -1):
            if enemiesList[list][rect][0] < -300 or enemiesList[list][rect][1] > 650:
                del enemiesList[list][rect]
    # Activating and deactivating all enemies
    for list in range(len(enemiesList)):
        for enemy in range(len(enemiesList[list]) - 1, -1, -1):
            if enemiesList[list][enemy][ENMYIDLE] == 0 and enemiesList[list][enemy][X] < 800:
                enemiesList[list][enemy][ENMYIDLE] = 1
            elif enemiesList[list][enemy][ENMYIDLE] == 2 and enemiesList[list][enemy][ENMYINFLOOR] == 0:
                del enemiesList[list][enemy]


# Declaring loading functions

def loadFile(targetFile):
    """ Function to load files and make lists out of them"""
    outputList = []
    file = open(targetFile, "r")  # Loading file
    fileLines = file.readlines()  # Splitting into lines
    for line in fileLines:
        line = line.strip("\n")  # Removing any line seperators
        line = line.split(",")  # Dividing elements seperated by commas
        listLength = len(line)
        outputList.append([int(line[index]) for index in range(listLength)])  # Appending line info to list
    return outputList  # Returning final list-

# Declaring main functions

def game():
    running = True
    X, Y, VX, VY, DIR, STATE = 0, 1, 2, 3, 4, 5
    ONGROUND, JUMPFRAMES, INGROUND, ISCROUCH, ONPLATFORM, ISFALLING, ISANIMATING = 0, 1, 2, 3, 4, 5, 6
    PTS, COIN, LIVES = 0, 1, 2
    global marioStats, RECTFINDER, marioPos # REMOVE THESE AT END
    playSound(backgroundSound, "music")  # Starting the background music
    pausedBool = False
    isMuted = False
    timesUp = False
    startTime = time.get_ticks()  # Variable to keep track of time since level start
    uniSprite = 0  # Counter to control all non - Mario sprites
    # Declaring session specific lists
    breakingBrick = []
    moveCoins = []
    mushrooms = []
    # Declaring packaged lists
    rectList = [brickList, interactBricks, questionBricks]
    clearRectList = [coins, moveCoins, breakingBrick, mushrooms, goombas]
    itemsList = [mushrooms]
    enemiesList = [goombas]
    fast = False
    while running:
        mx, my = mouse.get_pos()
        initialSpace = False
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            if evnt.type == KEYDOWN:
                if evnt.key == K_SPACE:
                    initialSpace = True # Keep track of when the user first presses space
                elif evnt.key == K_m:
                    isMuted = not isMuted
                    globalSound("toggleVol") # Toggling the music volume on or off
                elif evnt.key == K_p:
                    pausedBool = not pausedBool # Toggling the paused status
                    if pausedBool:
                        globalSound("pause")
                        playSound(pauseSound, "extra")
                        pauseTime = time.get_ticks() - startTime
                    else:
                        globalSound("unpause")
                elif evnt.key == K_ESCAPE and pausedBool:
                    return "menu"
                elif evnt.key == K_o:
                    if marioPos[STATE] == 0:
                        marioPos[STATE] = 1
                    else:
                        marioPos[STATE] = 0
                elif evnt.key == K_m:
                    globalSound('toggle')
                elif evnt.key == K_0:
                    marioPos = [0, 496, 0, 0, "Right", 0]
                    marioStats = [True, 0, False, False, False, False, False, 0]
            elif evnt.type == KEYUP:
                if evnt.key == K_SPACE:
                    marioStats[ISFALLING] = True
                elif evnt.key== K_s:
                    marioStats[ISCROUCH]=False
            elif evnt.type == MOUSEBUTTONDOWN:
                RECTFINDER = [mx,my]
        if not pausedBool and not marioStats[ISANIMATING]:
            uniSprite = spriteCounter(uniSprite)
            rotateRect(rectList, breakingBrick, itemsList, enemiesList)
            checkMovement(marioPos, marioStats, marioAccelerate, rectList, initialSpace, clearRectList)
            moveSprites(marioPos, marioStats, marioSprites, marioFrame)
            moveBricks(questionBricks, interactBricks)
            spinCoins(moveCoins, uniSprite)
            moveItems(rectList, enemiesList, mushrooms, goombas)
            checkCollide(marioPos, marioStats, marioScore, rectList, breakingBrick, moveCoins, mushrooms)
            checkClearCollide(marioPos, marioStats, marioScore, coins, mushrooms, enemiesList, marioFrame)
        if marioStats[ISANIMATING]:
            moveSprites(marioPos, marioStats, marioSprites, marioFrame)
        drawScene(backgroundPics[levelNum - 1], backPos, marioPos, marioSprites, marioFrame, rectList, breakingBrick, brickSprites, coins, moveCoins, coinsPic, mushrooms, itemsPic, enemiesList, enemiesPic, uniSprite, isMuted)
        fast, timesUp = drawStats(marioPos, marioStats, marioScore[PTS], marioScore[COIN], startTime, levelNum, fast, timesUp, statCoin, uniSprite)
        if pausedBool:
            drawPause()
            startTime += (time.get_ticks() - startTime) - pauseTime
        display.flip()
        fpsCounter.tick(60)
        #print(RECTFINDER[0] - backPos, RECTFINDER[1], mx - RECTFINDER[0], my - RECTFINDER[1] )
    return "loading"


def menu():
    global levelNum, marioScore
    if mixer.Channel(0).get_volume() == 0:
        globalSound("toggleVol")
    levelNum = 0
    marioScore= [0, 0, 3]
    running = True
    globalSound("stop") # Stop any music that's playing
    selected = 0 # Variable for current selected option
    textPoints = [[360, 350], [290, 390], [333, 430], [360, 470]]
    textList = [playText, instructText, creditText, quitText]
    returnList = ["loading", "instructions", "credit", "exit"]
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            if evnt.type == KEYDOWN:
                if evnt.key == K_UP or evnt.key == K_w:
                    selected -= 1
                elif evnt.key == K_DOWN or evnt.key == K_s:
                    selected += 1
                elif evnt.key == K_RETURN:
                    return returnList[selected]
        if selected < 0:
            selected = 3
        elif selected > 3:
            selected = 0
        screen.blit(backgroundPics[0],(0,0))
        screen.blit(marioSprites[0][0], (40, 496))
        screen.blit(titleLogo,(160,80))
        for index in range(len(textList)):
            screen.blit(textList[index], (textPoints[index][0], textPoints[index][1]))
        screen.blit(titleSelect, (textPoints[selected][0] - 30, textPoints[selected][1] - 4 ))
        display.flip()
        fpsCounter.tick(60)
    return "exit"


def loading():
    PTS, COIN, LIVES = 0, 1, 2
    # Loading up and declaring all level elements
    global levelNum
    levelNum += 1
    marioPos = [40, 496, 0, 0, "Right", 0]
    marioStats = [True, 0, False, False, False, False, False, 0]
    backPos = 0
    brickList = loadFile(str("data/level_" + str(levelNum) + "/bricks.txt"))
    interactBricks = loadFile(str("data/level_" + str(levelNum) + "/interactBricks.txt"))  # 1-4: Rect, VY, State, Coins
    questionBricks = loadFile(str("data/level_" + str(levelNum) + "/questionBricks.txt"))  # 1-4: Rect, VY, State, Type
    coins = loadFile(str("data/level_" + str(levelNum) + "/coins.txt"))
    goombas = loadFile(str("data/level_" + str(levelNum) + "/goombas.txt"))
    uniSprite = 0
    currentWorld = marioFontBig.render("World 1-%s" %levelNum, False, (255,255,255))
    lives = marioFontBig.render("X  %s" %marioScore[LIVES], False, (255,255,255))
    startTime = time.get_ticks()
    while time.get_ticks() - startTime < 2500:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"
        screen.fill(BLACK)
        uniSprite = spriteCounter(uniSprite)
        drawStats(None, None, 0, 0, time.get_ticks(), levelNum, True, True, statCoin, uniSprite)
        screen.blit(currentWorld, (300, 250))
        screen.blit(lives, (390, 315))
        screen.blit(marioSprites[0][0], (315, 300))
        display.flip()
        fpsCounter.tick(60)
    return ["game", brickList, interactBricks, questionBricks, coins, goombas, marioPos, backPos, marioStats]


def instructions():
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == KEYDOWN:
                if evnt.key == K_RETURN:
                    return "menu"
            if evnt.type == QUIT:
                return "exit"
        screen.blit(backgroundPics[0],(0,0))
        screen.blit(instructHelp,(235,40))
        screen.blit(moveRightHelp,(80,130))
        screen.blit(moveLeftHelp,(80,170))
        screen.blit(jumpHelp,(80,210))
        screen.blit(crouchHelp,(80,250))
        screen.blit(pauseHelp,(80,290))
        screen.blit(musicPauseHelp,(80,330))
        screen.blit(backTextHelp,(650,450))
        screen.blit(titleSelect,(610,445))
        screen.blit(brickSprites[0][3], (375,400))
        display.flip()
        fpsCounter.tick(60)
    return "menu"


def credit():
    running = True
    while running:
        for evnt in event.get():
            if evnt.type == KEYDOWN:
                if evnt.key == K_RETURN:
                    return "menu"
            if evnt.type == QUIT:
                return "exit"
        screen.blit(backgroundPics[0], (0, 0))
        screen.blit(creditTitleHelp,(170,45))
        screen.blit(marioSprites[0][0],(400,494))
        screen.blit(marioSprites[1][0],(130,450))
        screen.blit(enemiesPic[0][0],(630,495))
        screen.blit(creditTextHelp1,(30,350))
        screen.blit(creditTextHelp2, (335, 400))
        screen.blit(creditTextHelp3, (550, 420))
        screen.blit(backTextHelp, (50, 50))
        screen.blit(titleSelect, (10, 45))
        display.flip()
        fpsCounter.tick(60)
    return "menu"

# Main loop to check for which page to fall on

while page != "exit":
    if page == "menu":
        page = menu()
    if page == "loading":
        page, brickList, interactBricks, questionBricks, coins, goombas, marioPos, backPos, marioStats = loading()
    if page == "game":
        page = game()
    if page == "instructions":
        page = instructions()     
    if page == "credit":
        page = credit()
quit()
