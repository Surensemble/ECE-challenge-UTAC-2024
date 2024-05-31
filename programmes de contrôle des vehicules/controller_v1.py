#library 

from vehicle import Driver
import matplotlib.pyplot as plt
from controller import Brake, Supervisor


#vatiables, function and init
driver = Driver()
driver.setCruisingSpeed(0)
driver.setSteeringAngle(0)

T= 500 # max number of iteration before braking
i=0

speed=0
angle = 0
v=[]            #array for save measure speed variation
temps=[]        #array for time axis
v_command=[]    #array for save command speed variation
current=0       #variable for save current speed
sec= 0


#Driving 
while driver.step() != -1:
    i +=1
    timestep = driver.getTime()
    temps.append(timestep)
    current= driver.getCurrentSpeed()
    v.append(current)
    v_command.append(speed)
    
    #driving
    if i< T:            
       speed= 50
       driver.setCruisingSpeed(speed)
       driver.setSteeringAngle(angle)
      
    #sudden braking       
    else:
       speed=0
       driver.setCruisingSpeed(speed)
       driver.setBrakeIntensity(0.8)
       driver.setSteeringAngle(0)
       
       
    # data display
    if timestep >= 34 and timestep<=34.01:
       plt.plot(temps,v_command, label ="setpoint")
       plt.plot(temps,v,label="measurement")   
       plt.suptitle("speed variation of red vehicle") 
       plt.xlabel("time (sec)")
       plt.ylabel("speed (km/h)")
       plt.grid(1)
       plt.legend()
       plt.show()   
    
   
       