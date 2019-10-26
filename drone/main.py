import bluepy
import sys
import time
import binascii
from drone import Drone, TaggedMarkers, Marker
from statistics import stdev, mean
from bluepy.btle import DefaultDelegate, BluepyHelper, BTLEException, ScanEntry


manufacturer = sys.argv[1]

print "scanning for device with manufacture data |" + manufacturer + "|"

# create a delegate class to receive the BLE broadcast packets


class Scanner(BluepyHelper):

    def __init__(self, iface=0):
        BluepyHelper.__init__(self)
        self.scanned = {}
        self.iface = iface
        self.passive = False

    def _cmd(self):
        return "pasv" if self.passive else "scan"

    def start(self, passive=False):
        self.passive = passive
        self._startHelper(iface=self.iface)
        self._mgmtCmd("le on")
        self._writeCmd(self._cmd()+"\n")
        rsp = self._waitResp("mgmt")
        if rsp["code"][0] == "success":
            return
        # Sometimes previous scan still ongoing
        if rsp["code"][0] == "busy":
            self._mgmtCmd(self._cmd()+"end")
            rsp = self._waitResp("stat")
            assert rsp["state"][0] == "disc"
            self._mgmtCmd(self._cmd())

    def stop(self):
        self._mgmtCmd(self._cmd()+"end")
        self._stopHelper()

    def clear(self):
        self.scanned = {}

    def process(self, timeout=10.0):
        if self._helper is None:
            raise BTLEException(BTLEException.INTERNAL_ERROR,
                                "Helper not started (did you call start()?)")
        start = time.time()
        while True:
            if timeout:
                remain = start + timeout - time.time()
                if remain <= 0.0:
                    break
            else:
                remain = None
            resp = self._waitResp(['scan', 'stat'], remain)
            if resp is None:
                break

            respType = resp['rsp'][0]
            if respType == 'stat':
                # if scan ended, restart it
                if resp['state'][0] == 'disc':
                    self._mgmtCmd("scan")

            elif respType == 'scan':
                # device found
                addr = binascii.b2a_hex(resp['addr'][0]).decode('utf-8')
                addr = ':'.join([addr[i:i+2] for i in range(0, 12, 2)])
                if addr in self.scanned:
                    dev = self.scanned[addr]
                else:
                    dev = ScanEntry(addr, self.iface)
                    self.scanned[addr] = dev
                isNewData = dev._update(resp)
                if self.delegate is not None:
                    self.delegate.handleDiscovery(
                        dev, (dev.updateCount <= 1), isNewData)

            else:
                raise BTLEException(
                    BTLEException.INTERNAL_ERROR, "Unexpected response: " + respType)

    def gatherAverageRSSI(self, manufacturer, n_samples, passive=False):
        self.clear()
        self.start(passive=passive)

        rssi_scans = []

        while len(rssi_scans) < n_samples:
            # wait 3 seconds before a timeout
            resp = self._waitResp(['scan', 'stat'], 3.0)
            #                                        ^

            if resp is None:
                break

            respType = resp['rsp'][0]
            if respType == 'stat':
                # if scan ended, restart it
                if resp['state'][0] == 'disc':
                    self._mgmtCmd("scan")

            elif respType == 'scan':
                # device found
                addr = binascii.b2a_hex(resp['addr'][0]).decode('utf-8')
                addr = ':'.join([addr[i:i+2] for i in range(0, 12, 2)])
                if addr in self.scanned:
                    dev = self.scanned[addr]
                else:
                    dev = ScanEntry(addr, self.iface)
                    self.scanned[addr] = dev
                isNewData = dev._update(resp)

                for (adtype, desc, value) in dev.getScanData():
                    if desc == "Manufacturer" and value == manufacturer:
                        rssi_scans.append(dev.rssi)

            else:
                raise BTLEException(
                    BTLEException.INTERNAL_ERROR, "Unexpected response: " + respType)

        mean_rssi = mean(rssi_scans)

        std_dev = stdev(rssi_scans)

        cutoff_rssi = []

        lower_cutoff = mean_rssi - std_dev
        upper_cutoff = mean_rssi + std_dev

        for x in rssi_scans:
            if not (x < lower_cutoff or x > upper_cutoff):
                cutoff_rssi.append(x)

        self.stop()
        return mean(cutoff_rssi)

    def getDevices(self):
        return self.scanned.values()

    def scan(self, timeout=10, passive=False):
        self.clear()
        self.start(passive=passive)
        self.process(timeout)
        self.stop()
        return self.getDevices()


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
    rssi = scanner.gatherAverageRSSI(manufacturer, 7, scanner)
    if last_rssi > rssi:
        drone.rotate(90)
        drone.rotate(90)
        drone.moveForward(mv_distance / 2)
        drone.rotate(rotate_dir * 90)
        last_rssi = rssi
        rssi = scanner.gatherAverageRSSI(manufacturer, 7, scanner)
        mv_distance = abs(rssi) * 0.02
        drone.moveForward(mv_distance)
        last_rssi = rssi
        rssi = scanner.gatherAverageRSSI(manufacturer, 7, scanner)
        if last_rssi > rssi:
            rotate_dir = rotate_dir * -1
            drone.rotate(90)
            drone.rotate(90)
            drone.moveForward(mv_distance * 2)
            last_rssi = rssi
            rssi = scanner.gatherAverageRSSI(manufacturer, 7, scanner)

drone.land()
