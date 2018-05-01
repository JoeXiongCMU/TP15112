
class PowerUp(object):
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.size = 10
        self.name = name
        pass
    
    #return true if collide with a player
    def checkCollision(self,x,y,size):
        dis = ((self.x - x)**2 + (self.y - y)**2)**0.5
        if dis > size + self.size:
            
            return False
        else:
            print("COLLIDE A PowerUp")
            return True
        
    #draw the painter
    def drawPowerUp(self, canvas,data):
        r = self.size
        o = canvas.create_oval(self.x-r, self.y-r, 
                           self.x+r, self.y+r, fill='purple', width = 1)
        t = canvas.create_text(self.x, self.y, text='?', fill="white",
                                font="Times 8 bold ")
        data.updateShapes.append(o)
        data.updateShapes.append(t)