#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
import time
import string
from queue import Queue

HOST = "" # put your IP address here if playing on multiple computers
PORT = 50061

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

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

from tkinter import *
from painter import *
from click_button import *
import random
####################################
# menu
####################################

def drawMenuWindow(canvas,data):
  if data.gameState == "menu" or data.gameState == "select":
    menu = canvas.create_text(data.width / 2, data.height / 5,
                              text = "Painter Battle",fill="black",
                              font="Times 38 bold" )
    data.updateShapes.append(menu)
    
    for button in data.menuButtons:
      button.drawButton(data,canvas)
    
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
     
    player = data.me
    items = ["Player:",player.name,player.color,player.getReadyStr()]
    drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
    offsetY += gridY
    
    for PID in data.otherStrangers:
      player = data.otherStrangers[PID]
      items = ["Player:",player.name,player.color,player.getReadyStr()]
      drawSelectRow(canvas,data,items,offsetX,offsetY,gridX)
      offsetY += gridY
    
    for button in data.selectButtons:
      button.drawButton(data,canvas)
    

def drawSelectRow(canvas,data,items,offsetX,offsetY,gridX):
    for item in items:
      t = canvas.create_text(offsetX,offsetY,text = item,fill="yellow",
                        font="Times 12 bold")
      offsetX += gridX
      data.updateShapes.append(t)
    
    
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

def drawGameUI(canvas,data):
    text_time = canvas.create_text(data.width - 30,30,anchor = NE,
                              text="Time:"+str(int(data.time)), fill="black",
                              font="Times 10 bold"
                              )
    data.updateShapes.append(text_time)



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
              data.otherStrangers.pixels += 1
    
    data.me.updatePercentage(data.rows * data.cols)
    for PID in data.otherStrangers:
      data.otherStrangers[PID].updatePercentage(data.rows * data.cols)

def initGameSetting(data):
    data.time = 40
    data.me.percentage = 0
    data.resultUpdateTime = 5000
    
    for PID in data.otherStrangers:
      data.otherStrangers[PID].percentage = 0
    
    data.rows = data.height
    data.cols = data.width
    #use to record every pixel's color.
    data.paper = [ ([""] * data.cols) for row in range(data.rows) ]
    

def initSelectButton(data):
    data.selectButtons = []
    
    button_ready = ClickButton(300-50,450-20,
                                   300+50, 450+20,
                                    "ready",
                                    "Ready!",40,'yellow')
    data.selectButtons.append(button_ready)
    
def initName(data):
    data.newName = ""
    data.nameButtons = []
    
    button_done_name = ClickButton(300-50,450-20,
                                   300+50, 450+20,
                                    "done_name",
                                    "Done!",40,'yellow')
    data.nameButtons.append(button_done_name)
    

def initMenuButton(data):
    offsetX = data.width/3
    offsetY = data.height/3
    
    buttonX = 200
    buttonY = 50
    fontSize = 30
    buttonInter = 20
    
    button_play_online = ClickButton(offsetX,offsetY,
                                    offsetX + buttonX, offsetY + buttonY,
                                    "online",
                                    "Start Game!",fontSize,'orange')
    data.menuButtons.append(button_play_online)
    
    button_play_offline = ClickButton(offsetX,
                                      offsetY + buttonY + buttonInter ,
                                      offsetX + buttonX , 
                                      offsetY + buttonY * 2 + buttonInter,
                                      "offline",
                                      "Offline Game!",fontSize,'orange')
    data.menuButtons.append(button_play_offline)
    
    button_play_instruction = ClickButton(offsetX,
                                          offsetY + buttonY * 2 + buttonInter *2,
                                          offsetX + buttonX, 
                                          offsetY + buttonY * 3 + buttonInter *2,
                                          "insturction",
                                          "How to Play?",fontSize,'orange')
    
    data.menuButtons.append(button_play_instruction)
      

def checkAllReady(data):
  if not data.me.ready:
    return False
  for PID in data.otherStrangers:
    player = data.otherStrangers[PID]
    if not player.ready:
      return False
  return True

####################################
# custom functions
####################################


#draw a player's trail on paper
def drawOneCircle(canvas,cx,cy,size,color):
    c = canvas.create_oval(cx - size, cy - size,
                       cx + size, cy + size, fill = color,width = 0)
    

def drawPlayerCircle(canvas,player):
    cx = player.x
    cy = player.y
    size = player.size
    color = player.color
    drawOneCircle(canvas,cx,cy,size,color)

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


