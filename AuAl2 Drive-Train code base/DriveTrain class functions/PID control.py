
import time
import math


################################
#          Variables           #
################################

#CONSTANTS
Kp = 1.0
Ki = 0.1
Kd = 0.01

#Function clamps
#belongs to class: umin = 3
#belongs to class: umax = 100

#Kd filter
alpha = .3

tick = 50

#DATA STUFF
target_position = 30
dataLog = []
# belongs to PID class: error_previous = 0
# belongs to PID class: integral = 0
previous_time = time.time()

   
################################
#         SMALL FUNCS          #
################################
def get_current_position():
    pass # probably use a smooth list for now

def get_elapsed_time(previous_time):
    current_time = time.time()
    dt = current_time - previous_time
    return dt, current_time

def low_pass_filter(self, value, vprev, alpha):
    return alpha*value +(1-alpha)*vprev


################################
#       CLASS DEFINITION       #
################################

class PIDController:
    def __init__(self, Kp, Ki, Kd, target, alpha=0.1, umax=100, umin=2):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target = target
        self.alpha = alpha  # Filtering coefficient for derivative term
        self.umax = umax # integrator clamp max
        self.umin = umin # integrator clamp min
        
        self.previous_error = 0
        self.previous_derivative = 0
        self.integral = 0
        self.filtered_derivative = 0
        
    def update(self, Progress, dt):
        error = self.target - Progress
        # Proportional term
        P = self.Kp * error
        # Derivative term (unfiltered)
        D_unfiltered = (error - self.previous_error) / dt
        
        # Apply low-pass filter to the derivative term
        self.filtered_derivative = D_unfiltered.low_pass_filter(self.previous_derivative, self.alpha)
        p_d = self.filtered_derivative
        #self.filtered_derivative = self.alpha * D_unfiltered + (1 - self.alpha) * self.filtered_derivative
        D = self.Kd * self.filtered_derivative
        
        
        # Clamped Integral term
        dint_unclamped = error * dt
        I_unclamped = self.Ki * dint_unclamped
        if P + I_unclamped + D < self.umax and P + I_unclamped + D > self.umin:
            self.integral += dint_unclamped
            I = I_unclamped
        #needs else?
        
        # Control output
        U = P + I + D
        
        # Update previous 
        self.previous_error = error
        self.previous_derivative = p_d 
        return U



################################
#         CONTROL LOOP         #
################################
# Initialize PID controller
pid = PIDController(Kp, Ki, Kd, target_position, alpha=0.1)

# Control loop
previous_time = time.time()

while True:
    current_position = get_current_position()
    dt, previous_time = get_elapsed_time(previous_time)
    
    control_output = pid.update(current_position, dt)
    
    # Apply control output to the motor
    
    # Exit condition (for example, target angle reached or a specific time passed)
    if abs(current_position - target_position) < 1:  # tolerance
        #stop motor
        break
    
    time.sleep(0.01)  # Small delay to prevent too frequent updates



