wait(30,MSEC)

#imports
import time
import threading
from math import sin,cos,tan,asin,acos,atan,pi,degrees,radians,sqrt


################################
#          Variables           #
################################
StickDeadzone = .2
StickCurveShape = "parabolic"

TrackingDiameter = 2.75
WheelDiameter = 2.75

Acceltime = .7
VelConst = 1/(Acceltime**2)
MaxVelocity = 1
MaxTurnRadius = 10

BotWidth = 20

################################
#       CLASS DEFINITIONS      #
################################
class Sensor_Manager:
    def __init__(self):
        self.IsUpdated = False
        #self.time = time.time
        #self.prevtime = time.time
        #self.TrackerF = self.get_TrackerF
        self.Lstick = self.get_Lstick
        self.Rstick = self.get_Rstick
        #self.Velocity = self.get_Velocity
        #self.prevTrackerF = self.TrackerF
        #self.prevLstick = self.Lstick
        #self.prevRstick = self.Rstick
        #self.prevVelocity = self.Velocity
        
    def get_TrackerF(self):
        pass
    def get_Lstick(self):
        stick = None #v5 controller method
        #Sensitivity Curve
        if -1 <= stick <= -StickDeadzone:
            curvedstick = -(stick**2)
        elif StickDeadzone <= stick <= 1:
            curvedstick = stick**2
        else: curvedstick = 0
        self.Lstick = curvedstick

    def get_Rstick(self):
        stick = None #v5 controller method
        #Sensitivity Curve
        if -1 <= stick <= -StickDeadzone:
            curvedstick = -(stick**2)
        elif StickDeadzone <= stick <= 1:
            curvedstick = stick**2
        else: curvedstick = 0
        self.Rstick = curvedstick

    '''def get_Velocity(self):
        pass'''

    def update_Inputs(self):
        #self.Rstick = self.get_Rstick
        #self.Lstick = self.get_Lstick
        self.IsUpdated = True
        pass
    
    def update_Variables(self):
        self.prevtime = self.time
        #self.prevVelocity = self.Velocity
        #self.Velocity = self.get_Velocity
        #self.prevRstick = self.Rstick
        #self.Rstick = self.get_Rstick
        #self.prevLstick = self.Lstick
        #self.Lstick = self.get_Lstick
        #self.prevTrackerF = self.TrackerF
        #self.TrackerF = self.get_TrackerF
        self.IsUpdated = True


################################
#        FUNCS & INITS         #
################################

Sensors = Sensor_Manager
ClampActive = False

def low_pass_filter(vprev, value, alpha):
    return alpha*vprev +(1-alpha)*value

def CurvatureDrive(Lstick, Rstick):
    #Assuming Normalized RstickX Values to -1 < x < 1

    #Sensitivity Curve
    if Rstick < -1:
        TurnValue = -1
    elif -1 <= Rstick <= -.2:
        TurnValue = -(Rstick**2)
    elif .2 <= Rstick <= 1:
        TurnValue = Rstick**2
    elif Rstick > 1:
        TurnValue = 1
    else: TurnValue = 0
    
    #convert to radius
    TurnRadius = -MaxTurnRadius * abs(TurnValue) + MaxTurnRadius

    #calc the drive velocities; outputs are normalized
    LongArc = 2*(TurnRadius+BotWidth/2)*pi
    MidArc =  2*(TurnRadius)*pi
    ShortArc = 2*(TurnRadius - BotWidth/2)*pi
    
    MaxTanV = MidArc/LongArc #maximum speed of turning center
    if MaxTanV >= Lstick:
        TanVelocity = Lstick
    else: TanVelocity = MaxTanV

    if TurnValue < 0:
        RightVel = (LongArc*TanVelocity)/MidArc
        LeftVel = (ShortArc*TanVelocity)/MidArc
    elif TurnValue > 0:
        LeftVel = (LongArc*TanVelocity)/MidArc
        RightVel = (ShortArc*TanVelocity)/MidArc
    else: RightVel,LeftVel = 0,0
    
    return LeftVel,RightVel

def Intake():
    pass
def Outtake():
    pass 

def clamp():
    pass
def release_clamp():
    pass

def MogoClamp():
    if Sensors.hasgoal == True and ClampActive == False :
        release_clamp()
    
    ClampActive = not ClampActive
    if ClampActive == False:
        release_clamp()
    else:
        clamp()



################################
#           THREADS            #
################################
SensorThread = threading.Thread(target=Sensors.update_Variables)
InputThread = threading.Thread(target=Sensors.update_Inputs)
#TrackingThread = threading.Thread(target=AutoDriver.update)
#Main thread for managing Waypoints

################################
#         CONTROL LOOP         #
################################