#############################
# Sockets Server Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
from queue import Queue

HOST = "" # put your IP address here if playing on multiple computers
PORT = 50061
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + readyMsg)
        command = msg.split("\n")
    except:
      # we failed
      print("wtf msg:"+msg)
      return

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0]
    instruction = msgList[1]
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
          print("> sent to %s:" % cID, sendMsg[:-1])
    print()
    serverChannel.task_done()

clientele = dict()
playerNum = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

names = ["A", "B", "C", "D"]
colors = ["red", "blue","green","orange"]

while True:
  client, address = server.accept()
  # myID is the key to the client in the clientele dictionary
  myID = names[playerNum]
  myColor = colors[playerNum]
  print(myID, myColor,playerNum)
  
  index = 0
  for cID in clientele:
    print (repr(cID), repr(playerNum))
    clientele[cID].send(("newPlayer %s %s\n" % (myID, myColor)).encode())
    client.send(("newPlayer %s %s\n" % (cID,colors[index])).encode())
    index += 1
  clientele[myID] = client
  client.send(("myIDis %s %s\n" % (myID,myColor)).encode())
  
  print("connection recieved from %s" % myID)
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1
  
  client.send(("synSettings \n").encode())