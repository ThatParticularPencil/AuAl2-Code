from math import pi
BotWidth = 1.06 #dist from wheel to wheel
MaxTurnRadius = 5

def Plan_Arc(Lstick, Rstick):
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
            LeftVel,RightVel = Rstick/2,-Rstick/2
    

    return LeftVel,RightVel

print(Plan_Arc(.1,1))

def iscorrect(L,R):
    pass