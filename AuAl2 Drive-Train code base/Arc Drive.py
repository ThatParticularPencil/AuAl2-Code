from math import pi
BotWidth = 1.5 #dist from wheel to turning center
MaxRadius = 10

def Plan_Arc(LstickY, RstickX):
    #Assuming Normalized RstickX Values to -1 < x < 1

    #Sensitivity Curve
    if RstickX < -1:
        TurnValue = -1
    elif -1 <= RstickX <= -.2:
        TurnValue = -(RstickX**2)
    elif .2 <= RstickX <= 1:
        TurnValue = RstickX**2
    elif RstickX > 1:
        TurnValue = 1
    else: TurnValue = 0
    
    #convert to radius
    TurnRadius = -MaxRadius * abs(TurnValue) + MaxRadius

    #calc the drive velocities; outputs are normalized
    LongArc = 2*(TurnRadius+BotWidth/2)*pi
    MidArc =  2*(TurnRadius)*pi
    ShortArc = 2*(TurnRadius - BotWidth/2)*pi
    
    MaxTanV = MidArc/LongArc #maximum speed of turning center
    if MaxTanV >= LstickY:
        TanVelocity = LstickY
        print("good value")
    else: TanVelocity = MaxTanV

    if TurnValue < 0:
        RightVel = (LongArc*TanVelocity)/MidArc
        LeftVel = (ShortArc*TanVelocity)/MidArc
    elif TurnValue > 0:
        LeftVel = (LongArc*TanVelocity)/MidArc
        RightVel = (ShortArc*TanVelocity)/MidArc
    else: RightVel,LeftVel = 0,0
    
    return LeftVel,RightVel


