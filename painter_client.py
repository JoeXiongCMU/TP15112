#############################
# Painter Battle Client
# by Zhenhao Xiong
#############################

import socket
import threading
import time
import string
from queue import Queue

HOST = "" # put your IP address here if playing on multiple computers
PORT = 50002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

#Handle Server Msg
def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

# events-example0.py from 15-112 website
# Barebones timer, mouse, and keyboard events


names = ["A", "B", "C", "D"]
colors = ["red", "blue","green","orange"]


from tkinter import *
from painter import *
from click_button import *
from block import *
from power_up import *
import random
####################################
# menu
####################################

# draw menu window(including title and buttons)
def drawMenuWindow(canvas,data):
  if data.gameState == "menu" or data.gameState == "select":
    menu = canvas.create_text(data.width / 2, data.height / 5,
                              text = "Painter Battle",fill="black",
                              font="Times 38 bold" )
    data.updateShapes.append(menu)
    
    for button in data.menuButtons:
      button.drawButton(data,canvas)

# draw instruction window
def drawInstruction(canvas,data):
  if data.gameState == "instruction" :
    data.instructionImage = PhotoImage(file=data.imageName)
    title = canvas.create_text(data.width / 2, 50,
                              text = "How to play?",fill="black",
                              font="Times 38 bold" )
    data.updateShapes.append(title)
    
    img = canvas.create_image(data.width/2,data.height/2,
                        anchor = CENTER,image=data.instructionImage)
    data.updateShapes.append(img)
    for button in data.instructionButtons:
      button.drawButton(data,canvas)

# draw select window(A grid of players)    
def drawSelectWindow(canvas,data):
  if data.gameState == "select":
    selectMenu = canvas.create_rectangle(data.width/5, data.height/3,
                                        data.width/5*4 ,data.height/3 *2.5,
                                        fill = 'black',width = 2
                                        )
    data.updateShapes.append(selectMenu)
    offsetX = data.width /4
    offsetY = data.height/3* 1.2
    
    gridX = 50
    gridY = 30
   
    items = ["","Name","Color","Ready?"]
    drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
    offsetY += gridY
    
    #draw my info
    player = data.me
    items = ["Player:",player.name,player.color,player.getReadyStr()]
    drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
    offsetY += gridY
    #draw other player info
    for PID in data.otherStrangers:
      player = data.otherStrangers[PID]
      items = ["Player:",player.name,player.color,player.getReadyStr()]
      drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
      offsetY += gridY
    #draw "ready" button
    for button in data.selectButtons:
      button.drawButton(data,canvas)
    
#draw a single row of "Items"
def drawSelectRow(canvas,data,items,offsetX,offsetY,gridX):
    for item in items:
      t = canvas.create_text(offsetX,offsetY,text = str(item),fill="yellow",
                        font="Times 12 bold")
      offsetX += gridX
      data.updateShapes.append(t)
    
#draw the window of change name    
def drawChangeName(canvas,data):
  if data.gameState == "name":
    nameMenu = canvas.create_rectangle(data.width/5, data.height/3,
                                        data.width/5*4 ,data.height/3 *2.5,
                                        fill = 'black',width = 2
                                        )
    data.updateShapes.append(nameMenu)
    offsetX = data.width /5
    offsetY = data.height/3
    
    text1 = canvas.create_text(data.width/2,offsetY + 50,anchor = CENTER,
                              text="Enter your Name", fill="yellow",
                              font="Times 20 bold"
                              )
    data.updateShapes.append(text1)
    
    text_name = canvas.create_text(data.width/2,offsetY + 100, anchor = CENTER,
                              text=data.newName, fill="yellow",
                              font="Times 20 bold"
                              )
    data.updateShapes.append(text_name)
    
    text_line = canvas.create_text(data.width/2,offsetY + 120, anchor = S,
                              text="________________________", fill="yellow",
                              font="Times 20 bold"
                              )
    data.updateShapes.append(text_line)
  
    for button in data.nameButtons:
      button.drawButton(data,canvas)

#draw the gameplay UI
def drawGameUI(canvas,data):
    text_time = canvas.create_text(data.width - 30,30,anchor = NE,
                              text="Time:"+str(int(data.time)), fill="black",
                              font="Times 20 bold"
                              )
    data.updateShapes.append(text_time)

