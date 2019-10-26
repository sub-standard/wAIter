import ps_drone
import time


class Drone():

    # ~~~~ INIT ~~~~
    def __init__(self):
        self.drone = ps_drone.Drone()
        self.drone.startup()
        self.drone.reset()
        while (self.drone.getBattery()[0] == -1):
            time.sleep(0.1)
        self.configure()

    def configure(self):
        CDC = self.drone.ConfigDataCount
        self.drone.setConfig("general:ardrone_name", "wAIter")
        self.drone.setConfig("detect:detect type", "3")
        self.drone.setConfig("detect:detections select v", "128")
        while CDC == self.drone.ConfigDataCount:
            time.sleep(0.0001)

    # ~~~~ STATUS ~~~~
    def getBatteryPercent(self):
        return self.drone.getBattery()[0]

    def getBatteryStatus(self):
        return self.drone.getBattery()[1]

    # ~~~~ NAVIGATIONAL DATA ~~~~
    # ~~~~ MOVEMENT COMMANDS ~~~~
    def takeoff(self):
        self.drone.takeoff()

    def land(self):
        self.drone.land()

    def moveForward(self, distance):
        self.drone.moveForward(5)

    def moveLeft(self, distance):
        self.drone.moveLeft(5)

    def moveRight(self, distance):
        self.drone.moveRight(5)

    def moveBack(self, distance):
        self.drone.moveBackward(5)

    def rotate(self, angle):
        self.drone.turnAngle(angle, 0.0)

    def getTaggedMarkers(self):
    # ~~~~ PRIVATE FUNCTIONS ~~~~~
        NDC = self.drone.NavDataCount
        while self.drone.NavData == NDC:
            time.sleep(0.01)
        return TaggedMarkers(self.drone.NavData["vision_detect"])


class TaggedMarkers():
    def __init__(self, visionDetect):
        self.markers = []
        for i in range(visionDetect[0]):
            self.markers[i] = Marker(
                visionDetect[2][i],
                visionDetect[3][i],
                visionDetect[6][i],
                visionDetect[7][i]
            )


class Marker():
    def __init__(self, x, y, dist, angle):
        self.x = x
        self.y = y
        self.distance = dist
        self.angle = angle
