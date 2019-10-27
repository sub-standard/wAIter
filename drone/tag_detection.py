#########
# firstTagDetection.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to detect tag/marker of a Parrot AR.Drone 2.0 using the PS-Drone-API.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

##### Suggested clean drone startup sequence #####
import time
import sys
# Import PS-Drone
import ps_drone

# Start using drone
drone = ps_drone.Drone()
# Connects to drone and starts subprocesses
drone.startup()

# Sets the drone's status to good (LEDs turn green when red)
drone.reset()
while (drone.getBattery()[0] == - 1):
    time.sleep(0.1)        # Wait until the drone has done its reset
# Gives a battery-status
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])
# Just give me 15 basic dataset per second (is default anyway)
drone.useDemoMode(True)
# Packets, which shall be decoded
drone.getNDpackage(["demo", "vision_detect"])
# Give it some time to awake fully after reset
time.sleep(0.5)

##### Mainprogram begin #####
# Setting up detection...
# Shell-Tag=1, Roundel=2, Black Roundel=4, Stripe=8, Cap=16, Shell-Tag V2=32, Tower Side=64, Oriented Roundel=128
# Enable universal detection
drone.setConfig("detect:detect_type", "3")
# Detect "Oriented Roundel" with front-camera
# drone.setConfig("detect:detections_select_h", "128")
# No detection with ground cam
drone.setConfig("detect:detections_select_v", "128")
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:
    time.sleep(0.01)        # Wait until configuration has been set

# Get detections
stop = False
while not stop:
    NDC = drone.NavDataCount
    while NDC == drone.NavDataCount:
        time.sleep(0.01)
    if drone.getKey():
        stop = True
    # Loop ends when key was pressed
    # Number of found tags
    tagNum = drone.NavData["vision_detect"][0]
    # Horizontal position(s)
    tagX = drone.NavData["vision_detect"][2]
    # Vertical position(s)
    tagY = drone.NavData["vision_detect"][3]
    tagZ = drone.NavData["vision_detect"][6]                 # Distance(s)
    tagRot = drone.NavData["vision_detect"][7]                 # Orientation(s)

    # Show detections
    if tagNum:
        for i in range(0, tagNum):
            print "Tag no "+str(i)+" : X= "+str(tagX[i])+"  Y= "+str(
                tagY[i])+"  Dist= "+str(tagZ[i])+"  Orientation= "+str(tagRot[i])
