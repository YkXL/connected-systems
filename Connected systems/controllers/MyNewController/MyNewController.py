from re import L
from controller import Supervisor
import socket
import pickle

rechts = 1
achter = 2
links = 3
voor = 4

robot = Supervisor()
supervisorNode = robot.getSelf()
timestep = int(robot.getBasicTimeStep())


ledRechts = robot.getDevice("LEDRechts")
ledAchter = robot.getDevice("LEDAchter")
ledLinks = robot.getDevice("LEDLinks")
ledVoor = robot.getDevice("LEDVoor")

sensorRechts = robot.getDevice("sensorRechts")
sensorAchter = robot.getDevice("sensorAchter")
sensorLinks = robot.getDevice("sensorLinks")
sensorVoor = robot.getDevice("sensorVoor")

output = []
input = []

sendToServer = []

#send ("Rood", [(None, 0), ("B1", 0), ("A2", 0), (None, 0)], "A1")


# move the robot in the right direction
def move(i):
    pos = supervisorNode.getPosition()
    trans = supervisorNode.getField("translation")
    if i == rechts:
        pos[0] = pos[0] - 0.1
        trans.setSFVec3f(pos)
    elif i == achter:
        pos[1] = pos[1] + 0.1
        trans.setSFVec3f(pos)
    elif i == links:
        pos[0] = pos[0] + 0.1
        trans.setSFVec3f(pos)
    elif i == voor:
        pos[1] = pos[1] - 0.1
        trans.setSFVec3f(pos)
    else:
        print("that is not a direction")
# turn on the LED in wich way the robot is going
def turnOnLED(i):

    ledRechts.set(0)
    ledAchter.set(0)
    ledLinks.set(0)
    ledVoor.set(0)
    if i == rechts:
        ledRechts.set(1)
    elif i == achter:
        ledAchter.set(1)
    elif i == links:
        ledLinks.set(1)
    elif i == voor:
        ledVoor.set(1)
    else:
        print("not an option")
# turns on the sensor in wich way the robot is going
def turnOnSensor(i):

    if i == rechts:
        sensorRechts.enable(100)
        return sensorRechts
    elif i == achter:
        sensorAchter.enable(100)
        return sensorAchter
    elif i == links:
        sensorLinks.enable(100)
        return sensorLinks
    elif i == voor:
        sensorVoor.enable(100)
        return sensorVoor
    else:
        print("not an option")
        return None
#function to check if there is an obstacle in the given direction
def getObstacle(i):
    o = False
    if (turnOnSensor(i).getValue() != 1000):
        o = True
    return o
#function to operate evertying in the right direction
def go(direction):
    cordinates = chessToCordinates(direction)
    print("go to", cordinates)
    posNow = supervisorNode.getPosition()
    print("is now", posNow)
    if int(cordinates[0] * 10) > int(posNow[0] * 10):
        go = links
        posNow[0] = posNow[0] + 0.1
        print("rechts")
    elif int(cordinates[0] * 10) < int(posNow[0] * 10):
        go = rechts
        posNow[0] = posNow[0] - 0.1
        print("links")
    elif int(cordinates[1] * 10) >int( posNow[1] * 10):
        go = achter
        posNow[1] = posNow[1] + 0.1
        print("voor")
    elif int(cordinates[1] * 10) < int(posNow[1] * 10):
        go = voor
        posNow[1] = posNow[1] - 0.1
        print("achter")
    else:
        go = 5
    if go != 5 :
        turnOnLED(go)
        sensor = turnOnSensor(go)
        print(sensor.getValue())
        if(sensor.getValue() == 1000):
            move(go)
            return True, ""
        return False
    else:
        print("that is not a direction")
        return False, ""
#dijkstra cordinates to webots cordinats
def chessToCordinates(chess):
    x = (ord(chess[0]) - 65) * 0.1
    if len(chess) == 2:
        y = (int(chess[1])-1) * 0.1
    else :
        y = (int(chess[1]+chess[2])-1) / 10
    return y,x
#webot cordinates to dijkstra cordinates
def cordinatesToChess(cordinates):
    x = chr(int((cordinates[1] / 0.1) + 65))
    y = str(int((cordinates[0] / 0.1))+ 1)
    if x > 75 or x < 65 or y > 11 or y < 1:
        return None
    return x+y
def getSideCord(i):
    posNow = supervisorNode.getPosition()
    if i == rechts:
        posNow[0] = posNow[0] - 0.1
    elif i == achter:
        posNow[1] = posNow[1] + 0.1
    elif i == links:
        posNow[0] = posNow[0] + 0.1
    elif i == voor:
        posNow[1] = posNow[1] - 0.1
    else:
        print("Dat is geen kant!")
        return None
    return cordinatesToChess(posNow)

turnOnSensor(links)
turnOnSensor(rechts)
turnOnSensor(achter)
turnOnSensor(voor)
duration = (1000 // timestep) * timestep
#main loop
def robotMovement():
    kleur = robot.getName()
    directions = []
    while robot.step(duration) != -1:

        if directions != []:
            go(directions[0])
            # print("Obstacle:", obstacle)
            print("rechts:", getSideCord(rechts), getObstacle(rechts))
            print("achter", getSideCord(achter), getObstacle(achter))
            print("links", getSideCord(links), getObstacle(links))
            print("voor", getSideCord(voor), getObstacle(voor))
            obstakels = [(getSideCord(rechts), getObstacle(rechts)),(getSideCord(achter), getObstacle(achter)),(getSideCord(links), getObstacle(links)),(getSideCord(voor), getObstacle(voor))]
            sendToServer.append(kleur, obstakels, cordinatesToChess(supervisorNode.getPosition()))
        else:
            break
        # input.append((kleur, cordinatesToChess(supervisorNode.getPosition()), obstacle))


dataBuffer = []

#function to communicate to the server
def serverCommunication():
    i = 0
    speaking = True
    doorServer = False
    doorClient = False
    port = 1024


    try:
        while i == 0:
            # CLIENT
            if speaking == True:
                port = 1024
                s = socket.socket()
                s.connect(("localhost", port))


                if len(sendToServer) == 0:
                    s.sendall(pickle.dumps(("null", "null", "null")))
                else:
                    data = pickle.dumps(sendToServer[0])
                    s.send(data)
                    # print("webot kant heeft", input[0], "verzonden")
                    input.remove(sendToServer[0])
                s.close()



                speaking = False
                doorServer = False
                print(speaking)
            # SERVER
            if speaking == False:

                if robot.getName() == "Rood":
                    # print("rood is nu 1025")
                    port = 1025
                if robot.getName() == "Geel":
                    # print("geel is nu 1026")
                    port = 1026
                if doorServer == False:
                    print(robot.getName(), "zit nu in server en wilt ontvangen")
                    s = socket.create_server(("localhost", port))
                    s.listen()
                    # print("nu in server met port", port)

                    doorServer = True
                conn, addr = s.accept()
                # print("Connection accepted from", addr)
                data = conn.recv(4096)
                data = pickle.loads(data)
                output.append(data)
                # print("output", output)
                speaking = True
                doorSpeaking = False
            i = 1

    except Exception as e:
        print(e)
        exit()
robotMovement()
