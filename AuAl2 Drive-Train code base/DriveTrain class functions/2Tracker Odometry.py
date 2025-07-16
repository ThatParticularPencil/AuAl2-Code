#imports
from math import sin,cos,tan,pi,degrees,radians
Pos = (None,None)

def get_Heading():
    #must limit to 0-360 
    pass
def get_Tracker_F():
    #must calc distance
    pass
def get_Tracker_S():
    pass

def Linear_Odom():
    # Must be radians
    # forward /n turn
    curHeading = get_Heading() #these will need TrackerS values for arc based odom
    currentF = get_Tracker_F()
    deltaRelX = currentF - prevF
    avgHeading = (prevHeading+curHeading)/2

    #updates
    prevHeading = curHeading
    prevF = currentF

    #position vector change
    if 180 - avgHeading <= pi/2:
        limHeading = 180 -avgHeading
    else:
        limHeading = avgHeading

    deltaPos = (deltaRelX(cos(limHeading)), deltaRelX(sin(limHeading))) 
    FieldX,FieldY = Pos[0] + deltaPos[0], Pos[0] + deltaPos[1]

    Pos = (FieldX, FieldY)


    prevHeading = get_Heading()
    prevF = get_Tracker_F()
    prevS = get_Tracker_S()

print(Linear_Odom())