#draw the result window
def drawResult(canvas,data):
  if data.gameState == "end":
    winner = canvas.create_text(data.width / 2, data.height / 5,
                              text = "Winner: "+ str(data.winner.name),fill="black",
                              font="Times 38 bold" )
    data.updateShapes.append(winner)
    
    
    endMenu = canvas.create_rectangle(data.width/5, data.height/3,
                                        data.width/5*4 ,data.height/3 *2.5,
                                        fill = 'black',width = 2
                                        )
    data.updateShapes.append(endMenu)
    
    offsetX = data.width /4
    offsetY = data.height/3* 1.2
    
    gridX = 120
    gridY = 30
   
    items = ["Name","Color","Percentage"]
    drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
    offsetY += gridY
     
    #draw my result
    player = data.me
    items = [player.name,player.color,player.percentageStr()]
    drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
    offsetY += gridY
    #draw other palyer's result
    for PID in data.otherStrangers:
      player = data.otherStrangers[PID]
      items = [player.name,player.color,player.percentageStr()]
      drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
      offsetY += gridY
    
    for button in data.endButtons:
      button.drawButton(data,canvas)
    
    
#get all the pixel coodinate in a circle(cx,cy,size)
#can't go outside the paper.
def getPixelCircleList(data,cx,cy,size):
    lst = []
    
    rows = len(data.paper)
    cols = len(data.paper[0])
    
    for i in range(int(cx-size),int(cx+size+1)):
      for j in range(int(cy-size),int(cy+size+1)):
        if 0 <= i < rows and 0 <= j < cols:
          if distance(i,j,cx,cy) <= size:
            lst.append((i,j))
    return lst


#draw a player's trail on paper
def drawOnPaper(data,player):
    for (x,y) in getPixelCircleList(data,player.x,player.y,player.size):
      data.paper[x][y] = player.PID

#draw all the players' trail on paper
def updateResultOnPaper(data):
    drawOnPaper(data,data.me)
    for PID in data.otherStrangers:
      drawOnPaper(data,data.otherStrangers[PID])

def findWinner(data):
  players = []
  players.append(data.me)
  for PID in data.otherStrangers:
    players.append(data.otherStrangers[PID])
  
  max = 0
  winner = data.me
  for player in players:
    p = player.percentage
    if p > max:
      max = p
      winner = player
  
  data.winner = winner
  return max

#Update the pixel precentage result in every player
#low efficent, cost a lot of time
def updateResult(data):
    data.me.pixels = 0
    for PID in data.otherStrangers:
      data.otherStrangers[PID].pixels = 0
    
    for i in range(data.rows):
      for j in range(data.cols):
        if data.paper[i][j] == data.me.PID:
          data.me.pixels += 1
        else:
          for PID in data.otherStrangers:
            if data.paper[i][j] == PID:
              data.otherStrangers[PID].pixels += 1
    
    if data.me.PID == 'A':
      p = data.me.updatePercentage(data.rows * data.cols)
      #send msg to other player
      msg = "updateResult %s %f\n" %(data.me.PID,p)
      
      if (msg != ""):
        print ("sending: ", msg,)
        data.server.send(msg.encode())
      
      for PID in data.otherStrangers:
        p = data.otherStrangers[PID].updatePercentage(data.rows * data.cols)
        #send msg to other player
        msg = "updateResult %s %f\n" %(PID,p)
        
        if (msg != ""):
          print ("sending: ", msg,)
          data.server.send(msg.encode())
    
    findWinner(data)
      

#init the game setting
def initGameSetting(data):
    data.time = 30
    data.me.percentage = 0
    data.resultUpdateTime = 5000
    
    for PID in data.otherStrangers:
      data.otherStrangers[PID].percentage = 0
    
    data.rows = data.height
    data.cols = data.width
    #use to record every pixel's color.
    data.paper = [ ([""] * data.cols) for row in range(data.rows) ]
    
#init the buttons for select window
def initSelectButton(data):
    data.selectButtons = []
    
    button_ready = ClickButton(300-50,450-20,
                                   300+50, 450+20,
                                    "ready",
                                    "Ready!",30,'yellow')
    data.selectButtons.append(button_ready)
    button_bot = ClickButton(300-50,400-20,
                                   300+50, 400+20,
                                    "bot",
                                    "Add Bot",30,'yellow')
    data.selectButtons.append(button_bot)

#init the buttons for select window
def initInstructionButton(data):
    data.instructionButtons = []
    
    button_back = ClickButton(300-50,550-20,
                                   300+50, 550+20,
                                    "back",
                                    "Back!",30,'yellow')
    data.instructionButtons.append(button_back)