def painterMove(data):
    data.counter += 1
    msg = ""
    # move myself
    (dx,dy) = data.me.moveForward()
    # update message to send
    #if data.counter > 10:
    msg = "playerMoveTo %d %d\n" % (dx, dy)
   #   data.counter = 0
    
    # send the message to other players!
    if (msg != ""):
    #  print ("sending: ", msg,)
      data.server.send(msg.encode())
    

def countDownTimer(data):
    data.time -= data.timerDelay/1000
    
    data.resultCounter +=data.timerDelay
    if data.resultCounter > 5000:
      data.resultCounter = 0
      updateResult(data)
    

def responseFromServer(data):
    # print(serverMsg.qsize())
    # timerFired receives instructions and executes them
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
       
        msg = msg.split()
        command = msg[0]
        if not command == "playerMoveTo":
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


####################################
# tkinter
####################################

def init(data):
    data.me = Painter("A",data.width/2, data.height/2,
                      data.width,data.height)
    data.otherStrangers = dict()
    
    #use for tech demo, generate powerups in every client
    data.squares = []
    data.squareSize = 10
    
    #frame = 25
    data.timerDelay = 40
    
    #game state
    data.gameState = "menu"
    
    data.updateShapes = []
    
    data.drawCounter = 0
    data.counter = 0
    data.resultCounter = 0
    
    data.menuButtons = []
    initMenuButton(data)
    
    initName(data)
    initSelectButton(data)
    
    initGameSetting(data)
    
    data.numPlayers = 0
    data.numReadyPlayers = 0


def mousePressed(event, data):
    msg = ""
    
    if data.gameState == "menu":
      for button in data.menuButtons:
        if button.clicked(event.x,event.y):
          if button.name == "online":
            data.gameState = "name"
            return
    elif data.gameState == "name":
      for button in data.nameButtons:
        if button.clicked(event.x,event.y):
          data.me.name = data.newName
          msg = "changeName %s\n" % (data.newName)
          data.gameState = "select"
    elif data.gameState == "select":
      for button in data.selectButtons:
        if button.clicked(event.x,event.y):
          msg = "ready LLL\n" 
          data.me.changeReady(True)
          
    
    
    
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
      painterMove(data)
      drawPaper(canvas,data)
      countDownTimer(data)
    elif data.gameState == "select":
      if checkAllReady(data):# and len(data.otherStrangers) > 0:
        data.gameState = "game"
        
    responseFromServer(data)
    
   

def redrawAll(canvas, data):
    if data.gameState == "menu":
      drawMenuWindow(canvas,data)
    elif data.gameState == "name":
      drawChangeName(canvas,data)
    elif data.gameState == "select":
      drawMenuWindow(canvas,data)
      drawSelectWindow(canvas,data)
    elif data.gameState == "game":
      # draw other players
      for playerName in data.otherStrangers:
        data.otherStrangers[playerName].drawPainter(canvas,data)
      # draw me
      data.me.drawPainter(canvas,data)
      
      # draw UI
      drawGameUI(canvas,data)
    
    

def drawPaper(canvas,data):
    data.drawCounter += 2
    if data.drawCounter > 1:
      drawCircles(canvas,data)
      data.drawCounter = 0

####################################
# use the run function as-is
####################################

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        time1 = time.time()
        for i in data.updateShapes:
          canvas.delete(i)
          data.updateShapes.remove(i)
        redrawAll(canvas, data) 
        time2 = time.time()
        #for i in data.updateShapes:
        #canvas.update()
        time3 = time.time()
        d1 = (time2 - time1) * 1000
        d2 = (time3 - time2) * 1000
       # print("ddd:(%d,%d)" %(d1,d2))
        
    
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
       # redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas,  data):
        keyPressed(event, data)
      #  redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        time1 = time.time()
        timerFired(canvas,data)
        time2 = time.time()
        time3 = time.time()
        redrawAllWrapper(canvas, data)
        time4 = time.time()
        dall = (time4 - time1) * 1000
        d1 = (time2 - time1) * 1000
        d2 = (time3 - time2) * 1000
        d3 = (time4 - time3) * 1000
        
        
      #  print("%.2f(%.2f,%.2f,%.2f)" %(dall,d1,d2,d3))
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
    
   # canvasPaper = Canvas(root, width=data.width, height=data.height)
   # canvasPaper.pack()
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
