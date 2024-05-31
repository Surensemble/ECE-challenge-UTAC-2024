#######---------library and constant -------#############
from vehicle import Driver
from controller import Lidar
import numpy as np
import time
import matplotlib.pyplot as plt

DISTANCE = 32
SPEED =50
KP = 3



##########-------variable, function and init--------###########
speed = 0
angle = 0

driver = Driver()
driver.setCruisingSpeed(speed)
driver.setSteeringAngle(angle)

basicTimeStep = int(driver.getBasicTimeStep())
sensorTimeStep = 4 * basicTimeStep

#Lidar
lidar = Lidar("Sick LMS 291")
lidar.enable(sensorTimeStep)
lidar.enablePointCloud() 
 
timestep=0
d=0
T=[]
V=[]                         #array for save measure speed variation
V_command=[]                 #array for save command speed variation 
interVehicular_distance=[]   #array for save intervehicular distance 
temps=[]                     #array for time axis

error=0 

def secure_distance(vitesse):
    ten= vitesse//10
    secure= ten*3*2
    return secure

def brake_distance(vitesse):
    return secure_distance(vitesse)/2
    
      
############----------------Driving------------------##############
while driver.step() != -1:
    #acquisition des donnees du lidar
    donnees_lidar_brutes = lidar.getRangeImage()
    dm= donnees_lidar_brutes[90]
    
    #data acquisition 
    timestep= driver.getTime()
    current_speed = driver.getCurrentSpeed()
    V.append(current_speed)
    V_command.append(speed)
    interVehicular_distance.append(dm)
    temps.append(timestep)

    #speed control    
    error= DISTANCE - dm
    control= KP*error
    speed =  SPEED - control       
             
    if donnees_lidar_brutes[90]<=brake_distance(current_speed):       
           speed=0
           driver.setBrakeIntensity(1)
           driver.setCruisingSpeed(speed)
    else:
          driver.setBrakeIntensity(0) 
          if speed<0:
              speed=0
              driver.setCruisingSpeed(speed)
          elif speed>130:
              speed=130
              driver.setCruisingSpeed(speed)    
          else:     
              driver.setCruisingSpeed(speed)


    print("distance intervehiculaire",donnees_lidar_brutes[90])
    print("time:",timestep)
    print("speed = ",speed)
        
###########----------------Data extraction------------##################       

    if timestep >= 35 and timestep<=35.01:
       plt.plot(temps,V_command, label ="setpoint")
       plt.plot(temps,V,label="measurement")   
       plt.suptitle("speed variation of blue vehicle") 
       plt.xlabel("time (sec)")
       plt.ylabel("speed (km/h)")
       plt.grid(1)
       plt.legend()
       plt.show()   