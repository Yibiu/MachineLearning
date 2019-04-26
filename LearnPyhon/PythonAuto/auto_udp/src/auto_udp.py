import os
import time
import subprocess
import pymouse
import prettytable
import configparser


g_config_path = "./py_config.ini"


class DectKey:
    def __init__(self, pc_log, pc_start, pc_stop,
                 udp_log, udp_start, udp_stop,
                 udp_cvt_start, udp_cvt_stop,
                 client_log, client_start, client_stop):
        self.pc_log = pc_log
        self.pc_start = pc_start
        self.pc_stop = pc_stop
        self.udp_log = udp_log
        self.udp_start = udp_start
        self.udp_stop = udp_stop
        self.udp_cvt_start = udp_cvt_start
        self.udp_cvt_stop = udp_cvt_stop
        self.client_log = client_log
        self.client_start = client_start
        self.client_stop = client_stop


# mode: video/picture/ppt
# rounds: test rounds
# point: [x, y, click, period], period in unit of second
# start_count: {device: [pc udp display]}
class AutoUDP:
    def __init__(self, devs):
        self.mouse = pymouse.PyMouse()
        self.detect = DectKey("", "", "", "", "", "", "", "", "", "", "")
        self.devices = devs
        self.rounds = 0
        self.points = []
        # Variable params
        self.start_count = {}
        self.last_start_count = {}
        self.stop_count = {}
        self.last_stop_count = {}
        for dev in self.devices:
            self.start_count[dev] = [0, 0, 0, 0]
            self.last_start_count[dev] = [0, 0, 0, 0]
            self.stop_count[dev] = [0, 0, 0, 0]
            self.last_stop_count[dev] = [0, 0, 0, 0]
        # Table
        self.table = prettytable.PrettyTable(["Remote", "PC Start Count", "PC Stop Count",
                                              "UDP Start Count", "UDP Stop Count",
                                              "UDP CvtStart Count", "UDP CvtStop Count",
                                              "Client Start Count", "Client Stop Count",
                                              "Start", "Stop"])
        self.table.align["Remote"] = 1
        self.table.padding_width = 1

    def click_point(self, point):
        if 2 == point[2]:
            self.mouse.move(point[0], point[1])
            self.mouse.click(point[0], point[1])
            time.sleep(0.1)
            self.mouse.click(point[0], point[1])
            time.sleep(point[3])
        else:
            self.mouse.move(point[0], point[1])
            self.mouse.click(point[0], point[1])
            time.sleep(point[3])

    def get_settings(self):
        cf = configparser.ConfigParser()
        cf.read(g_config_path)
        self.rounds = cf.getint("COMMON", "round")
        count = cf.getint("COMMON", "count")
        for i in range(count):
            key = "point" + str(i)
            value = cf.get("COMMON", key)
            pt = []
            pt.append(int(value.split(",")[0]))
            pt.append(int(value.split(",")[1]))
            pt.append(int(value.split(",")[2]))
            pt.append(int(value.split(",")[3]))
            self.points.append(pt)
        self.detect.pc_log = cf.get("PC", "pc_log")
        self.detect.pc_start = cf.get("PC", "pc_start")
        self.detect.pc_stop = cf.get("PC", "pc_stop")
        self.detect.udp_log = cf.get("UDP", "udp_log")
        self.detect.udp_start = cf.get("UDP", "udp_start")
        self.detect.udp_stop = cf.get("UDP", "udp_stop")
        self.detect.udp_cvt_start = cf.get("UDP", "udp_cvt_start")
        self.detect.udp_cvt_stop = cf.get("UDP", "udp_cvt_stop")
        self.detect.client_log = cf.get("CLIENT", "client_log")
        self.detect.client_start = cf.get("CLIENT", "client_start")
        self.detect.client_stop = cf.get("CLIENT", "client_stop")
        # Print
        print("Config:")
        print("[COMMON]")
        print("round=%d" % self.rounds)
        print(self.points)
        print("[PC]")
        print("pc_log=%s" % self.detect.pc_log)
        print("pc_start=%s" % self.detect.pc_start)
        print("pc_stop=%s" % self.detect.pc_stop)
        print("[UDP]")
        print("udp_log=%s" % self.detect.udp_log)
        print("udp_start=%s" % self.detect.udp_start)
        print("udp_stop=%s" % self.detect.udp_stop)
        print("udp_cvt_start=%s" % self.detect.udp_cvt_start)
        print("udp_cvt_stop=%s" % self.detect.udp_cvt_stop)
        print("[CLIENT]")
        print("client_log=%s" % self.detect.client_log)
        print("client_start=%s" % self.detect.client_start)
        print("client_stop=%s" % self.detect.client_stop)
        print("")

    def init_rounds(self):
        for dev in self.devices:
            self.last_start_count[dev] = [0, 0, 0, 0]
            self.last_stop_count[dev] = [0, 0, 0, 0]
            # Local log
            if self.detect.pc_log != "":
                with open(self.detect.pc_log, 'r') as f:
                    for line in f.readlines():
                        if -1 != line.find(self.detect.pc_start):
                            self.last_start_count[dev][0] += 1
                        elif -1 != line.find(self.detect.pc_stop):
                            self.last_stop_count[dev][0] += 1
            # Remote udp log
            if self.detect.udp_log != "":
                for line in os.popen('adb -s %s shell cat %s' % (dev, self.detect.udp_log)):
                    if -1 != line.find(self.detect.udp_start):
                        self.last_start_count[dev][1] += 1
                    elif -1 != line.find(self.detect.udp_stop):
                        self.last_stop_count[dev][1] += 1
                    if -1 != line.find(self.detect.udp_cvt_start):
                        self.last_start_count[dev][2] += 1
                    elif -1 != line.find(self.detect.udp_cvt_stop):
                        self.last_stop_count[dev][2] += 1
            # Remote client log
            if self.detect.client_log != "":
                for line in os.popen('adb -s %s shell cat %s' % (dev, self.detect.client_log)):
                    if -1 != line.find(self.detect.client_start):
                        self.last_start_count[dev][3] += 1
                    elif -1 != line.find(self.detect.client_stop):
                        self.last_stop_count[dev][3] += 1

        # Print
        print("---------------- INIT ROUNDS ----------------")
        self.table.clear_rows()
        for dev in self.devices:
            self.table.add_row([dev, self.last_start_count[dev][0], self.last_stop_count[dev][0],
                                self.last_start_count[dev][1], self.last_stop_count[dev][1],
                                self.last_start_count[dev][2], self.last_stop_count[dev][2],
                                self.last_start_count[dev][3], self.last_stop_count[dev][3],
                                "PC->UDP->UDPCVT->CLIENT", "PC->UDP->UDPCVT->CLIENT"])
        print(self.table)
        print("")

    def uninit_rounds(self):
        # Print
        print("---------------- UNINIT ROUNDS ----------------")
        self.table.clear_rows()
        for dev in self.devices:
            self.table.add_row([dev, self.start_count[dev][0], self.stop_count[dev][0],
                                self.start_count[dev][1], self.stop_count[dev][1],
                                self.start_count[dev][2], self.stop_count[dev][2],
                                self.start_count[dev][3], self.stop_count[dev][3],
                                "PC->UDP->UDPCVT->CLIENT", "PC->UDP->UDPCVT->CLIENT"])
        print(self.table)
        print("")

    def before_round(self):
        pass

    def parse_round(self):
        for dev in self.devices:
            self.start_count[dev] = [0, 0, 0, 0]
            self.stop_count[dev] = [0, 0, 0, 0]
            # Local log
            if self.detect.pc_log != "":
                with open(self.detect.pc_log, 'r') as f:
                    for line in f.readlines():
                        if -1 != line.find(self.detect.pc_start):
                            self.start_count[dev][0] += 1
                        elif -1 != line.find(self.detect.pc_stop):
                            self.stop_count[dev][0] += 1
            # Remote udp log
            if self.detect.udp_log != "":
                for line in os.popen('adb -s %s shell cat %s' % (dev, self.detect.udp_log)):
                    if -1 != line.find(self.detect.udp_start):
                        self.start_count[dev][1] += 1
                    elif -1 != line.find(self.detect.udp_stop):
                        self.stop_count[dev][1] += 1
                    if -1 != line.find(self.detect.udp_cvt_start):
                        self.start_count[dev][2] += 1
                    elif -1 != line.find(self.detect.udp_cvt_stop):
                        self.stop_count[dev][2] += 1
            # Remote client log
            if self.detect.client_log != "":
                for line in os.popen('adb -s %s shell cat %s' % (dev, self.detect.client_log)):
                    if -1 != line.find(self.detect.client_start):
                        self.start_count[dev][3] += 1
                    elif -1 != line.find(self.detect.client_stop):
                        self.stop_count[dev][3] += 1

    def after_round(self):
        self.table.clear_rows()
        for dev in self.devices:
            pc_diff_start = self.start_count[dev][0] - self.last_start_count[dev][0]
            pc_diff_stop = self.stop_count[dev][0] - self.last_stop_count[dev][0]
            udp_diff_start = self.start_count[dev][1] - self.last_start_count[dev][1]
            udp_diff_stop = self.stop_count[dev][1] - self.last_stop_count[dev][1]
            udpcvt_diff_start = self.start_count[dev][2] - self.last_start_count[dev][2]
            udpcvt_diff_stop = self.stop_count[dev][2] - self.last_stop_count[dev][2]
            dis_diff_start = self.start_count[dev][3] - self.last_start_count[dev][3]
            dis_diff_stop = self.stop_count[dev][3] - self.last_stop_count[dev][3]
            start_proto = "PC(%d)->UDP(%d)->UDPCVT(%d)->CLIENT(%d)" % \
                          (pc_diff_start, udp_diff_start, udpcvt_diff_start, dis_diff_start)
            stop_proto = "PC(%d)->UDP(%d)->UDPCVT(%d)->CLIENT(%d)" % \
                         (pc_diff_stop, udp_diff_stop, udpcvt_diff_stop, dis_diff_stop)
            self.table.add_row([dev, self.start_count[dev][0], self.stop_count[dev][0],
                                self.start_count[dev][1], self.stop_count[dev][1],
                                self.start_count[dev][2], self.stop_count[dev][2],
                                self.start_count[dev][3], self.stop_count[dev][3],
                                start_proto, stop_proto])
        print(self.table)
        print("")
        for dev in self.devices:
            self.last_start_count[dev] = self.start_count[dev]
            self.last_stop_count[dev] = self.stop_count[dev]

    def test(self):
        print("*********************** SETTINGS ***********************")
        self.get_settings()

        print("*********************** ROUNDS ***********************")
        print("waitting 2s to run...")
        time.sleep(2)
        self.init_rounds()
        for rd in range(self.rounds):
            print("---------------- ROUND %d ----------------" % rd)
            self.before_round()
            for pt in self.points:
                self.click_point(pt)
            self.parse_round()
            self.after_round()
        self.uninit_rounds()


class RemoteDevices:
    def __init__(self):
        self.count = 0
        self.devices = []

    def run(self):
        # Enumerate all devices
        print("*********************** DEVICES ************************")
        p = subprocess.Popen("adb devices", stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            line_str = bytes.decode(line)
            if -1 != line_str.find("device"):
                if 0 != self.count:
                    self.devices.append(line_str.split()[0])
                self.count += 1
        for dev in self.devices:
            print("Remote: %s" % dev)
        print("")

        # Do auto test
        auto_test = AutoUDP(self.devices)
        auto_test.test()


if __name__ == "__main__":
    devices = RemoteDevices()
    devices.run()
    input("Enter to exit...")
