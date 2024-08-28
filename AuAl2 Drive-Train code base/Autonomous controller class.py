#imports
import time
import threading
from math import sin,cos,tan,asin,acos,atan,pi,degrees,radians,sqrt


################################
#          Variables           #
################################
StartPos = (0,0)
Pos = StartPos #global ,field oriented position vector
Heading = 0 #gloabl ,field oriented heading. starts at zero

TrackingDiameter = 2.75 #design DB -v
WheelDiameter = 3.75
BotDiameter = 8


MaxVelocity = 1

#Waypoints
WAYPOINTS = { #count, target, turn or drive, pid consts, 
    None
}
Waypoint = 0 #the current point that the bot is heading towards

HALT_AUTON = False


################################
#       CLASS DEFINITIONS      #
################################
class Sensor_Manager:
    def __init__(self):
        self.IsUpdated = False
        self.IMU1 = self.get_IMU1
        self.IMU2 = self.get_IMU2
        self.TrackerF = self.get_TrackerF
        self.TrackerS = self.get_TrackerS
        self.prevIMU1 = self.IMU1
        self.prevIMU2 = self.IMU2
        self.prevTrackerF = self.TrackerF
        self.prevTrackerS = self.TrackerS
        
    def get_IMU1(self):
        pass
    def get_IMU2(self):
        pass
    def get_TrackerF(self):
        pass
    def get_TrackerS(self):
        pass
    def get_Heading(self,wWeight=1):
        # needs extra math probably to convert to an actual heading
        # must be radians
        global Heading
        delta1 = abs(self.IMU1 - self.prevIMU1) #change in sensor reading
        delta2 = abs(self.IMU2 - self.prevIMU2)
        if delta1 == 0 or delta2 ==0:
            return .5*(self.IMU1+self.IMU2)

        recipAlpha = 1/(delta1/delta2 +1) #normalized to 0-1 with a reciprocal function
        #FilteredIMU = recipAlpha*self.IMU1 + (1-recipAlpha)*self.IMU2 #low-pass filter
        FilteredIMU = low_pass_filter(self.IMU1, self.IMU2, recipAlpha)
        Heading = FilteredIMU
        return FilteredIMU

    def Linear_Odom(self):
        # Must be radians
        # forward /n turn
        global Pos
        global Heading
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

    def update_Secondary(self):
        #some loops
        pass
    
    def update(self):
        self.prevIMU1 = self.IMU1
        self.prevIMU2 = self.IMU2
        self.prevTrackerF = self.TrackerF
        self.prevTrackerS = self.TrackerS
        self.IMU1 = self.get_IMU1
        self.IMU2 = self.get_IMU2
        self.TrackerF = self.get_TrackerF
        self.TrackerS = self.get_TrackerS
        self.IsUpdated = True

class PIDController:
    def __init__(self, Kp, Ki, Kd, target, alpha=0.2, umax=100, umin=2):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target = target
        self.alpha = alpha  # Filtering coefficient for derivative term
        self.umax = umax # integrator clamp max
        self.umin = umin # integrator clamp min
        
    #   !These will belong to the Sensor Manager
        self.previous_error = 0     #all these are updated but start at zero
        self.previous_derivative = 0
        self.integral = 0
        self.filtered_derivative = 0
        self.prev_update = time.time()
        
    def update(self, Progress, dt):
        error = self.target - Progress
        
        # Proportional term
        P = self.Kp * error
        # Derivative term (unfiltered)
        D_unfiltered = (error - self.previous_error) / dt
        
        # Apply low-pass filter to the derivative term
        self.filtered_derivative =low_pass_filter(self.previous_derivative, D_unfiltered, self.alpha)
        p_d = self.filtered_derivative
        #self.filtered_derivative = self.alpha * D_unfiltered + (1 - self.alpha) * self.filtered_derivative
        D = self.Kd * self.filtered_derivative
        
        
        # Clamped Integral term
        dint_unclamped = error * dt
        I_unclamped = self.Ki * dint_unclamped
        if P + I_unclamped + D < self.umax and P + I_unclamped + D > self.umin:
            self.integral += dint_unclamped
            I = I_unclamped
        else: I = I_unclamped   

        # Control output
        U = P + I + D
        
        # Update previous 
        self.previous_error = error
        self.previous_derivative = p_d 
        return U


################################
#        FUNCS & INITS         #
################################
def low_pass_filter(vprev, value, alpha):
    return alpha*vprev +(1-alpha)*value

Sensors = Sensor_Manager

################################
#           THREADS            #
################################
SensorThread = threading.Thread(target=Sensors.update)
#TrackingThread = threading.Thread(target=AutoDriver.update)
#Main thread for managing Waypoints

################################
#         CONTROL LOOP         #
################################