import pymouse
import time


# Get the mouse position
if __name__ == "__main__":
    mouse = pymouse.PyMouse()
    while True:
        print(mouse.position())
        time.sleep(2)


