import socket
import time
import pickle

rows = columns = 11
objects = []
fromRobots = []
nrOfRobots = 0

# Define all Nodes with all it's adjecent Nodes with their corresponding wheight
adjecent = {}
currentLetter = '@'  # Next is 'A' -> 'B' etc.
startNode = 'A1'
firstLetter = chr(65)
lastLetter = chr(65+rows-1)
robots = []


class Robot:
    def __init__(self, currentPosition, name, destination=None, plannedPos=None):
        self.currentPosition = currentPosition
        self.destination = destination
        self.priority = nrOfRobots
        self.name = name
        self.plannedPos = plannedPos


def updateDetails(data):
    for object in range(len(data[1])):
        if data[1][object][0] is not None:
            if data[1][object][1] == 1:
                objects.append(data[1][object][0])
    updateObjecs()


# Makes a dicionary with every adjecent nodes on the chessboard.
for row in range(rows):
    currentLetter = chr(ord(currentLetter)+1)
    for column in range(1, columns+1):
        if currentLetter == firstLetter and column == 1:
            adjecent[currentLetter+str(column)] = [(
                (chr(ord(firstLetter)+1)+str(column)), 1), (firstLetter+str(column+1), 1)]
        elif currentLetter == firstLetter and column == 11:
            adjecent[currentLetter+str(column)] = [((chr(ord(firstLetter)+1)+str(
                column)), 1), (chr(ord(firstLetter)+1)+str(column-1), 1)]
        elif currentLetter == firstLetter:
            adjecent[currentLetter+str(column)] = [(currentLetter+str(column-1), 1),
                                                   (currentLetter+str(column+1), 1), (chr(ord(currentLetter)+1)+str(column), 1)]
        elif currentLetter == lastLetter and column == 1:
            adjecent[currentLetter+str(column)] = [((chr(ord(lastLetter)-1)+str(
                column)), 1), ((chr(ord(lastLetter))+str(column+1)), 1)]
        elif currentLetter == lastLetter and column == 11:
            adjecent[currentLetter+str(column)] = [((chr(ord(lastLetter)-1)+str(
                column)), 1), ((chr(ord(lastLetter))+str(column-1)), 1)]
        elif currentLetter == lastLetter:
            adjecent[currentLetter+str(column)] = [(currentLetter+str(column-1), 1),
                                                   (currentLetter+str(column+1), 1), (chr(ord(currentLetter)-1)+str(column), 1)]
        elif column == 1:
            adjecent[currentLetter+str(column)] = [(currentLetter+str(column+1), 1), (chr(
                ord(currentLetter)+1)+str(column), 1), (chr(ord(currentLetter)-1)+str(column), 1)]
        elif column == 11:
            adjecent[currentLetter+str(column)] = [(currentLetter+str(column-1), 1), (chr(
                ord(currentLetter)+1)+str(column), 1), (chr(ord(currentLetter)-1)+str(column), 1)]
        else:
            adjecent[currentLetter+str(column)] = [(currentLetter+str(column-1), 1), (currentLetter+str(
                column+1), 1), (chr(ord(currentLetter)+1)+str(column), 1), (chr(ord(currentLetter)-1)+str(column), 1)]
# print(adjecent)


def updateObjecs():
    # Every object gets a weight of 100.000
    for node in adjecent:
        for element in range(len(adjecent[node])):
            if adjecent[node][element][0] in objects:
                adjecent[node][element] = (adjecent[node][element][0], 100000)


def dijkstra(currentLocation, destination):
    # Define a nodeTable where the shortest routes for each nodes are stored
    nodeTable = {}
    firstLetter = True

    for letter in adjecent:
        nodeTable[letter] = [1000, None]
    nodeTable[startNode] = [0, None]

    print(nodeTable)

    notVisited = list(nodeTable.keys())

    for node in nodeTable:
        # Make the currentNode the node with the lowest wheigt in the nodeTable
        # Mark this Node as 'visited'
        currentNode = min(notVisited, key=nodeTable.get)
        notVisited.remove(currentNode)

        for pathes in range(len(adjecent[currentNode])):
            pathLetter = adjecent[currentNode][pathes][0]
            totalNewPathWeight = adjecent[currentNode][pathes][1] + \
                nodeTable[currentNode][0]
            oldPathWeight = nodeTable[adjecent[currentNode][pathes][0]][0]

            # If an adjent node from the currentNode is not visted, check if combined wheigt is lower than before.
            if pathLetter in notVisited and totalNewPathWeight < oldPathWeight:
                # If the combined wheight is lower, update the nodeTable with the new shortes route.
                nodeTable[pathLetter][0] = totalNewPathWeight
                nodeTable[pathLetter][1] = currentNode

    directions = []
    prev = destination
    currentLocation

    while True:
        node = nodeTable[prev][1]
        node = directions.append(nodeTable[prev][1])
        prev = nodeTable[prev][1]
        if prev == currentLocation:
            directions.insert(0, destination)
            directions.reverse()
            break
    return directions[1]


def destinationReached(name):
    for robot in robots:
        if robot.name == name:
            if robot.currentPosition == robot.destination:
                robot.destination = None


i = 0
speaking = False
doorServer = False
doorClient = False
port = 1024
output = []

dataBuffer = []
dataBuffer.append(("Rood", "F6"))
dataBuffer.append(("Geel", "J5"))
sendToDashboard = [("Rood", "F6"), ("Geel", "J6"),
                   ("Blauw", "A11"), ("Groen", "C2")]


def sendMessage(port, index):
    # time.sleep(1)
    # als index meer dan 0 is, moet het naar een robot verstuur worden
    if index > 0:
        s = socket.socket()
        s.connect(("localhost", port))
        robots[index].plannedPos = dijkstra(
            robots[index].currentPosition, robots[index].destination)
        data = pickle.dumps(robots[index].plannedPos)
        s.sendall(data)
        print(robots[index].plannedPos, "verstuurd")


    # anders naar het dashboard
    elif index < 0 and len(sendToDashboard) > 0:
        s = socket.socket()
        s.connect(("localhost", port))
        data = pickle.dumps(sendToDashboard[0])
        s.sendall(data)
        print(sendToDashboard[0], "verstuurd")
        del sendToDashboard[0]
    
    else:
        s = socket.socket()
        s.connect(("localhost", port))
        data = pickle.dumps((None, None))
        s.sendall(data)



while True:

    # CLIENT
    if speaking == True:
        sendMessage(1023, -1)
        # for index in range(len(robots)):
        #     if robots[i].destination is not None:
        #         sendMessage(1025+index, index)
        speaking = False
    # SERVER
    if speaking == False:
        port = 1024
        if doorServer == False:
            s = socket.create_server(("localhost", port))
            s.listen()
            doorServer = True
        conn, addr = s.accept()
        data = pickle.loads(conn.recv(4096))
        # newRobot = True
        # for robot in robots:
        #     if robot.name == data[0]:
        #         newRobot == False
        # if newRobot:
        #     robots[nrOfRobots] = Robot(data[2], data[0])
        #     nrOfRobots += 1
        # updateDetails(data)
        print("ONTVANGEN:", data)
        speaking = True
        doorSpeaking = False
