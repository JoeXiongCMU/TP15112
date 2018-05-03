##########################
# Block CLASS
# by Zhenhao Xiong
##########################

import math

class Block(object):
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
    
    #return true if (x,y) is inside the block
    def checkInside(self,x,y,size):
        dis = ((self.x - x)**2 + (self.y - y)**2)**0.5
        if dis > size + self.size:
            
            return False
        else:
          #  print("COLLIDE A BLOCK")
            return True
    
    
    #draw the block
    def drawBlock(self, canvas,data):
        r = self.size
        o = canvas.create_oval(self.x-r, self.y-r, 
                           self.x+r, self.y+r, fill='black', width = 1)
        data.updateShapes.append(o)
        