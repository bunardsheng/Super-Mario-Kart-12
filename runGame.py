from cmu_112_graphics import *
import math
import random
import pygame
from charSprites import Sprites, playerData
from player import Player
import time

#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#playingSoundsWithPygame
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())
    def start(self, loops):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)
    def stop(self):
        pygame.mixer.music.stop()

class Item(object):
    def __init__(self, name, start):
        self.name = name
        self.start = start
        self.hitbox = [self.start[0] - 30, self.start[1] - 30, self.start[0] + 30, self.start[1] + 30]
    def move(self, dx, dy):
        x, y = self.start
        newX = x + dx 
        newY = y + dy
        self.start = (newX, newY)

        x0, y0, x1, y1 = self.hitbox
        self.hitbox = (x0 + dx, y0 + dy, x1 + dx, y1 + dy)

        
        
# ######################## splash screen ########################## # 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html #

def grid(app):
    app.rows = 2
    app.cols = 4
    app.margin = 50
    app.selection = (-1, -1)

def pointInGrid(app, x, y):
    return (x > app.margin and x < app.width - app.margin) and (y > 0 and y < app.height)

def getCell(app, x, y):
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)

def getCellBounds(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth 
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def characterSelect_mouseMoved(app, event):
    app.playerSelected = not app.playerSelected
    (row, col) = getCell(app, event.x, event.y)
    if (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        app.playerSelected = True
        
def charPortraits(app):
    app.playerSelected = False
 
    app.mp = app.loadImage('marioPortrait.jpeg').resize((212, 265))
    app.pp = app.loadImage('peachPortrait.jpeg').resize((212, 265))
    app.tp = app.loadImage('toad.jpeg').resize((212, 265))
    app.dp = app.loadImage('donkeyPortrait.jpeg').resize((212, 265))
    app.lp = app.loadImage('luigiPortrait.jpeg').resize((212, 265))
    app.kp = app.loadImage('koopaPortrait.jpeg').resize((212, 265))
    app.bp = app.loadImage('bowserPortrait.jpeg').resize((212, 265))
    app.yp = app.loadImage('yoshiPortrait.jpeg').resize((212, 265))

    
    app.portraitList = [ [app.mp, app.lp, app.tp, app.pp], [app.bp, app.dp, app.kp, app.yp] ]
    
def characterSelect_redrawAll(app, canvas):

    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'royalblue3')
    choices = [['Mario', 'Luigi', 'Toad', 'Peach'], ['Bowser', 'Donkey', 'Koopa', 'Yoshi']]
    shift = 100
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            fill = "yellow" if (app.selection == (row, col)) else "black"
            canvas.create_image((x0+x1)//2, (y0+y1)//2, image=ImageTk.PhotoImage(app.portraitList[row][col]))
            canvas.create_rectangle(x0, y0, x1, y1, width = 5, outline=fill)
            canvas.create_text((x0+x1)//2 - 35, (y0+y1)//2 - shift, 
            text = f'"{choices[row][col].upper()}"', font = 'Arial 20 bold', fill = 'white')
            

    
    
def selectChar(app, event):
    
    row, col = app.selection[0], app.selection[1]
    app.player = app.charSelect[row][col]
    app.player.speed = 10
    app.player.maxSpeed = 35
    app.player.start = (app.width // 2, app.height // 1.75)

    app.player.hitbox = ( [app.player.start[0] - 30, app.player.start[1] - 36, 
    app.player.start[0] + 30, app.player.start[1] + 36] )
    app.mode = 'gameMode'
    app.enemies.remove(app.charSelect[row][col])
    
    app.places = makePlaces(app)
    
    app.time0 = time.time()

def makePlaces(app):
    places = [[app.player.total, app.player]]
    
    for enemy in app.enemies:
        places.append([(enemy.total), enemy])
    return places

def characterSelect_mousePressed(app, event):
    if app.selection == (0, 0):
        selectChar(app, event)
    if app.selection == (0, 1):
        selectChar(app, event)
    if app.selection == (0, 2):
        selectChar(app, event)
    if app.selection == (0, 3):
        selectChar(app, event)
    
    if app.selection == (1, 0):
        selectChar(app, event)
    if app.selection == (1, 1):
        selectChar(app, event)
    if app.selection == (1, 2):
        selectChar(app, event)
    if app.selection == (1, 3):
        selectChar(app, event)

####################################################################

#splash screen image: https://www.cultofmac.com/722261/mario-kart-tour-gets-nostalgic-in-its-latest-update/
def splashScreenMode_redrawAll(app, canvas):
    canvas.create_image((app.width//2, app.height//2), image=ImageTk.PhotoImage(app.splashScreen))
   
    if int(time.time() - app.timeSplash) % 2 == 0:
        
        canvas.create_text(app.width // 1.25, app.height // 7, text = 'Press Any Key To Start', font='Arial 20 bold', fill = 'white')

def drawEndScreen(app, canvas):
    shift = 0
    cx = app.width // 2 
    sy = app.height // 6
    x0 = cx - 150
    x1 = cx + 150
    y0 = sy - 20
    y1 = sy + 20
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'lightblue')
    
    canvas.create_text(app.width // 2, app.height // 12, text = 'SCOREBOARD', 
    fill = 'white', font = 'Arial 24 bold')
    
    
    space = 20
    for person in app.lapTimes:
        for lap in app.lapTimes[person]:
            canvas.create_text(x0, app.height // 8 + space * lap, text = 'Lap ' +f'{lap}' + " : " 
            f'{app.lapTimes[person][lap]}' + 's' , font = 'Arial 14 bold', fill = 'white', anchor = 'sw')
            

    for i in range(8):
        shift += 50
        canvas.create_rectangle(x0, y0 + (shift), x1, y1 + (shift), fill = 'deepskyblue', 
        outline = 'white', width = 3)

        if i == 0:
            end = 'st -- '
        elif i == 1:
            end = 'nd -- '
        elif i == 2:
            end = 'rd -- '
        else:
            end = 'th -- '

        if app.places[i][1] == app.player:
            fill = 'gold'
        else:
            fill = 'white'

        if i % 2 == 0:
            offset = 200
        else:
            offset = -200
        canvas.create_image((cx + offset, sy+shift), 
        image=ImageTk.PhotoImage(app.places[i][1].back.resize((35, 42))))
        canvas.create_text(cx, sy + shift, text=f'{(1+i)}'+end + 
        f'{app.places[i][1].name}', fill = fill, font='Arial 14 bold')
    

    if int(time.time() - app.timeSplash) % 2 == 0:
        canvas.create_text(app.width // 2, app.height * 0.925, 
        text = 'Press Space to Continue', font = 'Arial 18 bold', fill='white')
        


                    
def endMode_redrawAll(app, canvas):
    drawEndScreen(app, canvas)

            
    # enter user input and store their time
    # create a leaderboard based on their places and have their sprite

def endMode_keyPressed(app, event):
    if event.key == 'Space':
        restartApp(app)
        app.mode = 'splashScreenMode'

    



def splashScreenMode_keyPressed(app, event):
    app.mode = 'characterSelect'

def drawFinishLine(app, canvas):
    blocks = makeFinishLine(app)
    color = 0
    for block in blocks:
        color += 1
        x0, y0, x1, y1 = block
        showY0, showY1 = (y0 + app.player.location, y1 + app.player.location)
        
        if color % 2 == 0:
            fill = 'black'
        else:
            fill = 'white'
        
        canvas.create_rectangle(x0, showY0, x1, showY1, fill = fill )

def makeFinishLine(app):

    blocks = []
    w = 25
    h = 25
    x0 = -50
    x1 = x0 + w
    
    y0 = 170
    y1 = y0 + h
    
    for row in range(3):
        for col in range(52):
            blocks.append([x0 + (col*w) + (row*w), y0 + (row*h), x1 + ((row*w)) + (col*w), y1+(row*h)])
    return blocks

def makeItemGrid(app, canvas):
    w = 50
    x0 = 50
    x1 = x0 + w
    y0 = app.height // 10
    y1 = y0 + w
    for i in range(3):
        canvas.create_rectangle(x0 + i * w, y0, x1 + i * w, y1, fill = 'gray90',width = 5)

def drawItems(app, canvas):
    w = 50
    x0 = 50
    x1 = x0 + w
    y0 = app.height // 10
    y1 = y0 + w

    centerX = (x0 + x1 ) / 2
    centerY = (y0 + y1) / 2

    for i in range(len(app.player.items)):
        if len(app.player.items) >= 1:
            canvas.create_image((centerX + i*w, centerY), image = ImageTk.PhotoImage(app.player.items[i]))
            


def getItemCoords(app):
    w = 50
    h = 25
    l = 30

    itemLocationsX = list(range(250, 600))
    itemLocationsY = list(range(300, 10000))
    random.shuffle(itemLocationsX)
    random.shuffle(itemLocationsY)

    itemBox = []
    for i in range(6):
        pt1 = itemLocationsX[i], itemLocationsY[i]
        pt2 = pt1[0] + (w / 2), pt1[1] - (h / 2)
        pt3 = pt1[0]+w, pt1[1]
        pt4 = pt2[0], pt2[1] + h
        itemBox.append([pt1, pt2, pt3, pt4])
    
    return itemBox
        


def createItemBox(app, canvas):
    w = 50
    h = 25
    l = 30

    if int(time.time() - app.time0) % 2 == 0:
        fill1 = 'goldenrod2'
        fill2 = 'dodgerblue3'
        fill3 = 'deeppink2'
        fill4 = 'white'
    else:
        fill1 = 'dodgerblue4'
        fill2 = 'deeppink3'
        fill3 = 'yellow'
        fill4 = 'black'
    
    px, py = app.player.start

    for coords in app.itemBox:
        showPoints = []
        for point in coords:
            showPoints.append((point[0], (py + (app.player.location - point[1]))))

        pt1, pt2, pt3, pt4 = showPoints

        #item
        #canvas.create_rectangle(pt1[0], pt4[1]-l, pt3[0], pt2[1], outline = fill4)
    
        canvas.create_polygon(pt1, pt1[0], pt1[1] - l, pt4[0], pt4[1] - l, pt4, 
        fill = fill2, width = 3, outline = fill4)
    
        canvas.create_polygon(pt4, pt4[0], pt4[1] - l, pt3[0], pt3[1] -l, pt3, 
        fill = fill3, width = 3, outline = fill4)

        canvas.create_polygon(pt1, pt2, pt3, pt4, fill = fill1, width = 3, 
        outline = fill4)


def shuffleItems(index):
    w = 50
    h = 25
    l = 30

    itemLocationsX = list(range(250, 600))
    itemLocationsY = list(range(300, 10000))
    random.shuffle(itemLocationsX)
    random.shuffle(itemLocationsY)

    pt1 = itemLocationsX[index], itemLocationsY[index]
    pt2 = pt1[0] + (w / 2), pt1[1] - (h / 2)
    pt3 = pt1[0]+w, pt1[1]
    pt4 = pt2[0], pt2[1] + h
    

    return [pt1, pt2, pt3, pt4]
   


def itemCollide(app):
    l = 30
    px, py = app.player.start
    for i in range(len(app.itemBox)):
        showPoints = []
        for pt in app.itemBox[i]:
            showPoints.append((pt[0], (py + (app.player.location - pt[1]))))
            

        pt1, pt2, pt3, pt4 = showPoints
        x0, y0, x1, y1 = pt1[0], pt4[1] - l, pt3[0], pt2[1]
        itemHitbox = x0, y0, x1, y1
        if checkCollision(app, itemHitbox, app.player.hitbox):
            itemList = ( [app.mushroomSprite, app.mushroomSprite, app.mushroomSprite, 
            app.shellSprite, app.bulletSprite, app.shellSprite] )
            random.shuffle(itemList)
            app.itemBox.pop(i)
            app.itemBox.append(shuffleItems(i))
            if len(app.player.items) < 3:
                app.player.items.append(itemList[0])
    
            
def drawSpeed(app, canvas):
    canvas.create_text(app.width * 0.1, app.height * 0.85, text=f'Speed: {int(1.5*app.player.speed)}mph', 
    font='Arial 20 bold', fill = 'white')


def gameMode_redrawAll(app, canvas):
  
    canvas.create_rectangle(0,0,app.width, app.height, fill = 'gray33')
    createRoad(app, canvas)
    
    if app.curve:
      
        canvas.create_arc(450, app.height + 1000, app.width + 1000, 200, start = 80, style=CHORD, extent = 140, fill = 'tan2')
        canvas.create_arc(-1060, 400, 315, -500, start = -100, style=CHORD, extent = 120, fill = 'tan2')
        curveBlocks(app, canvas)
        
    else:
        
        drawRoadBlock(app, canvas)

    
    
    drawFinishLine(app, canvas)
    
    createEnemies(app, canvas)
    
    createPlayer(app, canvas)
    
    drawBananas(app, canvas)
    
    buildingTurnR(app, canvas)
    
    buildingTurnL(app, canvas)
    
    drawText(app, canvas)
    
    createTimer(app, canvas)
    
    makeItemGrid(app, canvas)

    createItemBox(app, canvas)

    drawItems(app, canvas)

    drawShell(app, canvas)

    drawPlace(app, canvas)
   
    makeBirdEye(app, canvas)
    
    makeBirdEyePlayer(app, canvas)
    
   

    if app.gameStart:
        canvas.create_text(app.width * 0.15, app.height * 0.9, text=f'Speed: {int(1.5*app.player.speed)} mph', 
        font='Arial 20 bold', fill = 'white')
    
    
#creates the right side of map
def buildingTurnR(app, canvas):
    for i in range(len(app.cubesR)):
        start, width, height = app.cubesR[i]
        if (i % 2) == 0: 
            fill = 'green'
        
        else:
            fill = 'red'
        
        if app.curve:
            createBuildingCurve(app, canvas, start, width, height, fill, 300, 1000)
        else:
            createBuildingR(app, canvas, start, width, height, fill, app.slopeR)

def buildingTurnL(app, canvas):
    
    for i in range(len(app.cubesL)):
        start, width, height = app.cubesL[i]
        if (i%2) == 0:
            fill = 'royalBlue'
        else:
            fill = 'goldenrod'
        
        if app.curve:
            createBuildingCurve(app, canvas, start, width, height, fill, -300, 800)
        else:
            createBuildingL(app, canvas, start, width, height, fill, app.slopeL)

def appStarted(app):
    restartApp(app)

def restartApp(app):
    app.counter = 0
    app.useMushroom = False
    app.useBullet = False
    app.useShell = False
    app.shell = Item('shell', (app.width // 2, app.height // 1.75))
    app.mushroomTime = 0
    app.bulletTime = 0
    app.shellTimer = 0
    app.gameStart = False
    app.countdown = 0
    app.shellSprite = 0
    app.bulletSprite = 0
    app.paused = False
    app.gameOver = False
    app.totalDistance = 0
    app.timeSplash = time.time()
    app.elapsed = 0
    

    app.lapTimes = {}
    
    
    app.winTime = 0

    Sprites(app)
    playerData(app)
    app.spriteCounter = 0
    app.spriteCounterAI = 0

    app.prevLap = 0
    app.currLap = 0

    #https://www.youtube.com/watch?v=u5VxJkYEJIs&ab_channel=lovegamescapsule
    app.background1 = Sound("background1.mp3")
    app.background2 = Sound("backgroundTrim.mp3")

    
    
    app.bananas = makeBanana(app)
    app.bananaSprite = app.loadImage('bananaSprite.png').resize((40, 40))

    app.itemBox = getItemCoords(app)
    charPortraits(app)
    grid(app)
    
    #app.timerDelay = 100
    app.slopeDx = 275
    app.curve = False

    app.bananaTimer = 5
    app.bananaTimerAI = 5
    
    app.rightRoad = (app.width * 0.7, app.height // 8, app.width - app.slopeDx, app.height // 1.15 )
    app.slopeR = ( (app.rightRoad[3] - app.rightRoad[1]) / (app.rightRoad[2] - app.rightRoad[0]) )
    
    app.leftRoad = (app.width * 0.3, app.height // 8, 0 + app.slopeDx, app.height // 1.15)
    app.slopeL = ( (app.leftRoad[3] - app.leftRoad[1]) / (app.leftRoad[2] - app.leftRoad[0]) ) 

    app.newChallenger = None
    
    app.enemies = [app.bowser, app.yoshi, app.toad, app.peach, app.luigi, app.donkey, app.koopa, app.mario]
    app.charSelect = [ 
                       [app.mario, app.luigi, app.toad, app.peach], 
                       [app.bowser, app.donkey, app.koopa, app.yoshi] 
                       
                       ]


    
    
    app.cubesR = makeCubesR(app)
    app.cubesL = makeCubesL(app)
    app.sx0 = app.width // 2.025
    app.sy0 = 575
    app.sx1 = app.width // 1.975
    app.sy1 = 600

    

    app.keys = set()
    app.blocks = makeRoadBlocks(app)
    app.distanceTraveled = 0
    app.scroll = 0
    
    app.increaseSpeed = False
    app.collide = False

# ------------------- bananas -------------------- #
def shuffleBananas(app, xList, yList, banW, banY, index):
    random.shuffle(xList)
    random.shuffle(yList)
    randW = xList[index]
    randY = yList[index]
    return [randW - banW, randY - banY, randW + banW, randY + banY]

def makeBanana(app):
    bananas = []
    intList = list(range(150, 800))
    randLocation = list(range(300, 10000))
    banW = 20
    banY = 20
    
    for i in range(15):
        coords = shuffleBananas(app, intList, randLocation, banW, banY, i)
        bananas.append(coords)

    return bananas

def checkbananas(app):
    intList = list(range(150, 800))
    randLocation = list(range(300, 5000))
    banW = 20
    banY = 20

    for i in range(len(app.bananas)):
        if banana[i][3] < app.player.location:
            app.bananas.pop(i)
            coords = shuffleBanas(app, intList, randLocation, banW, banY, i)
            app.bananas.append(coords)

def hitBanana(app):
    intList = list(range(150, 800))
    randLocation = list(range(300, 5000))
    banW = 20
    banY = 20
    
    for i in range(len(app.bananas)):
        (pX, pY) = app.player.start
        (x0, y0, x1, y1) = app.bananas[i]

        showY0 = pY + (app.player.location - y0)
        showY1 = pY + (app.player.location - y1)

        px0, py0, px1, py1 = app.player.hitbox

       
            #actual banana coordinates
            
            # the p needs to scale
        
        if checkCollision(app, (x0, showY0, x1, showY1), app.player.hitbox):
            
            
            
            app.spriteCounter = (1 + app.spriteCounter) % len(app.player.sprites)
            if not app.useBullet and not app.useMushroom:
                if app.player.slipTimer >= 1:
                    
                    app.player.curr = app.player.sprites[app.spriteCounter]
                    app.player.speed = 0
                    app.player.slipTimer -= 1
                    app.player.state = 'slipped'
                
                elif app.player.slipTimer < 1:
                    app.player.state = 'na'
                    app.bananas.pop(i)
                    coords = shuffleBananas(app, intList, randLocation, banW, banY, i)
                    app.bananas.append(coords)
                    app.player.slipTimer = 5
                        
                   
                
        
        for enemy in app.enemies:
            if checkCollision(app, (x0, showY0, x1, showY1), enemy.hitbox):
                app.spriteCounterAI = (1 + app.spriteCounterAI) % len(enemy.sprites)
                
                if enemy.slipTimer >= 1:
                    enemy.curr = enemy.sprites[app.spriteCounterAI]
                    enemy.speed = 0
                    enemy.slipTimer -= 1
                    enemy.state = 'slipped'
                elif enemy.slipTimer < 1:
                    enemy.state = 'na'
                    app.bananas.pop(i)
                    coords = shuffleBananas(app, intList, randLocation, banW, banY, i)
                    app.bananas.append(coords)
                    enemy.slipTimer = 5
        
def drawBananas(app, canvas):
    
    for i in range(len(app.bananas)):
        (pX, pY) = app.player.start
        
        x0, y0, x1, y1 = app.bananas[i]
        
        showY0 = pY + (app.player.location - y0)
        showY1 = pY + (app.player.location - y1)

        if abs(app.player.location - y0) <= 300 and abs(app.player.location-y1) <= 300:
            #display hit box, for testing purposes
            #canvas.create_rectangle(x0, showY0, x1, showY1, outline = 'yellow')
            canvas.create_image((x0 + x1) // 2, (showY0 + showY1) //2, 
            image=ImageTk.PhotoImage(app.bananaSprite))

def makeBirdEyePlayer(app, canvas):
    cx = app.width * 0.85
    cy = app.height * 0.85
    r = 55
    segment = (10000 / 6)
    value = (app.player.location / 10000) * 2 * math.pi
    coordX = r * math.cos(value)
    coordY = -r * math.sin(value)
    
    if app.player.location >= 0 and app.player.location <= 2500:
        playerSprite = app.player.turnL

    
    
    elif app.player.location >= 2500 and app.player.location <= segment*4:
        playerSprite = app.player.back
    elif app.player.location >= segment * 4 and app.player.location <= segment*6:
        playerSprite = app.player.turnR
    else:
        playerSprite = app.player.turnL

    canvas.create_image((cx+coordX, cy+coordY), image=ImageTk.PhotoImage(playerSprite.resize((20, 24))))
        
def makeBirdEye(app, canvas):
    cx = app.width * 0.85
    cy = app.height * 0.85
    r = 55
    segment = (10000 / 6)
    
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, width = 5, outline='bisque')

    for enemy in app.enemies:
        value = (enemy.location / 10000) * 2 * math.pi
        coordX = r * math.cos(value)
        coordY = -r * math.sin(value)
        
        if enemy.location >= 0 and enemy.location <= 2500:
            enemySprite = enemy.turnL

       
        
        elif enemy.location >= 2500 and enemy.location <= segment*4:
            enemySprite = enemy.back
        elif enemy.location >= segment * 4 and enemy.location <= segment*6:
            enemySprite = enemy.turnR
        else:
            enemySprite = enemy.turnL
        

        
        
        canvas.create_image((cx+coordX, cy+coordY), image=ImageTk.PhotoImage(enemySprite.resize((20, 24))))
    

    

# ---------------------makeFunctions----------------------- #

def makeCubesR(app):
    cubes = []
    wids = list(range(0, 150))
    lens = list(range(40, 90))
    random.shuffle(wids)
    random.shuffle(lens)
    
    start = 500
    for i in range(15): 
        cubes.append([start, wids[i], lens[i]])
        start += wids[i] + random.randint(0, 20)
    return cubes

def makeCubesL(app):
    cubes = []
    wids = list(range(0, 150))
    lens = list(range(0, 90))
    random.shuffle(wids)
    random.shuffle(lens)

    start = 400
    for i in range(15): 
        cubes.append([start, wids[i], lens[i]])
        start += -(wids[i] + random.randint(0, 20))
    return cubes

def makeRoadBlocks(app):
    shift = 50
    x0, y0, x1, y1 = app.sx0, app.sy0, app.sx1, app.sy1
    
    blocks = []
    for i in range(10):
        shift += 100
        blocks.append([app.sx0, (y0-shift), app.sx1, (y1-shift)])
    return blocks



# ---------------------timerFunctions----------------------- #
def checkCubes(app):
    wids = list(range(0, 150))
    lens = list(range(30, 90))
    random.shuffle(wids)
    random.shuffle(lens)
    
    buffer = 50
    
    for i in range(len(app.cubesR)):
        if app.cubesR[-1][0] >= app.width + buffer:
            app.cubesR.pop(-1)
            start = app.cubesR[0][0]
            app.cubesR.insert(0, [start - wids[i], wids[i], lens[i]])

    for i in range(len(app.cubesL)):
        if app.cubesL[-1][0] <= -buffer:
            app.cubesL.pop(-1)
            start = app.cubesL[0][0]
            app.cubesL.insert(0, [start + wids[i], wids[i], lens[i]])

def checkBounds(app):
    
    shift = 100
    
    for i in range(len(app.blocks)):
        if app.height - app.blocks[0][3] <= 0:
            app.blocks.pop(0)
            
            #app.blocks, first index is the very bottom
            app.blocks.append([app.sx0, app.blocks[-1][1] - shift, app.sx1, app.blocks[-1][3]-shift] )
        #gets the top of top rectangle
        
        if app.blocks[-1][1] < 0.5:
            app.blocks.pop(-1)
            app.blocks.insert(0, [app.sx0, app.blocks[0][1] + shift, app.sx1, app.blocks[0][3] + shift])   

def addBlock(app, event):
    if event.key == 'Up':
        for i in range(len(app.blocks)):
            
            app.blocks[i][1] += app.player.speed
            app.blocks[i][3] += app.player.speed
        for i in range(len(app.cubesR)):
            app.cubesR[i][0] += app.player.speed
        for i in range(len(app.cubesL)):
            app.cubesL[i][0] -= app.player.speed

    if event.key == 'Down':
        for i in range(len(app.blocks)):
            app.blocks[i][1] += app.player.speed
            app.blocks[i][3] += app.player.speed
        for i in range(len(app.cubesR)):
            app.cubesR[i][0] += app.player.speed
        for i in range(len(app.cubesL)):
            app.cubesL[i][0] -= app.player.speed

#gives a scrolling decceleration or accelerating affect 
def addBlockTimer(app):
    for i in range(len(app.blocks)):
        app.blocks[i][1] += app.player.speed
        app.blocks[i][3] += app.player.speed
    
    for i in range(len(app.cubesR)):
        app.cubesR[i][0] += app.player.speed
    
    for i in range(len(app.cubesL)):
        app.cubesL[i][0] -= app.player.speed
    
#fine tuned to balance enemy acceleration
def enemyFired(app):
    for char in app.enemies:
        if char.state != 'hit':
            if char.speed < char.maxSpeed:
                char.speed += 30 / (char.maxSpeed) * 1.81 ** 3
                char.location += char.speed
                char.total += char.speed

#used for the red shell
def findNearestPlayer(app):
    locations = {}
    for enemy in app.enemies:
        if app.player.location <= enemy.location:
            locations[enemy] = enemy.location
    
    if len(locations) > 0:
        return min(locations, key=locations.get)

def drawShell(app, canvas):
    if app.useShell:
        canvas.create_image((app.shell.start), image=ImageTk.PhotoImage(app.shellCurr))
        #draws the hitbox, for testing purposes
        #canvas.create_rectangle(app.shell.start[0] - 20, app.shell.start[1] - 20, 
        #app.shell.start[0] + 20, app.shell.start[1] + 20, outline = 'red3')

def throwShell(app):
    
    nearestPlayer = findNearestPlayer(app)
    if nearestPlayer != None:
        app.shell.hitbox = [app.shell.start[0] - 20, app.shell.start[1] - 20, 
        app.shell.start[0] + 20, app.shell.start[1] + 20]
        
        if app.useShell and not checkCollision(app, app.shell.hitbox, nearestPlayer.hitbox):
            if app.shell.start[0] < nearestPlayer.start[0]:
                app.shell.move(15, 0)
            
            if app.shell.start[1] < nearestPlayer.start[1]:
                app.shell.move(0, +15)
            
            if app.shell.start[0] > nearestPlayer.start[0]:
                app.shell.move(-15, 0)
            
            if app.shell.start[1] > nearestPlayer.start[1]:
                app.shell.move(0, -15)

        elif app.useShell and checkCollision(app, app.shell.hitbox, nearestPlayer.hitbox):
            
            app.shell.start = app.player.start
            nearestPlayer.speed = 0
            nearestPlayer.s()
            app.useShell = False
                
           
            


#displays ennemies relative to player location
def showEnemy(app):
    for enemy in app.enemies:
        enemy.start = enemy.start[0], app.player.start[1] + (app.player.location-enemy.location)
        enemy.hitbox = [enemy.start[0] - 30, enemy.start[1] - 36, enemy.start[0] + 30, enemy.start[1] + 36]

#keyPressed functions      
def pressed(app):
    if 'Up' in app.keys:
        #accelerates up to 20
        if app.player.speed <= app.player.maxSpeed:
            app.player.speed += 60 / (app.player.maxSpeed * 1.21**3)
    
    if 'Up' not in app.keys:
        #if released, while it's speeding up, decellerate
        if app.player.speed > 0:  
            app.player.speed -= 1.01 ** 2
            #don't go backwards
            if app.player.speed < 0:
                app.player.speed = 0
    
    if 'Down' in app.keys:
        if app.player.speed >= -app.player.maxSpeed:
            app.player.speed -= 0.8 * 1.01**3
        
    
    if 'Down' not in app.keys:
        if app.player.speed < 0:  
            app.player.speed += 1.01 ** 2
            if app.player.speed > 0:
                app.player.speed = 0

def beginCurveR(app):
    app.rightRoad = (app.width * 0.7, app.height // 8, app.width - app.slopeDx, app.height // 1.15 )
    app.slopeR = ( (app.rightRoad[3] - app.rightRoad[1]) / (app.rightRoad[2] - app.rightRoad[0]) ) 

    app.leftRoad = (app.width * 0.3, app.height // 8, 0 + app.slopeDx, app.height // 1.15)
    app.slopeL = ( (app.leftRoad[3] - app.leftRoad[1]) / (app.leftRoad[2] - app.leftRoad[0]) ) 

#defines when a curve is drawn
def curveDistances():
    gap = 1000

    start1 = 200
    dis1 = 4000
    end1 = start1+dis1

    start2 = end1 + gap
    dis2 = 1000
    end2 = start2 + dis2

    start3 = start2 + gap
    dis3 = 1000
    end3 = start3+dis3

    return start1, start2, start3, end1, end2, end3

def whenToCurve(app):
    start1, start2, start3, end1, end2, end3 = curveDistances()

    if app.player.location >= start1 and app.player.location <= end1:
        
        if app.slopeDx < 270:
            app.slopeDx += app.player.speed / 3
        if app.slopeDx >= 270:
            app.curve = True

    elif app.player.location >= start2 and app.player.location <= end2:
       
        if app.slopeDx < 270:
            app.slopeDx += app.player.speed / 3
        if app.slopeDx >= 270:
            app.curve = True

    elif app.player.location >= start3 and app.player.location <= end3:
        
        if app.slopeDx < 270:
            app.slopeDx += app.player.speed / 3
        if app.slopeDx >= 270:
            app.curve = True
    else:
        app.curve = False
        
        app.slopeDx = 0
        if app.slopeDx > 0:
            app.slopeDx -= app.player.speed

def turnSprite(app):
    if app.curve:
        for enemy in app.enemies:
            enemy.d()
        
        if app.player.state == 'na':
            app.player.d()
    
def curveBounds(app):
    curveStart = list((range(300, 600)))
    random.shuffle(curveStart)
    randomStart = list(range(200, 800))
    random.shuffle(randomStart)
    randomRange = list(range(25, 50))
    random.shuffle(randomRange)

    if app.curve:
        for i in range(len(app.enemies)):
            #app.enemies.speed = app.enemies.maxSpeed - app.
            if app.enemies[i].start[0] < curveStart[i]:
                app.enemies[i].move(app.enemies[i].maxSpeed, 0)
           
            if app.enemies[i].start[0] > curveStart[i]:
                app.enemies[i].move(-app.enemies[i].maxSpeed, 0)
    else:
        for i in range(len(app.enemies)):
            if app.enemies[i].state != 'hit':
                app.enemies[i].w()
            
            if app.enemies[i].start[0] < randomStart[i] + randomRange[i]:
                app.enemies[i].move(5, 0) 
            if app.enemies[i].start[0] > randomStart[i] - randomRange[i]:
                app.enemies[i].move(-5, 0)

def showTimer(app):
    if int(time.time() - app.time0) >= 6:
        app.startTimer += 1
        if app.startTimer <= 5:
            return True
    return False


def createTimer(app, canvas):
    if not app.gameStart:
        if int(time.time() - app.time0) < 4:
            canvas.create_text(app.width//2 - 8, app.height//6, text='WELCOME TO MARIO CIRCUIT', 
            font = 'Arial 32 bold', fill = 'blue')
            canvas.create_text(app.width//2 - 4, app.height//6, text='WELCOME TO MARIO CIRCUIT', 
            font = 'Arial 32 bold', fill = 'red4')
            canvas.create_text(app.width//2, app.height//6, text='WELCOME TO MARIO CIRCUIT', 
            font = 'Arial 32 bold', fill = 'white')
            canvas.create_text(app.width * 0.5, app.height * 0.22, text='Use Arrow Keys to Move, Press "F" To Use Item'
            ,font = 'Arial 12 bold', fill = 'white' )
            canvas.create_text(app.width * 0.5, app.height * 0.85, text= 
            ' Please Refrain from Holding the Arrow Keys Within First 10s', font='Arial 16 bold', fill = 'red3')
            canvas.create_text(app.width * 0.15, app.height * 0.9, text=f'Speed: 0 mph', 
            font='Arial 20 bold', fill = 'white')
        
        elif int(time.time()-app.time0) >= 6:
            canvas.create_text(app.width//2, app.height//2 - 20, 
            text=f'{11-int(time.time()-app.time0)}', font = 'Arial 36 bold', fill = 'white')

#checks the placing
def checkPlace(app):
    app.places = sorted(app.places, reverse=True)

def drawPlace(app, canvas):
    
    for row in range(len(app.places)):
        for col in app.places[row]:
            if col == app.player:
                if row == 0:
                    end = 'st'
                    fill = 'gold'

                elif row == 1:
                    end = 'nd'
                    fill = 'ghost white'
                elif row == 2:
                    end = 'rd'
                    fill = 'darkorange1'
                else:
                    end = 'th'
                    fill = 'snow'
                canvas.create_text(app.width * 0.85, app.height * 0.85, text = f'{1+row}' + end, font = 'Arial 20 bold', fill=fill)

def modLocation(app):
    app.player.location = app.player.location % 10000
    for enemy in app.enemies:
        enemy.location = enemy.location % 10000

#makes sure enemy speed does not go overboard
def enemySpeedCheck(app):
    for enemy in app.enemies:
        if enemy.speed > enemy.maxSpeed:
            enemy.speed -= 3 * (1.02**3)

def gameMode_timerFired(app): 
    if not app.paused:
        if time.time() - app.time0 < 15:
            beginCurveR(app)
            if app.slopeDx > 0:
                app.slopeDx -= 3.3
            if app.slopeDx <= 0:
                app.gameStart = True
                app.background1.start(1)
        if time.time() - app.time0 < 15:
            app.player.speed = 2
        if app.gameStart:
            modLocation(app)
            turnSprite(app)
            beginCurveR(app)
            whenToCurve(app)
            curveBounds(app)
            showEnemy(app)
            hitBanana(app)
            checkAllCollision(app)
            pressed(app)
            checkCubes(app)
            checkBounds(app)
            addBlockTimer(app)
            enemyFired(app)
            checkCollideBoundsL(app)
            checkCollideBoundsR(app, app.player.hitbox)
            itemCollide(app)
            itemTimer(app)
            enemySpeedCheck(app)
            findNearestPlayer(app)
            throwShell(app)
            app.places = makePlaces(app)
            checkPlace(app)
            collisionWithPlayer(app)
            checkWin(app)

            app.player.location += int(app.player.speed)
            app.player.total += app.player.speed
         
            

        


def checkWin(app):
    app.elapsed = int(time.time()-app.time0) 
    #checks each second and if the lap is different between seconds: record lap time
    if app.elapsed % 2 == 1:
        app.currLap = int(app.player.total // 10000)
    elif app.elapsed % 2 == 0:
        app.prevLap = int(app.player.total // 10000)
    
    if app.prevLap != app.currLap:
        if app.lapTimes == {}:
            app.lapTimes[app.player.name] = {max(app.prevLap, app.currLap) : app.elapsed}
            
        else:
            app.lapTimes[app.player.name][max(app.prevLap, app.currLap)] = app.elapsed
    
    #if the user does 2 laps, game over
    if app.prevLap >= 2 or app.currLap >= 2:
        app.gameStart = False
        app.mode = 'endMode'
        app.background1.stop()
        
#can change the sprite direction with wasd
def enemyTest(app, event):
    if event.key == 'w':
        for character in app.enemies:
            character.w()
    elif event.key == 'a':
        for character in app.enemies:
            character.a()
    elif event.key == 'd':
        for character in app.enemies:
            character.d()
    elif event.key == 's':
        for character in app.enemies:
            character.s()

#determines acceleration/decceleration based on a set
def gameMode_keyReleased(app, event):
    if app.gameStart:
        if event.key == 'Up':
            if len(app.keys) >= 1:
                app.keys.remove('Up')
        elif event.key == 'Left':
            if len(app.keys) >= 1:
                app.keys.remove('Left')
        elif event.key == 'Down':
            if len(app.keys) >= 1:
                app.keys.remove('Down')
        
        elif event.key == 'Right':
            if len(app.keys) >= 1:
                app.keys.remove('Right')

def upKey(app, event):
    if event.key == 'Up':
        app.keys.add('Up')
        
        if not app.curve and not app.useBullet and app.player.state == 'na':
            app.player.w()
       
        for i in range(len(app.enemies)):
            if checkCollision(app, app.enemies[i].hitbox, app.player.hitbox):
                
                vcf, vpf = getCollisionFactor(app, app.enemies[i], app.player)
                app.enemies[i].location += int(vpf // 3.5)
                
                if app.enemies[i].speed < vcf:
                    app.enemies[i].speed += 0.2
                
                if app.player.speed > vpf:
                    app.player.speed -= 1

def downKey(app, event):
    if event.key == 'Down':
        app.keys.add('Down')
        if not app.curve and not app.useBullet:
            app.player.s()
       
        #app.slopeDx -= 1
        
        for i in range(len(app.enemies)):
            if checkCollision(app, app.enemies[i].hitbox, app.player.hitbox):
                vcf, vpf = getCollisionFactor(app, app.enemies[i], app.player)
                
                while app.enemies[i].speed < vcf:
                    app.enemies[i].speed += 0.2
                app.enemies[i].location -= int(vpf)
                while app.player.speed > vpf:
                    app.player.speed -= 1


def leftKey(app, event):
    if event.key == 'Left':
        app.keys.add('Left')
        if not app.curve and not app.useBullet:
            app.player.a()
        
        if app.player.speed != 0:
            if not checkCollideBoundsL(app):
                app.player.move(-app.player.speed // 3, 0)
            
        else:
            if not checkCollideBoundsL(app):
                app.player.move(-10, 0)
        
        
        for i in range(len(app.enemies)):
            if checkCollision(app, app.enemies[i].hitbox, app.player.hitbox):
                
                vcf, vpf = getCollisionFactor(app, app.enemies[i], app.player)
                app.enemies[i].move(-(vcf // 3.5), 0)
                app.player.move((+vpf//3.5), 0)
    
                if app.enemies[i].speed < vcf:
                    app.enemies[i].speed += 0.2
                
                if app.player.speed > vpf:
                    app.player.speed -= 1
                
                
                

def rightKey(app, event):
    if event.key == 'Right':
        app.keys.add('Right')
        if not app.curve and not app.useBullet:
            app.player.d()

        if app.player.speed != 0:
            if not checkCollideBoundsR(app, app.player.hitbox):
                app.player.move(app.player.speed, 0)
                
            #if collided, player speed is slowed
        
        else:
            if not checkCollideBoundsR(app, app.player.hitbox):
                app.player.move(10, 0)
        
        if app.player.start[0] > 839:
            app.player.move(-10, 0)

        for i in range(len(app.enemies)):
            if checkCollision(app, app.enemies[i].hitbox, app.player.hitbox):
                vcf, vpf = getCollisionFactor(app, app.enemies[i], app.player)
                app.enemies[i].move(+(vcf // 6), 0)
                app.player.move(( -vpf // 6), 0)
    
                while app.enemies[i].speed < vcf:
                    app.enemies[i].speed += 0.2
                
                while app.player.speed > vpf:
                    app.player.speed -= 1

def gameMode_keyPressed(app, event):
    if event.key == 'p':
        app.paused = not app.paused


    if app.gameStart and not app.paused:
        addBlock(app, event)
        enemyTest(app, event)
        upKey(app, event)
        downKey(app, event)
        leftKey(app, event)
        rightKey(app, event)
        useItem(app, event)
        
    
def itemTimer(app):
    if app.useMushroom:
        app.player.state = 'na'
        app.mushroomTime += 1
        app.player.speed = app.player.maxSpeed + 2
        
        
        if app.mushroomTime > 15:
            app.useMushroom = False
            app.player.speed = app.player.maxSpeed // 3.75
            app.mushroomTime = 0
    
    elif app.useBullet:
        
        app.bulletTime += 1
        if app.curve:
            app.player.curr = app.bulletCurrTurn
        else:
            app.player.curr = app.bulletCurr
        app.player.speed = app.player.maxSpeed + 5
        
        if app.bulletTime > 40:
            app.useBullet = False
            app.player.speed = app.player.maxSpeed // 2.5
            
            if 'Up' not in app.keys:
                app.player.speed -= 2.01 ** 2
            
            app.player.w()
            app.bulletTime = 0
        
        
    
    
        #if not at the player's location
        #keep increasing speed of shell
        #if collide with then it works.

def useItem(app, event):
    if len(app.player.items) >= 1:
        if event.key == 'f':
    
            if app.player.items[0] == app.mushroomSprite:
                app.useMushroom = True
                app.useBullet = False
                app.useShell = False
                app.player.items.pop(0)

            elif app.player.items[0] == app.bulletSprite:
                app.useBullet = True
                app.useMushroom = False
                app.useShell = False
                app.player.items.pop(0)

            elif app.player.items[0] == app.shellSprite:
                app.useShell = True
                app.useBullet = False
                app.useMushroom = False
                app.player.items.pop(0)

#collisions between each enemy and player
def collisionWithPlayer(app):
    for i in range(len(app.enemies)):
        if checkCollision(app, app.enemies[i].hitbox, app.player.hitbox):
            vcf, vpf = getCollisionFactor(app, app.enemies[i], app.player)
            #xDis, checks whether collision was from right or left
            xDis = abs(app.player.start[0] - app.enemies[i].start[0]) // 35
            
            if app.enemies[i].start[0] > app.player.start[0]:
            
                app.enemies[i].move(-vcf * xDis, 0)
                app.player.move((+vpf // 3.5) * xDis , 0)
            
            else:
                app.enemies[i].move(-vcf * xDis, 0)
                app.player.move(+(vpf // 3.5) * xDis , 0)
            
            if app.enemies[i].speed < vcf:
                app.enemies[i].speed += 0.2
        
            if app.player.speed > vpf:
                app.player.speed -= 1
            

#collisions between all enemies
def checkAllCollision(app):
    if time.time() - app.time0 >= 5: 
        for i in range(len(app.enemies)):
            for j in range(len(app.enemies)-i):
                if checkCollision(app, app.enemies[i].hitbox, app.enemies[i+j].hitbox):
                    vcf, vpf = getCollisionFactor(app, app.enemies[i], app.enemies[i+j])
                    xDis = abs(app.player.start[0] - app.enemies[i].start[0]) // 35

                    if app.enemies[i].start[0] < app.enemies[i+j].start[0]:
                        app.enemies[i].move((-vcf // 3.5) * xDis, 0)
                        app.enemies[i+j].move((+vpf // 3.5) * xDis, 0)

                    elif app.enemies[i].start[0] > app.enemies[i+j].start[0]:
                        app.enemies[i].move((+vcf // 3.5) * xDis, 0)
                        app.enemies[i+j].move((-vpf // 3.5) * xDis, 0)
                   
                    if app.enemies[i].speed < vcf:
                        app.enemies[i].speed += 0.2
                
                    if app.enemies[i+j].speed > vpf:
                        app.enemies[i+j].speed -= 1
            
            
                    
# https://www.youtube.com/watch?v=O8VyU4j6dT0&t=67s&ab_channel=JohnMcCaffrey 
# altered from Processing                   
def checkCollision(app, characterPts, otherPts):
    x0, y0, x1, y1 = characterPts
    ax0, ay0, ax1, ay1 = otherPts

    cx = (x0 + (x1-x0) / 2)
    cy = (y0 + (y1-y0) / 2)



    acx = ( ax0 + (ax1-ax0) / 2 )
    acy = ( ay0 + (ay1-ay0) / 2 )


    distanceApartX = abs(cx - acx)
    distanceApartY = abs(cy - acy)

    halfWidth = ((x1 - x0) / 2) + ((ax1 - ax0) / 2)
    halfHeight = ((y1 - y0) / 2) + ((ay1 - ay0) / 2)

    if distanceApartX - halfWidth < 5 and distanceApartY - halfHeight < 5:
        return True

    #if colliding from left, set sprite to right
    return False

# https://courses.lumenlearning.com/boundless-physics/chapter/collisions/
def getCollisionFactor(app, char, other):
    m1, v1o = char.weight, char.speed
    m2, v2o = other.weight, other.speed
    
    v2f = ( ( (2 * m1) / (m2+m1) ) * v1o ) + ( (m2-m1) / (m2+m1) ) * v2o
    v1f = ( (m1-m2) / (m2+m1 ) * v1o ) + ( (2 * m2) / (m2+m1) ) * v2o

    return v1f, v2f
    

#slope function
def coords(slope, ep, x):
    x1, y1 = ep
    x0 = x
    y0 = slope*(x-x1) + y1

    return x0, y0

#square root function
def curve(x):
    y = -(32 * math.sqrt(abs(x)))
    
    return x, y 

def findXCurve(y):
    x = ( (y ** 2) / (32 * 32) )
    return x, y

#creates curves based on the point of each rectangle from the MakeCubes function
def createBuildingCurve(app, canvas, start, width, height, fill, shiftX, shiftY):
    start, y0Start = curve(start)
    ey1 = y0Start + height
    h = height
    w = width
    
    xshift = shiftX
    yshift = shiftY

    (x0, y0) = findXCurve(y0Start)
    (x1, y1) = findXCurve(ey1)
    #1, 3, 2, 4

    pt1 = (x0 + xshift), (y0 + yshift)
    pt2 = (x1 + xshift), (y1 + yshift)
    pt3 = (x1 + w + xshift), (y1 + yshift)
    pt4 = (x0 +w+xshift), (y0 + yshift)

        

    canvas.create_polygon(pt1, pt2, pt3, pt4, fill = fill, width = 1.1, outline = 'black')
    canvas.create_rectangle(pt3, pt2[0], pt2[1] + w // 2, fill = fill+'4', width = 1.1, outline = 'black')
    canvas.create_polygon(pt3, pt3[0], pt3[1] + w //2, pt4[0], pt4[1] + w//2, pt4, fill = fill+'3', outline = 'black')
    


def createBuildingR(app, canvas, start, width, height, fill, slope):
    gap = 20 
    ex0, ey0, ex1, ey1 = app.rightRoad 
    
    ep = (ex1 + gap, ey1)
   
    x0 = start 
    x1 = x0 + width 
    h = height

    if time.time() - app.time0 < 15:
        shiftFactor = app.slopeDx // 1.5
    else:
        shiftFactor = 0

    (x3, y3) = coords(slope, ep, x0)
    (x4, y4) = coords(slope, ep, x1)


    #right top, left, top, left bottom, right bottom
    pt1 = x4 - shiftFactor, y4 - h 
    pt2 = x3 - shiftFactor , y3 - h 
    pt3 = x3 - shiftFactor, y3
    pt4 = x4 - shiftFactor, y4 

    canvas.create_polygon(pt1, pt2, pt3, pt4, fill = fill, width = 1.1, outline = 'black')
    canvas.create_rectangle(pt1, app.width, y4, fill = fill+'4', width = 1.1, outline = 'black')
    canvas.create_polygon(pt1, pt2, app.width, y3-h, app.width, y4-h, fill = fill+'3', outline = 'black')
    

def createBuildingL(app, canvas, start, width, height, fill, slope):
    gap = 20
    x1, y1, x0, y0 = app.leftRoad
    ep = (x1 - gap, y1)

    x0 = start 
    x1 = x0 + width
    h = height
    
    if time.time() - app.time0 < 15:
        shiftFactor = app.slopeDx // 1.5
    else:
        shiftFactor = 0

    (x0, y0) = coords(slope, ep, x0)
    (x4, y4) = coords(slope, ep, x1)

    # (x0, y0) = curve(y0)
    # (x4, y4) = curve(y1)

    
    pt1 = x0 + shiftFactor, y0
    pt2 = x0 + shiftFactor, y0 - h
    pt3 = x4 + shiftFactor, y4 - h
    pt4 = x4 + shiftFactor, y4

    canvas.create_rectangle(pt2, 0, pt1[1], fill = fill+'4', outline = 'black')
    canvas.create_polygon(pt3, 0, pt3[1], 0, pt2[1], pt2, fill=fill+'2', outline = 'black')
    canvas.create_polygon(pt1, pt2, pt3, pt4, fill = fill+'3', width = 1.1, outline = 'black')

#makes sure user does not go off road
def checkCollideBoundsL(app):
    endPoints = app.leftRoad[0], app.leftRoad[1]
    slope = app.slopeL
    x0, y0, x1, y1 = app.player.hitbox

    xLine, yLine = coords(slope, endPoints, x0)

    if xLine > x0 or (abs(x0 - xLine) <= 5 and y0-yLine <= 5):
        return True
    
    return False


def checkCollideBoundsR(app, points):
    endPoints = app.rightRoad[0], app.rightRoad[1]
    slope = app.slopeR
    x0, y0, x1, y1 = points
    
    xLine, yLine = coords(slope, endPoints, x1)
 
    if xLine < x1 or (abs(x1 - xLine) <= 5 and y0-yLine <= 5):
        return True
    
    return False

def curveBlocks(app, canvas):
    for i in range(len(app.blocks)):
        fill = 'yellow'
        x0, y0, x1, y1 = app.blocks[i]
        start = y0
        h = (y1 - y0)   
        w = (x1 - x0) 
        y1 = (start + w)
        createBuildingCurve(app, canvas, start, w, h, fill, -50, 1000)

def createRoad(app, canvas):
    x1, y1, x0, y0 = app.leftRoad
    x2, y2, x3, y3 = app.rightRoad

    if not app.curve:
        canvas.create_line(x1, y1, x0, y0, width = 7, fill='white')
    #100, 240
        canvas.create_line(x2, y2, x3, y3, width = 7, fill = 'white')

        

def drawText(app, canvas):
    canvas.create_text(app.width * 13 // 14, app.height// 14, text = f'LAP: {1+int(app.player.total // 10000)} / 3', anchor = 'se',font = 'Arial 20 bold'
    , fill = 'white')

def drawRoadBlock(app, canvas):
    for coords in app.blocks:
        x0, y0, x1, y1 = coords
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'yellow')

def createEnemies(app, canvas):
    for character in app.enemies:
        x0, y0, x1, y1 = character.hitbox
        if app.curve:
            if character.start[1] > 100:
                #hitbox
                #canvas.create_rectangle(x0, y0, x1, y1, outline = 'green')
                canvas.create_image(character.start, image=ImageTk.PhotoImage(character.curr))
        else:
            #hitbox
            #canvas.create_rectangle(x0, y0, x1, y1, outline = 'green')
            canvas.create_image(character.start, image=ImageTk.PhotoImage(character.curr))

        
def createPlayer(app, canvas):
    x0, y0, x1, y1 = app.player.hitbox
    if app.useMushroom:
        fill = 'yellow'
        canvas.create_text(x0 - 15, y0, anchor='sw', text='speed', fill='lightblue')
    else:
        fill = 'red'
    #hitbox
    #canvas.create_rectangle(x0, y0, x1, y1, outline = fill)
    #draw the sprite
    canvas.create_image(app.player.start, image=ImageTk.PhotoImage(app.player.curr))

runApp(width=960, height=640)




    