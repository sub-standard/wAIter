import bluepy
import sys
from statistics import stdev
from bluepy.btle import Scanner, DefaultDelegate


manufacturer = sys.argv[1]

print "scanning for device with manufacture data |" + manufacturer + "|"

# create a delegate class to receive the BLE broadcast packets


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address

    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (_, desc, value) in dev.getScanData():
            if desc == "Manufacturer" and value == manufacturer:
                print("found one")


def mean(numbers):
    if len(numbers) == 0:
        return None
    return float(sum(numbers)) / max(len(numbers), 1)


def gatherAverageRSSI(manufacturer, n_samples, scanner):
    RSSIs = []

    while len(RSSIs) < n_samples:
        new_devices = scanner.scan(5.0)
        for dev in new_devices:
            for (_, desc, value) in dev.getScanData():
                if desc == "Manufacturer" and value == manufacturer:
                    RSSIs.append(dev.rssi)

    mean_rssi = mean(RSSIs)
    std_dev = stdev(RSSIs)

    cutoff_rssi = []

    lower_cutoff = mean_rssi - std_dev
    upper_cutoff = mean_rssi + std_dev
    for x in RSSIs:
        if not (x < lower_cutoff or x > upper_cutoff):
            cutoff_rssi.append(x)

    return mean(cutoff_rssi)


# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())


def move(distance):
    print "move forward " + str(distance)
    input()
    return


def rotate(angle):
    print "rotate " + str(angle)
    return


rssi = gatherAverageRSSI(manufacturer, 7, scanner)

# define whether to rotate clockwise or anticlockwise
rotate_dir = 1


# stop the method because we're close enough
while rssi < -40:
    mv_distance = abs(rssi) * 0.02
    move(mv_distance)
    last_rssi = rssi
    rssi = gatherAverageRSSI(manufacturer, 7, scanner)
    if last_rssi > rssi:
        rotate(180)
        move(mv_distance / 2)
        rotate(rotate_dir * 90)
        last_rssi = rssi
        rssi = gatherAverageRSSI(manufacturer, 7, scanner)
        mv_distance = abs(rssi) * 0.02
        move(mv_distance)
        last_rssi = rssi
        rssi = gatherAverageRSSI(manufacturer, 7, scanner)
        if last_rssi > rssi:
            rotate_dir = rotate_dir * -1
            rotate(180)
            move(mv_distance * 2)
            last_rssi = rssi
            rssi = gatherAverageRSSI(manufacturer, 7, scanner)
