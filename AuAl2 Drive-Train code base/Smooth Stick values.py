StickDeadzone = .2
StickCurveShape = "parabolic"

def Smooth_Stick(stick, shape): #input value [-1,1] out value [0,1]
    #Sensitivity Curve
    if -1 <= stick <= -StickDeadzone:
        curvedstick = -(stick**2)
    elif StickDeadzone <= stick <= 1:
        curvedstick = stick**2
    else: curvedstick = 0

    return curvedstick
    
    
    
    
    
    
    
    