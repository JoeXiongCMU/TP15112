##########################
# DOT CLASS
# by Kyle Chin
##########################
import math

class Painter(object):

    def __init__(self, PID, x, y, paperW, paperH,color = "red"):
        self.PID = PID
        self.name = PID
        self.x = x
        self.y = y
        self.size = 20
        self.dir = 0 # the direction of painter
        self.speed = 3
        self.turnSpeed = 15
        self.color = color
        self.paperW = paperW
        self.paperH = paperH
        self.ready = False
        self.percentage = 0
        self.pixels = 0
        
    #move forward in the dir with speed. Can't go out of the border
    def moveForward(self):
        self.x += self.speed * math.sin(self.dir*math.pi/180)
        self.y += self.speed * math.cos(self.dir*math.pi/180)
        if self.x > self.paperW:
            self.x = self.paperW
        elif self.x < 0:
            self.x = 0
        if self.y > self.paperH:
            self.y = self.paperH
        elif self.y < 0:
            self.y = 0
        return (self.x,self.y)
    
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
        t = canvas.create_text(self.x, self.y, text=self.name, fill="black",
                                font="Times 8 bold ")
        data.updateShapes.append(o)
        data.updateShapes.append(t)
    
    def updatePercentage(self,num):
        self.percentage = self.pixels / num
        print("%s per:%.1f%"%(self.color,self.percentage))