#init the buttons for end window
def initEndButton(data):
    data.endButtons = []
    
    button_back = ClickButton(300-50,450-20,
                                   300+50, 450+20,
                                    "end",
                                    "Play Again!",40,'yellow')
    data.endButtons.append(button_back)



#init the buttons for change name window   
def initName(data):
    data.newName = ""
    data.nameButtons = []
    
    button_done_name = ClickButton(300-50,450-20,
                                   300+50, 450+20,
                                    "done_name",
                                    "Done!",40,'yellow')
    data.nameButtons.append(button_done_name)
    
#init the buttons for main menu
def initMenuButton(data):
    offsetX = data.width/3
    offsetY = data.height/3
    
    buttonX = 200
    buttonY = 50
    fontSize = 30
    buttonInter = 50
    
    button_play_online = ClickButton(offsetX,offsetY,
                                    offsetX + buttonX, offsetY + buttonY,
                                    "online",
                                    "Start Game!",fontSize,'orange')
    data.menuButtons.append(button_play_online)
    
    button_play_instruction = ClickButton(offsetX,
                                      offsetY + buttonY + buttonInter ,
                                      offsetX + buttonX , 
                                      offsetY + buttonY * 2 + buttonInter,
                                      "instruction",
                                      "How to Play?",fontSize,'orange')
    data.menuButtons.append(button_play_instruction)
    

#generate blocks
def initBlock(data):
    if data.me.PID == 'A':
      data.blocks = []
      for i in range(3):
        b = 120
        x = random.randint(b,data.width - b)
        y = random.randint(b,data.height - b)
        while(checkBlockOverlay(data.blocks,x,y)):
          x = random.randint(b,data.width - b)
          y = random.randint(b,data.height - b)
          
        size = random.randint(30,60)
        data.blocks.append(Block(x,y,size))
        #send msg to other player
        msg = "addBlock %d %d %d\n" %(x,y,size)
        print("newBlock %d %d" %(x,y))
        if (msg != ""):
          print ("sending: ", msg,)
          data.server.send(msg.encode())

#check the blocks overlay, return true if overlay
def checkBlockOverlay(blocks,x,y):
    for block in blocks:
      if distance(block.x,block.y,x,y) < 120:
        print("OVERLAY!!\n")
        return True
    return False
    
 
def initPowerups(data):
   data.powerups = []
   data.powerupTimer = 0


def moveAllBot(data):
  if data.me.PID == 'A':
    for PID in data.otherStrangers:
      player = data.otherStrangers[PID]
      botAI(player)

#the core code of bot AI
def botAI(player):
  #only control bot move angle
  if not player.isBot:
    return
  dis = distance(player.x,player.y,player.targetX,player.targetY)
  if dis > 80:
    
    currentAngle = player.dir
   # print("%s:%f,%f"%(player.color,player.targetDir,currentAngle))
    
    delta = currentAngle - player.targetDir
    if delta < -5 or delta > 5:
      if currentAngle > player.targetDir:
        player.turn(-player.turnSpeed/3)
      else:
        player.turn(player.turnSpeed/3)
      print("%s TURNING!\n"%player.color)
  else:
    player.changeTargetPosition()
    print("%s CHANGING\n" % player.color)
    
#deal with power up spawning
def updatePowerUp(data):
   # print(data.powerups)
    
    #spawn of powerup
    if data.me.PID == 'A':
      data.powerupTimer += data.timerDelay/1000
      if data.powerupTimer > 12:
        data.powerupTimer = 0
        x = random.randint(10,data.width)
        y = random.randint(10,data.height)
        type = random.randint(0,1)
        if type == 0:
          name = "speedup"
        else:
          name = "sizeup"
        data.powerups.append(PowerUp(x,y,name))
      
        #send msg to other player
        msg = "addPowerUp %d %d %s\n" %(x,y,name)
        
        if (msg != ""):
          print ("sending: ", msg,)
          data.server.send(msg.encode())
    
    #update power up time
    for PID in data.otherStrangers:
      player = data.otherStrangers[PID]
      updatePowerUpTime(data,player)
    
    updatePowerUpTime(data,data.me)
 
 #update a player's power up remaining time   
