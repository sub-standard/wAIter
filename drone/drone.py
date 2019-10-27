import ps_drone
import time
from math import sqrt


class Drone():

    # ~~~~ INIT ~~~~
    def __init__(self):
        self.drone = ps_drone.Drone()
        self.drone.startup()
        self.drone.reset()
        while (self.drone.getBattery()[0] == -1):
            time.sleep(0.1)
        self.drone.useDemoMode(True)
        self.drone.getNDpackage(["demo", "altitude", "vision_detect", "time"])
        self.configure()

    def configure(self):
        CDC = self.drone.ConfigDataCount
        self.drone.setConfig("general:ardrone_name", "wAIter")
        self.drone.setConfig("detect:detect_type", "3")
        self.drone.setConfig("detect:detections_select_v", "128")
        while CDC == self.drone.ConfigDataCount:
            time.sleep(0.0001)

    # ~~~~ STATUS ~~~~
    def getDroneTime(self):
        return self.drone.NavDataTimeStamp

    def getBatteryPercent(self):
        return self.drone.getBattery()[0]

    def getBatteryStatus(self):
        return self.drone.getBattery()[1]

    def getMotorStatus(self):
        return self.drone.State[12]

    def getUltrasonicSensorStatus(self):
        return self.drone.State[21]

    # ~~~~ NAVIGATIONAL DATA ~~~~
    def getSpeed(self):
        return sqrt(self.getSpeedX()**2 + self.getSpeedY()**2 + self.getSpeedZ()**2)

    def getSpeedX(self):
        return self.drone.NavData["demo"][4][0]

    def getSpeedY(self):
        return self.drone.NavData["demo"][4][1]

    def getSpeedZ(self):
        return self.drone.NavData["demo"][4][2]

    def getPitch(self):
        self.waitForNavData()
        return self.drone.NavData["demo"][2][0]

    def getRoll(self):
        self.waitForNavData()
        return self.drone.NavData["demo"][2][1]

    def getYaw(self):
        self.waitForNavData()
        return self.drone.NavData["demo"][2][2]

    def getAltitude(self):
        self.waitForNavData()
        return self.drone.NavData["altitude"][3]

    def getTaggedMarkers(self):
        self.waitForNavData()
        markers = []
        visionDetect = self.drone.NavData["vision_detect"]
        for i in range(visionDetect[0]):
            markers[i] = Marker(
                visionDetect[2][i],
                visionDetect[3][i],
                visionDetect[6][i],
                visionDetect[7][i]
            )
        return markers

    # ~~~~ MOVEMENT COMMANDS ~~~~
    def takeoff(self):
        self.drone.takeoff()

    def land(self):
        self.drone.land()

    def moveForward(self, speed=None):
        self.drone.moveForward(speed)

    def moveLeft(self, speed=None):
        self.drone.moveLeft(speed)

    def moveRight(self, speed=None):
        self.drone.moveRight(speed)

    def moveBack(self, speed=None):
        self.drone.moveBackward(speed)

    def moveForwardDistance(self, distance):
        self.drone.moveForward()
        self.waitForDistance(distance)
        self.stop()

    def moveLeftDistance(self, distance):
        self.drone.moveLeft()
        self.waitForDistance(distance)
        self.stop()

    def moveRightDistance(self, distance):
        self.drone.moveRight()
        self.waitForDistance(distance)
        self.stop()

    def moveBackDistance(self, distance):
        self.drone.moveBackward()
        self.waitForDistance(distance)
        self.stop()

    def rotate(self, angle):
        self.drone.turnAngle(angle, 0.0)

    def driftRight(self):
        self.drone.move(0.2, 0, 0, -0.2)

    def driftLeft(self):
        self.drone.move(-0.2, 0, 0, 0.2)

    def stop(self):
        self.drone.stop()

    # ~~~~ PRIVATE FUNCTIONS ~~~~~
    def waitForNavData(self):
        NDC = self.drone.NavDataCount
        while self.drone.NavData == NDC:
            time.sleep(0.01)

    def waitForDistance(self, distance):
        n = 1
        avgSpeed = 0
        currentDistance = 0
        droneStartTime = self.getDroneTime()
        while currentDistance < distance:
            avgSpeed = avgSpeed + (self.getSpeed() - avgSpeed) / n
            n += 1
            time.sleep(0.1)
            droneCurrentTime = self.getDroneTime()
            currentDistance = avgSpeed * (droneCurrentTime - droneStartTime)


class Marker():
    def __init__(self, x, y, dist, angle):
        self.x = x
        self.y = y
        self.distance = dist
        self.angle = angle
