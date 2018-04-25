#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
import time
from queue import Queue

HOST = "" # put your IP address here if playing on multiple computers
PORT = 50016

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
    
    pass

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
    


def responseFromServer(data):
    # print(serverMsg.qsize())
    # timerFired receives instructions and executes them
    while (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
       # print("received: ", msg, "\n")
        msg = msg.split()
        command = msg[0]

        if (command == "myIDis"):
          myPID = msg[1]
          myColor = msg[2]
          data.me.changePID(myPID)
          data.me.changeColor(myColor)

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


####################################
# tkinter
####################################

def init(data):
    data.me = Painter("A", data.width/2, data.height/2,
                      data.width,data.height)
    data.otherStrangers = dict()
    
    #use for tech demo, generate powerups in every client
    data.squares = []
    data.squareSize = 10
    
    #frame = 25
    data.timerDelay = 40
    
    #game state
    data.gameState = "menu"
    
    data.rows = data.height
    data.cols = data.width
    #use to record every pixel's color.
    data.paper = [ ([""] * data.cols) for row in range(data.rows) ]
    
    data.updateShapes = []
    
    data.drawCounter = 0
    data.counter = 0


def mousePressed(event, data):
    msg = ""
    
    # send the message to other players!
    if (msg != ""):
      print ("sending: ", msg,)
      data.server.send(msg.encode())
    

def keyPressed(event, data):
    msg = ""

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
    painterMove(data)
    responseFromServer(data)
    
   

def redrawAll(canvas, data):
    
    # draw other players
    for playerName in data.otherStrangers:
      data.otherStrangers[playerName].drawPainter(canvas,data)
    # draw me
    data.me.drawPainter(canvas,data)
    
    

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
        drawPaper(canvas,data)
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

run(200, 200, serverMsg, server)
