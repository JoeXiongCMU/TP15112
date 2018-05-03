##########################
# Click Button CLASS
# by Zhenhao Xiong
##########################

class ClickButton(object):
    def __init__(self,x1,y1,x2,y2,name,text,fontSize,fontColor):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.text = text
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.x = (self.x1 + self.x2)/2
        self.y = (self.y1 + self.y2)/2
        self.name = name
    
    def drawButton(self,data,canvas):
        bg = canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,
                                     fill = 'black',width = 1)
        txt = canvas.create_text(self.x, self.y, 
                                text=self.text, fill=self.fontColor,
                                font="Times "+str(int(self.fontSize))+" bold ")
        data.updateShapes.append(bg)
        canvas.tag_raise(bg)
        data.updateShapes.append(txt)
        canvas.tag_raise(txt)
    #return true if clicked
    def clicked(self,x,y):
        if self.x1 < x < self.x2 and self.y1 < y < self.y2:
            return True
        return False
        
        