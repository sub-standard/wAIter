import sys
import signal
import time
from drone import Drone
# from scanner import Scanner

drone = Drone()


def signal_handler(sig, frame):
    global drone
    if drone:
        drone.stop()
        drone.land()
    sys.exit(0)


def withinRange(value):
    tolerance = 10
    return value < (500 + tolerance) and value > (500 - tolerance)


signal.signal(signal.SIGINT, signal_handler)
# manufacturer = sys.argv[1]
# scanner = Scanner()

print "Initalising wAIter Drone"

print "Initialisation Complete"
print ""
print "Status check commencing"
print "Battery Percentage       : " + str(drone.getBatteryPercent()) + "%"
print "Battery Status           : " + str(drone.getBatteryStatus())
print "Motor Status             : " + str(drone.getMotorStatus())
print "Ultrasonic Sensor Status : " + str(drone.getUltrasonicSensorStatus())
print "Status check complete"

# scanner.sampleRSSI(manufacturer, 1)
print "Located next destination"

print "Taking off"
drone.takeoff()
time.sleep(7.5)
drone.stop()
# drone.moveRight(0.003)

print "Moving towards target"
drone.move(-0.01, 0.08, 0.0, 0.0)

markers = None
start = time.time()
while markers == None:
    markers = drone.getTaggedMarkers()
    end = time.time()
    if end - start > 5:
        drone.stop()
        drone.land()
        exit()

drone.stop()
print "Located LZ"

print "Zeroing in"
while not markers or (not withinRange(markers.x[0]) and not withinRange(markers.y[0])):
    if markers.y[0] < 500:
        drone.moveForward(0.05)
    else:
        drone.moveBack(0.05)

    if markers.x[0] < 500:
        drone.moveLeft(0.1)
    else:
        drone.moveRight(0.1)

    time.sleep(markers.distance[0] / 1000)
    drone.stop()
    markers = drone.getTaggedMarkers()

print "Zeroed in on LZ"
drone.stop()

print "Landing"
drone.land()

print "Mission complete"

# TODO wait until beacon has been deactivated before taking off again

# define whether to rotate clockwise or anticlockwise
# rotate_dir = 1
# stop the method because we're close enough
# while rssi < -40:
#     mv_distance = abs(rssi) * 0.02
#     drone.moveForward(mv_distance)
#     last_rssi = rssi
#     rssi = scanner.gatherAverageRSSI(manufacturer, 7)
#     if last_rssi > rssi:
#         drone.rotate(90)
#         drone.rotate(90)
#         drone.moveForward(mv_distance / 2)
#         drone.rotate(rotate_dir * 90)
#         last_rssi = rssi
#         rssi = scanner.gatherAverageRSSI(manufacturer, 7)
#         mv_distance = abs(rssi) * 0.02
#         drone.moveForward(mv_distance)
#         last_rssi = rssi
#         rssi = scanner.gatherAverageRSSI(manufacturer, 7)
#         if last_rssi > rssi:
#             rotate_dir = rotate_dir * -1
#             drone.rotate(90)
#             drone.rotate(90)
#             drone.moveForward(mv_distance * 2)
#             last_rssi = rssi
#             rssi = scanner.gatherAverageRSSI(manufacturer, 7)
