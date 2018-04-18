#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
from queue import Queue

HOST = "" # put your IP address here if playing on multiple computers
PORT = 50012

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

import random
####################################
# custom functions
####################################

#draw a player's trail on paper
def drawOnPaper(data,player):
    for (x,y) in getPixelCircleList(data,player.x,player.y,player.size):
      data.paper[x][y] = player.PID

#draw all the players' trail on paper
def drawAllOnPaper(data):
    drawOnPaper(data,data.me)
    for PID in data.otherStrangers:
      drawOnPaper(data,data.otherStrangers[PID])

#draw all the color on paper, pixel by pixel
#super slow
def drawPaper(canvas,data):
    rows = len(data.paper)
    cols = len(data.paper[0])
    
    for x in range(rows):
      for y in range(cols):
        pid = data.paper[x][y]
        if not pid == "":
          if pid == data.me.PID: 
            color = data.me.color
            canvas.create_line(x,y,x+1,y+1,fill = color)
          elif pid in data.otherStrangers:
            color = data.otherStrangers[pid].color
            canvas.create_line(x,y,x+1,y+1,fill = color)

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
    # move myself
    (dx,dy) = data.me.moveForward()
    # update message to send
    msg = "playerMoveTo %d %d\n" % (dx, dy)
    
    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())
    


####################################
# tkinter
####################################

def init(data):
    data.me = Painter("Lonely", data.width/2, data.height/2,
                      data.width,data.height)
    data.otherStrangers = dict()
    
    #use for tech demo, generate powerups in every client
    data.squares = []
    data.squareSize = 10
    
    #frame = 50
    data.timerDelay = 20
    
    #game state
    data.gameState = "start"
    
    data.rows = data.height
    data.cols = data.width
    #use to record every pixel's color.
    data.paper = [ ([""] * data.cols) for row in range(data.rows) ]

def mousePressed(event, data):
    data.squares.append((event.x,event.y))
    msg = "squareSpawn %d %d\n" % (event.x, event.y)
    
    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())
    

def keyPressed(event, data):
    msg = ""

    # Turn
    if event.keysym in ["Up", "Down", "Left", "Right"]:
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
    
    #Debug Mode Key
    elif event.keysym == "s":
      requestPosition(data)
      return

    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())

def timerFired(data):
    painterMove(data)
    drawAllOnPaper(data)
    
    # timerFired receives instructions and executes them
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        print("received: ", msg, "\n")
        msg = msg.split()
        command = msg[0]

        if (command == "myIDis"):
          myPID = msg[1]
          myColor = msg[2]
          data.me.changePID(myPID)
          data.me.changeColor(myColor)
         # requestPosition(data)

        elif (command == "newPlayer"):
          newPID = msg[1]
          newColor = msg[2]
          x = data.width/2
          y = data.height/2
          data.otherStrangers[newPID] = Painter(newPID, x, y,
                                                data.width,data.height,
                                                color = newColor)

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
          #myPID = msg[1]
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
      

def redrawAll(canvas, data):
    drawPaper(canvas,data)
    
    # draw other players
    for playerName in data.otherStrangers:
      data.otherStrangers[playerName].drawPainter(canvas)
    # draw me
    data.me.drawPainter(canvas)
    
    #draw purpleSquare
    for square in data.squares:
      drawSquare(canvas,square[0],square[1],data.squareSize)
    

####################################
# use the run function as-is
####################################

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
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

run(200, 200, serverMsg, server)
