from math import sqrt
Acceltime = .7
VelConst = 1/(Acceltime**2)
MaxVelocity = 1

#needs to be in the driver object
def Smooth_Stick(shape): #input value [-1,1] out value [0,1]
    #Sensitivity Curve
    if -1 <= stick <= -StickDeadzone:
        curvedstick = -(stick**2)
    elif StickDeadzone <= stick <= 1:
        curvedstick = stick**2
    else: curvedstick = 0

    return curvedstick


#needs to be in the driver object
def JL_Accel(self): #smoothed vLstick + globals
    #incorporate step size
    if self.curvedL != 0:
        if self.velocity >=0: 
            nextvalue = (sqrt(self.velocity)+1)**2
        else:
            nextvalue = -(sqrt(abs(self.velocity))+1)**2
    return nextvalue