def updatePowerUpTime(data,player):
    #update size up time
    if player.isSizeUp:
      player.sizeUpTimer -= data.timerDelay/1000
      if(player.sizeUpTimer < 0):
        player.isSizeUp = False
        player.size = 20
    #update speed up time
    if player.isSpeedUp:
      player.speedUpTimer -= data.timerDelay/1000
      if(player.speedUpTimer < 0):
        player.isSpeedUp = False
        player.speed = 4
    
    #Check collision to new powerup
    for powerup in data.powerups:
        if powerup.checkCollision(player.x,player.y,player.size):
            if powerup.name == "speedup":
                player.isSpeedUp = True
                player.speed = 8
                player.speedUpTimer = 10
            elif powerup.name == "sizeup":
                player.isSizeUp = True
                player.size = 30
                player.sizeUpTimer = 10
            data.powerups.remove(powerup)
            break
    

#return True if everyone is ready
def checkAllReady(data):
  if not data.me.ready:
    return False
  for PID in data.otherStrangers:
    player = data.otherStrangers[PID]
    if not player.ready:
      return False
  return True

#add a new bot
def addBot(data):
    playerNum = len(data.otherStrangers) + 1
    if playerNum >= 4:
        return
    
    #Set up player name
    botName = names[playerNum]
    botColor = colors[playerNum]
    
    x = data.width/2
    y = data.height/2
    data.otherStrangers[botName] = Painter(botName,x, y,
                                          data.width,data.height,
                                          color = botColor)
    data.otherStrangers[botName].isBot = True
    data.otherStrangers[botName].ready = True # always set bot ready
    data.otherStrangers[botName].changeTargetPosition()
    playerNum += 1
    
    #send bot msg to other player
    msg = "addBot %s %s\n" %(botName,botColor)
    
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())


####################################
# custom functions
####################################


#draw a player's trail on paper
def drawOneCircle(canvas,cx,cy,size,color):
    c = canvas.create_oval(cx - size, cy - size,
                       cx + size, cy + size, fill = color,width = 0)
    
#draw a single player's circle
def drawPlayerCircle(canvas,player):
    cx = player.x
    cy = player.y
    size = player.size
    color = player.color
    drawOneCircle(canvas,cx,cy,size,color)

#draw all the player's circle
def drawCircles(canvas,data):
    drawPlayerCircle(canvas,data.me)
    
    for PID in data.otherStrangers:
      drawPlayerCircle(canvas,data.otherStrangers[PID])
    


def distance(x1,y1,x2,y2):
  return ((x1-x2)**2 + (y1-y2)**2)**0.5

def drawSquare(canvas,x,y,size):
  #canvas.create_rectangle(x-size,y-size,x+size,y+size,fill='purple')
  pass

#send a request to other user to get their position
def requestPosition(data):
    msg = "requestPosition\n"
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())

#send my Position to rPID 
def sendMyPosition(data,rPID):
    msg = "synPosition %s %d %d\n" % (rPID,data.me.x,data.me.y)
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())

#move the painter forward and send message to other client
def painterMove(data):
    msg = ""
    # move myself
    (dx,dy) = data.me.moveForward(data)
    # update message to send
    #if data.counter > 10:
    msg = "playerMoveTo %d %d\n" % (dx, dy)
   #   data.counter = 0
    
    # send the message to other players!
    if (msg != ""):
    #  print ("sending: ", msg,)
      data.server.send(msg.encode())
    
    if data.me.PID == 'A':
      painterMoveBot(data)


def painterMoveBot(data):
    msg = ""
    for PID in data.otherStrangers:
      player = data.otherStrangers[PID]
      if player.isBot == True:
        (dx,dy) = player.moveForward(data)
        msg = "botMoveTo %s %d %d\n" % (PID,dx, dy)
        
      if (msg != ""):
      #  print ("sending: ", msg,)
        data.server.send(msg.encode())
    

def countDownTimer(data):
    data.time -= data.timerDelay/1000
    
    if data.time < 0:
      data.gameState = "end"
      updateResult(data)
    
    data.resultCounter +=data.timerDelay
    #if data.resultCounter > 5000:
    #  data.resultCounter = 0
     # updateResult(data)
    

