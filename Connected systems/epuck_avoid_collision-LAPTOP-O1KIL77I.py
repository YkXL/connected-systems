from controller import Supervisor

# robot = Supervisor()
# supervisorNode = robot.getSelf()

# timestep = int(robot.getBasicTimeStep())

# duration = (1000 // timestep) * timestep

# while robot.step(dureation) != -1:
    # if()
    

robot = Supervisor()
pos = supervisorNode.getPosition()

timestep = int(robot.getBasicTimeStep())

while robot.step(timestep) != -1:
    if(pos[0]>1.5):
        dir=-1
    if(pos[0]<-1.5):
        dir=1
    pos=[pos[0]+0.025*dir,pos[1],[2]]
    
    trans = supervisorNode.getField("name")
    trans = supervisorNode.getField("translation")
    trans.setSFVec3f(pos)