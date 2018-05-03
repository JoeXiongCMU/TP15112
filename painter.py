##########################
# DOT CLASS
# by Kyle Chin
##########################
import math
import random
class Painter(object):

    def __init__(self, PID, x, y, paperW, paperH,color = "red"):
        self.PID = PID
        self.name = PID
        self.x = x
        self.y = y
        self.size = 20
        self.dir = 0 # the direction of painter
        self.speed = 4
        self.turnSpeed = 15
        self.color = color
        self.paperW = paperW
        self.paperH = paperH
        self.ready = False
        self.percentage = 0
        self.pixels = 0
        
        self.initPosition()
        
        self.isSpeedUp = False
        self.isSizeUp = False
        
        self.speedUpTimer = 10
        self.sizeUpTimer = 10
        
        self.isBot = False
        self.targetX = 0
        self.targetY = 0
        self.targetDir = 0
        self.targetCoolDown = 0
        
        #change bot target position
        self.changeTargetPosition()
        
    
    def changeTargetPosition(self):
        if not self.isBot:
            return
        if not self.targetCoolDown <= 0:
            self.targetCoolDown -= 1
            return
        self.targetX = random.randint(0,self.paperW)
        self.targetY = random.randint(0,self.paperH)
        
            
        dis = ((self.x - self.targetX)**2 + (self.y - self.targetY)**2)**0.5
        self.targetDir = math.asin((-self.x+self.targetX)/dis)*180/math.pi
        if self.targetY < self.y:
            if self.targetDir > 0:
                self.targetDir += 90
            else:
                self.targetDir = -180 - (self.targetDir)
        
        print("%s TARGET:(%d,%d),%d, ME:(%d,%d,%d)" %(self.color,self.targetX,self.targetY,self.targetDir,self.x,self.y,self.dir))
        self.targetCoolDown = 8
    
    def reset(self):
        self.initPosition()
        self.ready = False
        self.isSpeedUp = False
        self.isSizeUp = False
        self.speed = 4
        self.size = 20
    
    #move forward in the dir with speed. Can't go out of the border
    def moveForward(self,data):
        oriX = self.x
        oriY = self.y
        blocks = data.blocks
        
        #Check collision with the block in X
        self.x += self.speed * math.sin(self.dir*math.pi/180)
        for block in blocks:
            if block.checkInside(self.x,self.y,self.size):
                self.x = oriX
                if self.isBot:
                    self.changeTargetPosition()
                break
        #Check collision with the block in Y
        self.y += self.speed * math.cos(self.dir*math.pi/180)
        for block in blocks:
            if block.checkInside(self.x,self.y,self.size):
                self.y = oriY
                if self.isBot:
                    self.changeTargetPosition()
                break
        #Check collision with the border of paper
        if self.x > self.paperW:
            self.x = self.paperW
            self.changeTargetPosition()
        elif self.x < 0:
            self.x = 0
            self.changeTargetPosition()
        if self.y > self.paperH:
            self.y = self.paperH
            self.changeTargetPosition()
        elif self.y < 0:
            self.y = 0
            self.changeTargetPosition()
        
        
                
        
                
        
        return (self.x,self.y)
    
    
    def initPosition(self):
        disToBorder = 50
        
        if self.PID == 'A':
            self.x = disToBorder
            self.y = disToBorder
            self.dir = 45
        elif self.PID == 'B':
            self.x = self.paperW - disToBorder
            self.y = disToBorder
            self.dir = -45
        elif self.PID == 'C':
            self.x = self.paperW - disToBorder
            self.y = self.paperH - disToBorder
            self.dir = -135
        elif self.PID == 'D':
            self.x = disToBorder
            self.y = self.paperH - disToBorder
            self.dir = 135
    
    #turn an angle
    def turn(self,angle):
        self.dir += angle
    
    def changeAngle(self,angle):
        self.dir = angle
    
    #get current position
    def getPosition(self,x,y):
        return (self.x,self.y)
    
    def teleport(self, x, y):
        self.x = x
        self.y = y

    def changePID(self, PID):
        self.PID = PID
    
    def changeName(self, name):
        self.name = name
    
    def changeColor(self, color):
        self.color = color
    
    def changeReady(self,r = False):
        self.ready = r
    
    def getReadyStr(self):
        if self.ready:
            return "O"
        else:
            return "X"
    
    #draw the painter
    def drawPainter(self, canvas,data):
        r = self.size
        o = canvas.create_oval(self.x-r, self.y-r, 
                           self.x+r, self.y+r, fill=self.color, width = 1)
        nameColor = "black"
        if data.me.PID == self.PID:
            nameColor = "white"
        t = canvas.create_text(self.x, self.y, text=self.name, fill=nameColor,
                                font="Times 8 bold ")
        
        data.updateShapes.append(o)
        data.updateShapes.append(t)
    
    def updatePercentage(self,num):
        self.percentage = self.pixels / num * 100
        
        print("%s per:%.1f" % (self.color,self.percentage))
        return self.percentage
    
    def percentageStr(self):
        return str(int(self.percentage * 10)/10)
    