def responseFromServer(data):
    # print(serverMsg.qsize())
    # timerFired receives instructions and executes them
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
       
        msg = msg.split()
        command = msg[0]
        if not (command == "playerMoveTo" or command == "botMoveTo"):
          print("received: ", msg, "\n")

        if (command == "myIDis"):
          myPID = msg[1]
          myColor = msg[2]
          data.me.changePID(myPID)
          data.me.changeColor(myColor)
          data.numPlayers += 1

        elif (command == "newPlayer"):
          newPID = msg[1]
          newColor = msg[2]
          x = data.width/2
          y = data.height/2
          data.otherStrangers[newPID] = Painter(newPID,x, y,
                                                data.width,data.height,
                                                color = newColor)
          data.numPlayers += 1
        
        elif(command == "addBot"):
          PID = msg[1]
          newPID = msg[2]
          newColor = msg[3]
          
          x = data.width/2
          y = data.height/2
          data.otherStrangers[newPID] = Painter(newPID,x, y,
                                                data.width,data.height,
                                                color = newColor)
          data.otherStrangers[newPID].isBot = True
          data.otherStrangers[newPID].ready = True
          data.numPlayers += 1
        
        elif(command == "updateResult"):
          sPID = msg[1]
          PID = msg[2]
          p = float(msg[3])
          if PID == data.me.PID:
            data.me.percentage = p
          else:
            data.otherStrangers[PID].percentage = p
          findWinner(data)
        
        elif(command == "addPowerUp"):
          PID = msg[1]
          x = int(msg[2])
          y = int(msg[3])
          name = msg[4]
          newPowerUp = PowerUp(x,y,name)
          data.powerups.append(newPowerUp)
        
        elif (command == "addBlock"):
          sendPID = msg[1]
          x = int(msg[2])
          y = int(msg[3])
          size = int(msg[4])
          newBlock = Block(x,y,size)
          data.blocks.append(newBlock)
          print(data.blocks)
        
        elif(command == "ready"):
          PID = msg[1]
          data.otherStrangers[PID].changeReady(True)
        
        elif (command == "changeName"):
          PID = msg[1]
          newName = msg[2]
          data.otherStrangers[PID].changeName(newName)
        
        elif (command == "playerMoveTo"):
          PID = msg[1]
          x = int(msg[2])
          y = int(msg[3])
          data.otherStrangers[PID].teleport(x,y)
        
        elif (command == "botMoveTo"):
          sendPID = msg[1]
          PID = msg[2]
          x = int(msg[3])
          y = int(msg[4])
          data.otherStrangers[PID].teleport(x,y)

        elif (command == "playerTeleported"):
          PID = msg[1]
          x = int(msg[2])
          y = int(msg[3])
          data.otherStrangers[PID].teleport(x, y)
        
        elif (command == "squareSpawn"):
          PID = msg[1]
          x = int(msg[2])
          y = int(msg[3])
          data.squares.append((x,y))
        
        elif (command == "synSettings"):
          requestPosition(data)
        
        elif(command == "requestPosition"):
          rPID = msg[1]
          sendMyPosition(data,rPID)
        
        elif(command == "synPosition"):
          sPID = msg[1] #syn PID
          rPID = msg[2] #request PID
          x = int(msg[3])
          y = int(msg[4])
          if(data.me.PID == rPID):
            data.otherStrangers[sPID].teleport(x,y)
          
      except:
        print("failed")
      serverMsg.task_done()


def initAll(data):
    #use for tech demo, generate powerups in every client
    data.squares = []
    data.squareSize = 10
    
    #game state
    data.gameState = "menu"
    
    data.drawCounter = 0
    data.counter = 0
    data.resultCounter = 0
    
    data.menuButtons = []
    initMenuButton(data)
    
    initName(data)
    initSelectButton(data)
    initEndButton(data)
    
    initGameSetting(data)
    initPowerups(data)
    initInstructionButton(data)
    data.blocks = []
    
    data.numReadyPlayers = 0
    data.initClear = False
    
    data.winner = data.me
    
    delGroup = []
    for PID in data.otherStrangers:
      player = data.otherStrangers[PID]
      if player.isBot:
        delGroup.append(PID)
        continue
      player.reset()
    
    for PID in delGroup:
      del data.otherStrangers[PID]
    
    data.me.reset()
    
    
####################################
# tkinter
####################################

def init(data):
    data.otherStrangers = dict()
    data.me = Painter("A",data.width/2, data.height/2,
                      data.width,data.height)
    
    data.numPlayers = 0
    
    data.updateShapes = []
    
    data.imageName = "instruction.gif"
    
    #frame = 25
    data.timerDelay = 40
    
    initAll(data)
    
