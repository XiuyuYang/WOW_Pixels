import time

import cv2
import keyboard
import numpy as np

import move
import utilities


class Attack:
    def __init__(self):
        self.mv = move.Move()
        self.min_hp = 25
        self.min_mp = 25

    @staticmethod
    def search_target():
        key = "tab"
        keyboard.press_and_release(key)
        return utilities.find_target()

    @staticmethod
    def check_player_stat(stat_type):
        pointer = cv2.imread("Source_img/pointer.jpg")
        if stat_type == "hp":
            bbox = (108, 80, 245, 88)
            pointer = cv2.split(pointer)[0]
            img = utilities.get_screenshot(bbox)
            img = cv2.split(img)[2]
        elif stat_type == "mp":
            bbox = (108, 90, 245, 100)
            pointer = cv2.split(pointer)[0]
            img = utilities.get_screenshot(bbox)
            img = cv2.split(img)[2]
        else:
            return
        img *= 20
        img[img > 1] = 255
        # cv2.imshow('Computer Vision', img)
        res = cv2.matchTemplate(img, pointer, cv2.TM_CCOEFF_NORMED)
        loc = (cv2.minMaxLoc(res)[3][0], cv2.minMaxLoc(res)[3][1])
        return loc[0] / 133 * 100

    def check_hp(self):
        return self.check_player_stat("hp")

    def check_mp(self):
        return self.check_player_stat("mp")

    def face_to_target(self):
        self.mv.rotate_to_target()
        time.sleep(0.2)
        self.mv.stop_moving()


class Magic(Attack):
    def __init__(self):
        super(Magic, self).__init__()

    def cast(self, key):
        self.face_to_target()
        keyboard.press_and_release(key)

    def attack(self):
        self.face_to_target()
        while utilities.find_target(dead=False, threshold=0.5):  # check if target dead
            if not utilities.skill_in_range("1"):
                self.mv.go_to_target_range("1")
            self.cast("1")
            time.sleep(2)
        self.loot()

        print(self.check_hp())
        print(self.check_mp())
        if self.check_hp() < self.min_hp:
            keyboard.press_and_release("-")
            print("need hp")
            time.sleep(20)
        if self.check_mp() < self.min_mp:
            keyboard.press_and_release("=")
            print("need mana")
            time.sleep(20)
            keyboard.press_and_release("space")

    def loot(self):
        print("looting.")
        while not utilities.find_target(dead=True, threshold=0.5):
            keyboard.press_and_release("g")
        self.mv.rotate_to_target()
        time.sleep(5)


if __name__ == '__main__':
    a = Magic()
    utilities.set_foreground()
    print(a.face_to_target())
