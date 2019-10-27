import sys
from drone import Drone, TaggedMarkers, Marker
from scanner import Scanner


manufacturer = sys.argv[1]

print "scanning for device with manufacture data |" + manufacturer + "|"

scanner = Scanner()
rssi = scanner.gatherAverageRSSI(manufacturer, 7, scanner)

# define whether to rotate clockwise or anticlockwise
rotate_dir = 1

drone = Drone()
drone.takeoff()

# stop the method because we're close enough
while rssi < -40:
    mv_distance = abs(rssi) * 0.02
    drone.moveForward(mv_distance)
    last_rssi = rssi
    rssi = scanner.gatherAverageRSSI(manufacturer, 7)
    if last_rssi > rssi:
        drone.rotate(90)
        drone.rotate(90)
        drone.moveForward(mv_distance / 2)
        drone.rotate(rotate_dir * 90)
        last_rssi = rssi
        rssi = scanner.gatherAverageRSSI(manufacturer, 7)
        mv_distance = abs(rssi) * 0.02
        drone.moveForward(mv_distance)
        last_rssi = rssi
        rssi = scanner.gatherAverageRSSI(manufacturer, 7)
        if last_rssi > rssi:
            rotate_dir = rotate_dir * -1
            drone.rotate(90)
            drone.rotate(90)
            drone.moveForward(mv_distance * 2)
            last_rssi = rssi
            rssi = scanner.gatherAverageRSSI(manufacturer, 7)

drone.land()