def mousePressed(event, data):
    msg = ""
    
    if data.gameState == "menu":
      for button in data.menuButtons:
        if button.clicked(event.x,event.y):
          if button.name == "online":
            data.gameState = "name"
            print("enter name\n")
            return
          if button.name == "instruction":
            data.gameState = "instruction"
    elif data.gameState == "instruction":
      for button in data.instructionButtons:
        if button.clicked(event.x,event.y):
          if button.name == "back":
            data.gameState = "menu"
    elif data.gameState == "name":
      for button in data.nameButtons:
        if button.clicked(event.x,event.y):
          data.me.name = data.newName
          msg = "changeName %s\n" % (data.newName)
          data.gameState = "select"
    elif data.gameState == "select":
      for button in data.selectButtons:
        if button.clicked(event.x,event.y):
          if button.name == "ready":
            msg = "ready LLL\n" 
            data.me.changeReady(True)
          elif button.name == "bot":
            addBot(data)
    elif data.gameState == "end":
      for button in data.endButtons:
        if button.clicked(event.x,event.y):
          data.gameState = "menu"
          initAll(data)
    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())
    

def keyPressed(event, data):
    msg = ""
    if data.gameState == "menu":
      pass
    elif data.gameState == "name":
      if event.keysym in string.ascii_letters:
        if len(data.newName) < 12:
          data.newName += event.keysym
      elif event.keysym == "BackSpace": #delete
        if len(data.newName) > 0:
          data.newName = data.newName[:-1]
    elif data.gameState == "game":
      # Turn
      if event.keysym in ["Left", "Right"]:
          if event.keysym == "Left":
              data.me.turn(data.me.turnSpeed)
          elif event.keysym == "Right":
              data.me.turn(-data.me.turnSpeed)
      # teleporting
      elif event.keysym == "space":
        # get a random coordinate
        x = random.randint(0, data.width)
        y = random.randint(0, data.height)
        # teleport myself
        data.me.teleport(x, y)
        # update the message
        msg = "playerTeleported %d %d\n" % (x, y)
    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())


def timerFired(canvas,data):
    if data.gameState == "menu":
      pass
    elif data.gameState == "game":
      moveAllBot(data)
      painterMove(data)
      drawPaper(canvas,data)
      countDownTimer(data)
      updateResultOnPaper(data)
      updatePowerUp(data)
    elif data.gameState == "select":
      if checkAllReady(data):# and len(data.otherStrangers) > 0:
        data.gameState = "game"
        if data.me.PID == 'A':
          initBlock(data)
        data.me.initPosition()
        
    responseFromServer(data)
    
def clearAll(canvas):
    for item in canvas.find_all():
      canvas.delete(item)
    

def redrawAll(canvas, data):
    if not data.initClear:
      data.initClear = True
      clearAll(canvas)
      
    if data.gameState == "menu":
      drawMenuWindow(canvas,data)
    elif data.gameState == "name":
      drawChangeName(canvas,data)
    elif data.gameState == "instruction":
      drawInstruction(canvas,data)
    elif data.gameState == "select":
      drawMenuWindow(canvas,data)
      drawSelectWindow(canvas,data)
    elif data.gameState == "game":
      # draw other players
      for playerName in data.otherStrangers:
        data.otherStrangers[playerName].drawPainter(canvas,data)
      # draw me
      data.me.drawPainter(canvas,data)
      
      #draw power-up
      for powerup in data.powerups:
        powerup.drawPowerUp(canvas,data)
      
      # draw blocks
      for block in data.blocks:
        block.drawBlock(canvas,data)

      # draw UI
      drawGameUI(canvas,data)
      
    elif data.gameState == "end":
      drawResult(canvas,data)
    

def drawPaper(canvas,data):
    data.drawCounter += 1
    if data.drawCounter > 1:
      drawCircles(canvas,data)
      data.drawCounter = 0

####################################
# use the run function as-is
####################################

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        for i in data.updateShapes:
          canvas.delete(i)
          data.updateShapes.remove(i)
        redrawAll(canvas, data) 
        
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
       # redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas,  data):
        keyPressed(event, data)
      #  redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        time1 = time.time()
        timerFired(canvas,data)
        redrawAllWrapper(canvas, data)
        time4 = time.time()
        dall = (time4 - time1) * 1000
        # pause, then call timerFired again
        canvas.after(int(max(data.timerDelay - dall,0)), timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(600, 600, serverMsg, server)
