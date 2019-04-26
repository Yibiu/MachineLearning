import time
import pymouse
import configparser


g_config_path = "./py_config.ini"


#
# point: [x, y, click, period], period in unit of second
# points: [point1, point2, ...]
#
# round: 测试轮数
# count: 测试点数
# 点击点(x,y)单/双击后停顿period秒时间
#
class AutoClick:
    def __init__(self):
        self.mouse = pymouse.PyMouse()
        self.round = 0
        self.points = []

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

    def run(self):
        print("************************ READING SETTINGS *********************")
        cf = configparser.ConfigParser()
        cf.read(g_config_path)
        self.round = cf.getint("POINTS", "round")
        count = cf.getint("POINTS", "count")
        for i in range(count):
            key = "point" + str(i)
            value = cf.get("POINTS", key)
            pt = []
            pt.append(int(value.split(",")[0]))
            pt.append(int(value.split(",")[1]))
            pt.append(int(value.split(",")[2]))
            pt.append(int(value.split(",")[3]))
            self.points.append(pt)
        print("Config:")
        print("round=%d" % self.round)
        print(self.points)
        print("")

        print("wait 2 secs to start...")
        time.sleep(2)
        print("************************ ROUND START **************************")
        for rd in range(self.round):
            print("-------------- round %d ------------" % rd)
            for pt in self.points:
                self.click_point(pt)
        print("************************* ROUND END **************************")


if __name__ == "__main__":
    test = AutoClick()
    test.run()
    input("enter to exit...")
