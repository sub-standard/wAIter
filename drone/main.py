import sys
import signal
import time
from drone import Drone
from scanner import Scanner


def signal_handler(sig, frame):
    drone.stop()
    drone.land()
    sys.exit(0)


def withinRange(value):
    tolerance = 10
    return value < (500 + tolerance) and value > (500 - tolerance)


signal.signal(signal.SIGINT, signal_handler)
manufacturer = sys.argv[1]
scanner = Scanner()

print "Initalising wAIter Drone"
drone = Drone()
print "Initialisation Complete"
print ""
print "Status check commencing"
print "Battery Percentage       : " + drone.getBatteryPercent() + "%"
print "Battery Status           : " + drone.getBatteryStatus()
print "Motor Status             : " + drone.getMotorStatus()
print "Ultrasonic Sensor Status : " + drone.getUltrasonicSensorStatus()
print "Status check complete"

rssi = None
while rssi == None:
    rssi = scanner.gatherAverageRSSI(manufacturer, 7)
print "Located next destination"

print "Taking off"
drone.takeoff()

print "Moving towards target"
drone.moveForward(0.05)

markers = None
while markers == None:
    markers = drone.getTaggedMarkers()
drone.stop()
print "Located LZ"

print "Zeroing in"
while not withinRange(markers[0].x) and not withinRange(markers[0].y):
    if markers[0].x < 500:
        drone.moveForward(0.05)
    else:
        drone.moveBack(0.05)

    if markers[0].y < 500:
        drone.moveLeft(0.05)
    else:
        drone.moveRight(0.05)

    time.sleep(markers[0].distance / 1000)
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
