from player import Player
import pygame

# http://www.mariouniverse.com/wp-content/img/sprites/snes/
def Sprites(app):
    app.splashScreen = app.loadImage('mariokart12.png').resize((960, 640))
    app.marioSprite = app.loadImage('marioNew.gif')
    app.bowserSprite = app.loadImage('bowserNew.gif')
    app.yoshiSprite = app.loadImage('yoshiNew.gif')
    app.toadSprite = app.loadImage('toadNew.gif')
    app.peachSprite = app.loadImage('princessNew.gif')

    app.donkeySprite = app.loadImage('donkeyNew.gif')
    app.luigiSprite = app.loadImage('luigiNew.gif')
    app.koopaSprite = app.loadImage('koopaNew.gif')
    
    app.mushroomLoad = app.loadImage('mushroomSprite.png')
    app.bulletLoad = app.loadImage('bulletSprite.png')
    app.shellLoad = app.loadImage('redShellSprite.png')
    app.shellCurrLoad = app.loadImage('redShellMoving.gif')


    adjust = (60, 72)
    app.mode = 'splashScreenMode'
    pygame.mixer.init()
    
    
    app.bulletCurr = app.bulletLoad.crop((0, 0, 590, 520)).resize((73, 65)).rotate(270)
    app.bulletCurrTurn = app.bulletLoad.crop((0, 0, 600, 520)).resize((73, 65)).rotate(210)
    app.shellCurr = app.shellCurrLoad.resize((30, 30))

    app.bulletSprite = app.bulletLoad.crop((0, 0, 590, 520)).resize((30, 30))
    app.mushroomSprite = app.mushroomLoad.resize((30, 30))
    app.shellSprite = app.shellLoad.resize((30, 30))



    app.marioF = app.marioSprite.crop((177.5, 32, 207.5, 67.5)).resize(adjust)
    app.marioL = app.marioSprite.crop((90, 32, 120, 67.5)).resize(adjust)
    app.marioR = app.marioSprite.crop((267, 32, 297, 67.5)).resize(adjust)
    app.marioB = app.marioSprite.crop((353, 65, 383, 100.5)).resize(adjust)
    app.marioSlip = [app.marioL, app.marioB, app.marioR, app.marioF]

    
    app.bowserF = app.bowserSprite.crop((175, 35, 205, 70)).resize(adjust)
    app.bowserL = app.bowserSprite.crop((82.5, 35.5, 112.5, 70.5)).resize(adjust)
    app.bowserR = app.bowserSprite.crop((267, 35, 297, 70)).resize(adjust)
    app.bowserB = app.bowserSprite.crop((346.5, 72, 378, 106.5)).resize(adjust)
    app.bowserSlip = [app.bowserL, app.bowserB, app.bowserR, app.bowserF]

    
    app.yoshiF = app.yoshiSprite.crop((200, 35, 230, 70)).resize(adjust)
    app.yoshiL = app.yoshiSprite.crop((72.5, 35.5, 102.5, 70.5)).resize(adjust)
    app.yoshiR = app.yoshiSprite.crop((295, 34, 325, 70)).resize(adjust)
    app.yoshiB = app.yoshiSprite.crop((373, 67, 403, 103)).resize(adjust)
    app.yoshiSlip = [app.yoshiL, app.yoshiB, app.yoshiR, app.yoshiF]

   
    app.toadF = app.toadSprite.crop((171, 32, 201, 68)).resize(adjust)
    app.toadL = app.toadSprite.crop((82.5, 33.5, 111.5, 68.5)).resize(adjust)
    app.toadR = app.toadSprite.crop((262, 33, 291, 68)).resize(adjust)
    app.toadB = app.toadSprite.crop((341, 64, 371, 100)).resize(adjust)
    app.toadSlip = [app.toadL, app.toadB, app.toadR, app.toadF]

    
    app.peachF = app.peachSprite.crop((203, 34, 233, 70)).resize(adjust)
    app.peachL = app.peachSprite.crop((80.5, 35.5, 110.5, 70.5)).resize(adjust)
    app.peachR = app.peachSprite.crop((293, 35, 322, 70)).resize(adjust)
    app.peachB = app.peachSprite.crop((373.5, 67.5, 403.5, 103.5)).resize(adjust)
    app.peachSlip = [app.peachL, app.peachB, app.peachR, app.peachF]

    
    app.luigiF = app.luigiSprite.crop((178, 33, 208, 69)).resize(adjust)
    app.luigiL = app.luigiSprite.crop((89, 33.5, 119, 67)).resize(adjust)
    app.luigiR = app.luigiSprite.crop((267, 33, 297, 67)).resize(adjust)
    app.luigiB = app.luigiSprite.crop((354, 67, 384, 102)).resize(adjust)
    app.luigiSlip = [app.luigiL, app.luigiB, app.luigiR, app.luigiF]

    
    app.donkeyF = app.donkeySprite.crop((181, 35, 213, 70)).resize(adjust)
    app.donkeyL = app.donkeySprite.crop((85.5, 33.5, 115.5, 69.5)).resize(adjust)
    app.donkeyR = app.donkeySprite.crop((277.5, 33.5, 307.5, 69.5)).resize(adjust)
    app.donkeyB = app.donkeySprite.crop((360, 68, 392, 103)).resize(adjust)
    app.donkeySlip = [app.donkeyL, app.donkeyB, app.donkeyR, app.donkeyF]

    
    app.koopaF = app.koopaSprite.crop((173, 32, 203, 66)).resize(adjust)
    app.koopaL = app.koopaSprite.crop((80.5, 32, 110.5, 65)).resize(adjust)
    app.koopaR = app.koopaSprite.crop((266, 32, 296, 65)).resize(adjust)
    app.koopaB = app.koopaSprite.crop((342, 64, 372, 98)).resize(adjust)
    app.koopaSlip = [app.koopaL, app.koopaB, app.koopaR, app.koopaF]

