import socket
import pickle
import string
import threading
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import Tk, Frame, Canvas

window = Tk()
window.geometry('740x650')
window.title("Dashboard")
sendToServer = []

frame = Frame(window)
frame.pack()
canvas = Canvas(frame, bg="white", width=740, height=650)
canvas.pack(expand=1, fill=BOTH)
background = PhotoImage(
    file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/map.png")
canvas.create_image(285, 285, image=background)
red = PhotoImage(file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/red.png")
canvas.create_image(225, 225, image=red)
green = PhotoImage(
    file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/green.png")
canvas.create_image(225, 225, image=green)
blue = PhotoImage(
    file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/blue.png")
canvas.create_image(225, 225, image=blue)
yellow = PhotoImage(
    file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/yellow.png")
canvas.create_image(225, 225, image=yellow)


def initDashboard():
    #--SEND COMMAND--#

    def getLocationInput():
        sendToServer.append((inputRobotColor.get(), inputLocation.get()))
        print(sendToServer)

    send = Label(window, text='Stuur')
    send.place(x=0, y=570)

    inputRobotColor = Entry(window)
    inputRobotColor.place(x=38, y=570)

    location = Label(window, text='naar locatie')
    location.place(x=123, y=570)

    inputLocation = Entry(window)
    inputLocation.place(x=190, y=570)

    sendCommand = Button(window, text='Verstuur command',
                         command=getLocationInput)
    sendCommand.place(x=320, y=570)

    #--QUEUE--#

    def getWachtrijInput():
        sendToServer.append((inputVanaf.get(), inputNaar.get()))
        print(sendToServer)

    pakop = Label(window, text='Pakop vanaf')
    pakop.place(x=0, y=595)

    inputVanaf = Entry(window)
    inputVanaf.place(x=38, y=595)

    naar = Label(window, text='en lever het bij')
    naar.place(x=123, y=595)

    inputNaar = Entry(window)
    inputNaar.place(x=210, y=595)

    wachtrijKnop = Button(
        window, text='Voegtoe aan wachtrij', command=getWachtrijInput)
    wachtrijKnop.place(x=340, y=595)

    #--STOP--#
    def getStopInput():
        sendToServer.append(("Stop"))
    stopKnop = Button(window, text='Stop!',
                      background="#FF0000", command=getStopInput)
    stopKnop.place(x=4, y=620)


locationWidget = Frame(window)
locationWidget.place(x=570, y=0)
locationTable = Treeview(locationWidget)
locationTable['columns'] = ('robot_kleur', 'locatie')
locationTable.column("#0", width=0,  stretch=NO)
locationTable.column("robot_kleur", anchor=CENTER, width=80)
locationTable.column("locatie", anchor=CENTER, width=80)
locationTable.heading("#0", text="", anchor=CENTER)
locationTable.heading("robot_kleur", text="Robot", anchor=CENTER)
locationTable.heading("locatie", text="Locatie", anchor=CENTER)
posRed = "(N/A, N/A)"
posGreen = "(N/A, N/A)"
posYellow = "(N/A, N/A)"
posBlue = "(N/A, N/A)"
locationTable.insert(parent='', index='end', iid=0,
                     text='', values=('Rood', posRed))
locationTable.insert(parent='', index='end', iid=1,
                     text='', values=('Groen', posGreen))
locationTable.insert(parent='', index='end', iid=2,
                     text='', values=('Geel', posYellow))
locationTable.insert(parent='', index='end', iid=3,
                     text='', values=('Blauw', posBlue))
locationTable.grid(column=570, row=0)

locationWidget = Frame(window)
locationWidget.place(x=570, y=250)
locationTable1 = Treeview(locationWidget)
locationTable1['columns'] = ('robot_kleur', 'intruction')
locationTable1.column("#0", width=0,  stretch=NO)
locationTable1.column("robot_kleur", anchor=CENTER, width=80)
locationTable1.column("intruction", anchor=CENTER, width=80)
locationTable1.heading("#0", text="", anchor=CENTER)
locationTable1.heading("robot_kleur", text="Robot", anchor=CENTER)
locationTable1.heading("intruction", text="Instructie", anchor=CENTER)
locationTable1.insert(parent='', index='end', iid=0,
                      text='', values=('Rood', '(0, 1)->(5, 1)'))
locationTable1.insert(parent='', index='end', iid=1,
                      text='', values=('Groen', '(6, 1)->(1, 5)'))
locationTable1.insert(parent='', index='end', iid=2,
                      text='', values=('Geel', '(2, 4)->(5, 9)'))
locationTable1.insert(parent='', index='end', iid=3,
                      text='', values=('Blauw', '(1, 5)->(6, 1)'))
locationTable1.grid(column=570, row=250)
frame = Frame(window)
frame.place(x=0, y=0)
canvas = Canvas(frame, bg="black", width=550, height=550)
canvas.place(x=0, y=0)


def moveRobot(data):
    x = (string.ascii_lowercase.index(data[1][0].lower())+1)*50-25
    y = (int(data[1][1:]))*50-25
    if data[0] == "Rood":
        global red
        red = PhotoImage(
            file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/red.png")
        canvas.create_image(x, y, image=red)
        posRed = str((x, y))
        print(locationTable.selection())
        # locationTable.insert(parent='', index='end', iid=0, text='', values=('Rood', posRed))
        locationTable.item(iid=0, text='blub', values=("Rood", posRed))
        locationTable.delete()

    elif data[0] == "Groen":
        global green
        green = PhotoImage(
            file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/green.png")
        canvas.create_image(x, y, image=green)
    elif data[0] == "Blauw":
        global blue
        blue = PhotoImage(
            file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/blue.png")
        canvas.create_image(x, y, image=blue)
    elif data[0] == "Geel":
        global yellow
        yellow = PhotoImage(
            file="C:/Users/tompr/School/Jaar 2/ConnectedSystems/yellow.png")
        canvas.create_image(x, y, image=yellow)


def serverCommunication():
    speaking = True
    doorServer = False

    while True:
        # CLIENT
        if speaking == True:
            window.update()

            port = 1024
            s = socket.socket()
            s.connect(("localhost", port))

            if len(sendToServer) > 0:
                data = pickle.dumps(sendToServer[0])
                del sendToServer[0]
            else:
                data = pickle.dumps((None, None))
            s.sendall(data)
            print("bericht verstuurd")
            s.close()
            speaking = False
            doorServer = False
            # SERVER
        if speaking == False:
            window.update()
            port = 1023
            if doorServer == False:
                s = socket.create_server(("localhost", port))
                s.listen()
                doorServer = True
            conn, addr = s.accept()
            data = pickle.loads(conn.recv(4096))
            print("ONTVANGEN:", data)
            if type(data) == tuple and data[0] is not None:
                moveRobot(data)
            speaking = True


initDashboard()
serverCommunication()
