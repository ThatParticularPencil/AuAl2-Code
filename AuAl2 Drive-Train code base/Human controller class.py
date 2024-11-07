#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
L1 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
L2 = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False)
L3 = Motor(Ports.PORT9, GearSetting.RATIO_6_1, True)
R1 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
R2 = Motor(Ports.PORT20, GearSetting.RATIO_6_1, False)
R3 = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)
intake = Motor(Ports.PORT21, GearSetting.RATIO_18_1, False)
Mogo = DigitalOut(brain.three_wire_port.a)
doinker = DigitalOut(brain.three_wire_port.b)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *
#imports
import time
#import threading
from math import sin,cos,tan,asin,acos,atan,pi,degrees,radians,sqrt

# Begin project code
wait(30,MSEC)



################################
#          Variables           #
################################
StickDeadzone = .01
StickCurveShape = "linear"

TrackingDiameter = 2.75
WheelDiameter = 3.75

Acceltime = .7
VelConst = 1/(Acceltime**2)
MaxTurnRadius = 10
#normalize turns from 1.25',

BotWidth = 1.05

intake.set_velocity(80, PERCENT)
intake.set_stopping(BRAKE)

IsDoinked = False


################################
#       CLASS DEFINITIONS      #
################################
class Sensor_Manager:
    def __init__(self):
        self.IsUpdated = False
        #self.time = time.time
        #self.prevtime = time.time
        #self.TrackerF = self.get_TrackerF
        self.Lstick = 0
        self.Rstick = 0
        #self.Velocity = self.get_Velocity
        #self.prevTrackerF = self.TrackerF
        #self.prevLstick = self.Lstick
        #self.prevRstick = self.Rstick
        #self.prevVelocity = self.Velocity
        
    def get_TrackerF(self):
        pass

    def get_Lstick(self):
        stick = controller_1.axis3.position()/100 #v5 controller method
        '''#Sensitivity Curve
        if -1 <= stick <= -StickDeadzone:
            curvedstick = -(stick**2)
        elif StickDeadzone <= stick <= 1:
            curvedstick = stick**2
        else: curvedstick = 0
        return curvedstick'''
        return stick

    def get_Rstick(self):
        stick = controller_1.axis1.position()/100 #v5 controller method
        ''' #Sensitivity Curve
        if -1 <= stick <= -StickDeadzone:
            curvedstick = -(stick**2)
        elif StickDeadzone <= stick <= 1:
            curvedstick = stick**2
        else: curvedstick = 0
        return curvedstick'''
        return stick

    '''def get_Velocity(self):
        pass'''

    def update_Inputs(self):
        self.Rstick = self.get_Rstick()
        self.Lstick = self.get_Lstick()
        self.IsUpdated = True
    
    def update_Variables(self):
        #self.prevtime = self.time
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

def SelectAuton():
    controller_1.screen.print("AUTON /n Red <- use dpad -> Blue")




def Drive(left,right):
    L1.set_stopping(BRAKE)
    L2.set_stopping(BRAKE)
    L3.set_stopping(BRAKE)
    R1.set_stopping(BRAKE)
    R2.set_stopping(BRAKE)
    R3.set_stopping(BRAKE)

    L1.set_velocity(left*100, PERCENT)
    L2.set_velocity(left*100, PERCENT)
    L3.set_velocity(left*100, PERCENT)
    R1.set_velocity(right*-100, PERCENT)
    R2.set_velocity(right*-100, PERCENT)
    R3.set_velocity(right*-100, PERCENT)


def low_pass_filter(vprev, value, alpha):
    return alpha*vprev +(1-alpha)*value

def CurvatureDrive(Lstick, Rstick):
    #Assuming Normalized RstickX Values to -1 < x < 1

    #Sensitivity Curve is already done
    print("TV", Rstick)
    if Rstick == 0:
         LeftVel,RightVel = Lstick,Lstick
         return LeftVel,RightVel

    #convert to radius
    TurnRadius = -MaxTurnRadius * abs(Rstick) + MaxTurnRadius
    print("TurnRadius",TurnRadius)
    if TurnRadius == 0:
        TurnRadius = .001

    #calc the drive lengths then velocities; outputs are normalized
    LongArc = 2*(TurnRadius+BotWidth/2)*pi
    MidArc =  2*(TurnRadius)*pi
    ShortArc = 2*(TurnRadius - BotWidth/2)*pi
    
    #so it dont ask for speeds above 100
    TanVelocity = Lstick
    Ltom = LongArc/MidArc
    Stom = ShortArc/MidArc
    if Ltom*abs(TanVelocity) > 1:
        if TanVelocity >0:
            TanVelocity = 1/Ltom 
        else:
            TanVelocity = -1/Ltom
        if TanVelocity > 1:
            TanVelocity = 1
        elif TanVelocity <-1:
            TanVelocity = -1 #adds a buffer in case of crappy code

    #Algebra so the Arc:MidArc = vel:TanVel
    if Rstick < 0:
        RightVel = Ltom * TanVelocity
        LeftVel = Stom * TanVelocity 
    elif Rstick > 0:
        LeftVel = Ltom * TanVelocity
        RightVel = Stom * TanVelocity

        if Lstick == 0:
            LeftVel,RightVel = Rstick/5,-(Rstick/5)
    

    return LeftVel,RightVel


    #Buttons#
def Intake():
    intake.spin(FORWARD)
    
def Outtake():
    intake.spin(REVERSE) 


def clamp():
    Mogo.set(True)
def release_clamp():
    Mogo.set(False)

def doink():
    global IsDoinked
    IsDoinked = not IsDoinked
    doinker.set(IsDoinked)
def release_doink():
    doinker.set(False)


################################
#           THREADS            #
################################
#SensorThread = threading.Thread(target=Sensors.update_Variables)
#InputThread = threading.Thread(target=Sensors.update_Inputs)
#TrackingThread = threading.Thread(target=AutoDriver.update)
#Main thread for managing Waypoints

################################
#         CONTROL LOOP         #
################################
driving = True
Sensors = Sensor_Manager()
Sensors.update_Inputs()
#InputThread.start
Drive(0,0)
L1.spin(FORWARD)
L2.spin(FORWARD)
L3.spin(FORWARD)
R1.spin(FORWARD)
R2.spin(FORWARD)
R3.spin(FORWARD)

while driving == True:
    #buttons#
    controller_1.buttonL1.pressed(clamp)
    controller_1.buttonL2.pressed(release_clamp)
    controller_1.buttonUp.pressed(doink)
    
    #driving#
    Sensors.update_Inputs()
    left,right = CurvatureDrive(Sensors.Lstick, Sensors.Rstick)
    Drive(left,right)

    #subsystems#
    if controller_1.buttonR1.pressing():
        Intake
    elif controller_1.buttonR2.pressing():
        Outtake

        