def playerData(app):
    app.player = None
    app.mario = Player('Mario', 0, [], 0, (app.width // 2, 500), 
    app.marioR, app.marioL, app.marioF, app.marioB, 30, 33, 1, 'na', 0, app.marioSlip, 5)
    
    app.bowser = Player('Bowser', 0, [], 0, (325, 450), 
    app.bowserR, app.bowserL, app.bowserF, app.bowserB, 32, 40, 2.1, 'na', 0, app.bowserSlip, 5)
    
    app.yoshi = Player('Yoshi', 0, [], 0, (250, 500), 
    app.yoshiR, app.yoshiL, app.yoshiF, app.yoshiB, 10, 37, 0.8, 'na', 0, app.yoshiSlip, 5)
    
    app.toad = Player('Toad', 0, [], 0, (560, 400), 
    app.toadR, app.toadL, app.toadF, app.toadB, 10, 38, 0.7, 'na', 0, app.toadSlip, 5)
    
    app.peach = Player('Peach', 0, [], 0, (710, 500), 
    app.peachR, app.peachL, app.peachF, app.peachB, 30, 41, 0.8, 'na', 0, app.peachSlip, 5)
    
    app.luigi = Player('Luigi', 0, [], 0, (635, 450), 
    app.luigiR, app.luigiL, app.luigiF, app.luigiB, 30, 39, 1.1, 'na', 0, app.luigiSlip, 5)
    
    app.donkey = Player('Donkey Kong', 0, [], 0, (app.width // 2, 450), 
    app.donkeyR, app.donkeyL, app.donkeyF, app.donkeyB, 22, 37, 1.9, 'na', 0, app.donkeySlip, 5)
    
    app.koopa = Player('Koopa', 0, [], 0, (400, 400), 
    app.koopaR, app.koopaL, app.koopaF, app.koopaB, 20, 37, 1.7, 'na', 0, app.koopaSlip, 5)