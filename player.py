class Player(object): 
    def __init__(self, name, location, items, lap, start, turnR, turnL, 
    front, back, speed, maxSpeed, weight, state, total, sprites, slipTimer):
        self.start = start
        self.name = name
        self.location = location
        self.items = items
        self.lap = lap
        self.items = []
        self.turnR = turnR
        self.turnL = turnL
        self.curr = front
        self.front = front
        self.back = back
        self.hitbox = [start[0] - 30, start[1] - 36, start[0] + 30, start[1] + 36]
        self.speed = speed
        self.maxSpeed = maxSpeed
        self.weight = weight
        self.state = state
        self.total = total
        self.sprites = sprites
        self.slipTimer = slipTimer
    
    def getItem(self, item):
        self.items.append(item)
    
    def a(self):
        self.curr = self.turnL
    def d(self):
        self.curr = self.turnR
    def w(self):
        self.curr = self.front
    
    def s(self):
        self.curr = self.back
    
    def move(self, dx, dy):
        currX, currY = self.start
        self.start = (currX + dx, currY + dy)
        x0, y0, x1, y1 = self.hitbox
        self.hitbox = [x0 + dx, y0 + dy, x1 + dx, y1 + dy]
    def addTotal(self, delta):
        self.total += delta

        