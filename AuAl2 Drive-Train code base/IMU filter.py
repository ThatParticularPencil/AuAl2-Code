
class IMU_Filter:
    #Variable Low Pass filter or smth, idk I made it up
    #It weights the average heavily toward the IMU that is changing slower
    def __init__(self,wWeight=1):
        self.prevIMU1 = 5
        self.prevIMU2 = 5
        self.IMU1 = self.get_IMU1()
        self.IMU2 = self.get_IMU2()
        self.wWeight = wWeight #How heavy the bias is 
    
    def get_IMU1(self):
        #prefer radians
        pass
    def get_IMU2(self):
        pass

    def get_Heading(self):
        # needs extra math probably to convert to an actual heading
        # must be radians
        delta1 = abs(self.IMU1 - self.prevIMU1) #change in sensor reading
        delta2 = abs(self.IMU2 - self.prevIMU2)
        if delta1 == 0 or delta2 ==0:
            return .5*(self.IMU1+self.IMU2)

        recipAlpha = 1/(delta1/delta2 +1) #normalized to 0-1 with a reciprocal function
        print(recipAlpha)
        FilteredIMU = recipAlpha*self.IMU1 + (1-recipAlpha)*self.IMU2 #low-pass filter
        return FilteredIMU

        
        

testy = IMU_Filter()
print(testy.get_Heading())