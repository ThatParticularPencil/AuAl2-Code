#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code save
MAX_DV = 96
MAX_TV = 80
TURN_SENS = .3
alpha3 = .98
controller_1 = Controller(PRIMARY)
intake = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
Mogo = DigitalOut(brain.three_wire_port.a)
doinker = DigitalOut(brain.three_wire_port.b)
Wall = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
L3 = Motor(Ports.PORT18, GearSetting.RATIO_6_1, True)
R3 = Motor(Ports.PORT8, GearSetting.RATIO_6_1, False)
left_motor_a = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
left_motor_b = Motor(Ports.PORT19, GearSetting.RATIO_6_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b,L3)
right_motor_a = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False)
right_motor_b = Motor(Ports.PORT9, GearSetting.RATIO_6_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b,R3)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 299.24, 295, 40, MM, 0.6)


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
wait(100, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

def low_pass_filter(vprev, value, alpha):
    return alpha*vprev +(1-alpha)*value


# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    axis_3 = 0 
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        global alpha3,TURN_SENS
        #accel limiter by average:
        axis_3 = low_pass_filter(axis_3, controller_1.axis3.position(), alpha3)

        if remote_control_code_enabled:

            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            DL = axis_3+(controller_1.axis1.position()*TURN_SENS)
            DR = axis_3-(controller_1.axis1.position()*TURN_SENS)

            drivetrain_left_side_speed = max(min(DL, MAX_DV),-MAX_DV)
            drivetrain_right_side_speed = max(min(DR, MAX_DV),-MAX_DV)
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(5, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

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
wait(5,MSEC)

################################
#          Variables           #
################################

Team = "RED" #either "RED" or "BlUE"
TimeAlertTriggered = False
TrackerRadius = 13.63/2

intake.set_velocity(90, PERCENT)
intake.set_stopping(HOLD)

IsDoinked = False
WallPosition = 0
hold_threshold = .3
Wall.set_stopping(HOLD)

'''
Kp = 1.4 or .4
Ki = 0.4 or .03
Kd = 0.3 or .2
''' 

################################
#       CLASS DEFINITIONS      #
################################
Heading = 0

class Sensor_Manager:
    global Heading
    def __init__(self):
        #self.IsUpdated = False
        self.IMU1 =0
        self.IMU2 = 0
        self.TrackerF = 0
        self.TrackerF2 = 0
        #self.TrackerS = 0
        #self.prevIMU1 = self.IMU1
        #self.prevIMU2 = self.IMU2
        self.prevTrackerF = self.TrackerF
        #self.prevTrackerS = self.TrackerS
        
    #def get_IMU1(self):
        #return imu1.heading(DEGREES)
    #def get_IMU2(self):
        #return imu2.heading(DEGREES)
    def get_TrackerF(self):
        return L3.position(DEGREES)* .0165
    def get_TrackerF2(self):
        return R3.position(DEGREES)* .0165
    def get_TrackerS(self):
        pass
    def get_Heading(self,wWeight=1):
        global Heading
        num = degrees((self.TrackerF - self.TrackerF2)/(2*TrackerRadius))
        Heading = num
        return num

    def update_Secondary(self):
        #some loops
        pass
    def update(self):
        Heading = self.get_Heading()
        #self.prevIMU1 = self.IMU1
        #self.prevIMU2 = self.IMU2
        self.prevTrackerF = self.TrackerF
        #self.prevTrackerS = self.TrackerS
        #self.IMU1 = self.get_IMU1()
        #self.IMU2 = self.get_IMU2()
        self.TrackerF = self.get_TrackerF()
        self.TrackerF2 = self.get_TrackerF2()
        #self.TrackerS = self.get_TrackerS()
        #self.IsUpdated = True

class PID_Controller:
    def __init__(self, Kp, Ki, Kd, target, alpha=0.2, umax=100, umin=.5):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target = target
        self.alpha = alpha  # Filtering coefficient for derivative term
        self.umax = umax # integrator clamp max
        self.umin = umin # integrator clamp min
        
        self.previous_error = 0     #all these are updated but start at zero
        self.previous_derivative = 0
        self.integral = 0
        self.filtered_derivative = 0
        self.prev_update = time.time()
        
    def update(self, Progress, dt):
        error = self.target - Progress
        print(error,"error")
        
        # Proportional term
        P = self.Kp * error
        # Derivative term (unfiltered)
        if dt != 0:
            D_unfiltered = (error - self.previous_error) / dt
        else: 
            D_unfiltered = 1
        
        # Apply low-pass filter to the derivative term
        self.filtered_derivative =low_pass_filter(self.previous_derivative, D_unfiltered, self.alpha)
        p_d = self.filtered_derivative
        #self.filtered_derivative = self.alpha * D_unfiltered + (1 - self.alpha) * self.filtered_derivative
        D = self.Kd * self.filtered_derivative
        
        
        # Clamped Integral term
        dint_unclamped = error * dt
        I_unclamped = self.Ki * dint_unclamped
        if self.umin < abs(P + I_unclamped + D) < self.umax:
            self.integral += dint_unclamped
            I = I_unclamped
        else: I = I_unclamped   

        # Control output
        U = P + I + D
        if U > 40:
            U = 40
        elif U<-40:
            U = -40
        
        # Update previous 
        self.previous_error = error
        self.previous_derivative = p_d 
        print(U,"U")
        return U

################################
#        FUNCS & INITS         #
################################
ClampActive = False

def SelectAuton():
    global Team
    brain.screen.set_fill_color(Color.RED)
    brain.screen.draw_rectangle(0, 0, 479, 239)
    brain.screen.set_fill_color(Color.BLUE)
    brain.screen.draw_rectangle(240, 0, 479, 239)

    while brain.screen.pressing() == False:
        if brain.screen.pressing():
            break
    
    if brain.screen.x_position() >=240:
        Team = "Blue"
        brain.screen.clear_screen()
        brain.screen.set_font(FontType.MONO60)
        brain.screen.print(Team)
    elif brain.screen.x_position() < 240:
        brain.screen.clear_screen()
        brain.screen.set_fill_color(Color.RED)
        brain.screen.set_font(FontType.MONO60)
        brain.screen.print(Team)
    return Team

def Intake():
    intake.spin(FORWARD)
def Outtake():
    intake.spin(REVERSE) 

def wallstake(pos):
    global WallPosition

    if pos == 0:
        Wall.spin_to_position(0*2.3, DEGREES,wait=False)
        WallPosition = 0
    elif pos == 1:
        Wall.spin_to_position(20*2.3,DEGREES,wait=False)
        WallPosition = 1
    elif pos == 2: 
        Wall.spin_to_position(114*2.3,DEGREES,wait=False)
        WallPosition = 2
    else: 
        if WallPosition == 0:
            Wall.spin_to_position(20*2.3,DEGREES,wait=False)
            WallPosition = 1
        elif WallPosition == 1 or WallPosition == 2:
            intake.spin_for(REVERSE,45,DEGREES)
            while controller_1.buttonY.pressing() == True:
                Wall.spin_to_position(110*2.3, DEGREES,wait=False)
                Wall.set_velocity(30,PERCENT)
                WallPosition = 2
            else:
                Wall.spin_to_position(20*2.3,DEGREES,wait=False)
                Wall.set_velocity(70,PERCENT)
                WallPosition = 1


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

def buzz():
    controller_1.rumble(".")
controller_1.buttonL2.pressed(buzz())

Manager = Sensor_Manager()

def head(dist, P=2, I=0.5, D=0.5, deadzone = .3):
    Control = PID_Controller(P, I, D, dist+Manager.TrackerF)
    while True:
        Manager.update()
        drivetrain.set_drive_velocity(Control.update(Manager.TrackerF, time.time()-Control.prev_update), PERCENT)
        if Control.target -deadzone < Manager.TrackerF < Control.target +deadzone:
            drivetrain.set_drive_velocity(0, PERCENT)
            del Control
            break
def circ(angl, P=.5 , I=.05, D=.3, deadzone = .3):
    global Heading
    if Team == "Blue":
        angl *= -1
    Control = PID_Controller(P, I, D, angl)
    while True:
        Manager.update()
        drivetrain.set_turn_velocity(Control.update(Heading, time.time()-Control.prev_update), PERCENT)
        if Control.target -deadzone < Heading < Control.target + deadzone:
            drivetrain.set_turn_velocity(0, PERCENT)
            del Control
            break

################################
#         CONTROL LOOP         #
################################
Wall.set_velocity(70, PERCENT)
intake.set_velocity(100,PERCENT)

Team = SelectAuton()
def driver_control():
    global alpha3, TURN_SENS
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(0, PERCENT)


    driving = True

    controller_1.buttonRight.pressed(doink)

    print("driving")
    #buttons#
    while True:
        if time.time == 85 and TimeAlertTriggered == False:
            controller_1.rumble("--.")
            controller_1.screen.print("20 SECONDS REMAIN")
            TimeAlertTriggered = True
        #driving#
        if controller_1.buttonL2.pressing():
            alpha3 = .0
            TURN_SENS = 1
        else:
            alpha3 = .98
            TURN_SENS = .65

        #subsystems#

        if controller_1.buttonR1.pressing():
            Intake()
        elif controller_1.buttonR2.pressing():
            Outtake()
        else: intake.stop()

        if controller_1.buttonL1.pressing():
                release_clamp()
        else:
            clamp()

        if controller_1.buttonB.pressing():
            wallstake(0)
        if controller_1.buttonY.pressing() :
            wallstake(None)
        


def autonomous():
    drivetrain.set_drive_velocity(0, PERCENT)
    drivetrain.set_turn_velocity(0, PERCENT)
    
    intake.set_velocity(100,PERCENT)
    
    drivetrain.set_stopping(HOLD)
    drivetrain.drive(FORWARD)
    drivetrain.turn(RIGHT)


    ############################################################################

    #Drive back 35 inches to clamp stake
    head(-28, 1.6, .4, .3)

    clamp()
    wait(.5,SECONDS)
    intake.spin(FORWARD)
    wait(.2,SECONDS)

    #turn towards first stack
    circ(135,.47)
    #Drive 25 and intake
    head(21, 1.8, .4, .3, .5)
    head(-2,1.8,.4,.3,.5)
    
    #turn to second stack
    circ(50)
    #ring2
    head(13, 2, .4, .3)
    #ring3
    circ(163)
    head(10)

    head(-10)
    circ(250,.6,0,.5)
    head(25)



    '''#doink stack
    head(-29)
    circ(272,.6)
    intake.spin_for(REVERSE, 50,DEGREES,wait=False)
    head(27,2)
    #doinker
    doink()
    wait(.5,SECONDS)
    circ(150,.5,.2,.05)
    release_doink()
    wait(.4,SECONDS)
    circ(245)
    intake.spin(FORWARD)
    head(15,1.6,.3)'''

    #go to tower
    wallstake(2)
    

competition = Competition(driver_control, autonomous)


################################
#            _SAVES            #
################################


'''#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code save
MAX_DV = 96
MAX_TV = 80
TURN_SENS = .3
alpha3 = .98
controller_1 = Controller(PRIMARY)
intake = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
Mogo = DigitalOut(brain.three_wire_port.a)
doinker = DigitalOut(brain.three_wire_port.b)
Wall = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
L3 = Motor(Ports.PORT18, GearSetting.RATIO_6_1, True)
R3 = Motor(Ports.PORT8, GearSetting.RATIO_6_1, False)
left_motor_a = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
left_motor_b = Motor(Ports.PORT19, GearSetting.RATIO_6_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b,L3)
right_motor_a = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False)
right_motor_b = Motor(Ports.PORT9, GearSetting.RATIO_6_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b,R3)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 299.24, 295, 40, MM, 0.6)


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
wait(100, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

def low_pass_filter(vprev, value, alpha):
    return alpha*vprev +(1-alpha)*value


# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    axis_3 = 0 
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        global alpha3,TURN_SENS
        #accel limiter by average:
        axis_3 = low_pass_filter(axis_3, controller_1.axis3.position(), alpha3)

        if remote_control_code_enabled:

            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            DL = axis_3+(controller_1.axis1.position()*TURN_SENS)
            DR = axis_3-(controller_1.axis1.position()*TURN_SENS)

            drivetrain_left_side_speed = max(min(DL, MAX_DV),-MAX_DV)
            drivetrain_right_side_speed = max(min(DR, MAX_DV),-MAX_DV)
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(5, MSEC)

'''
