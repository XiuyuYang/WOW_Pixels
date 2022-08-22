import time

import cv2
import keyboard
import numpy as np

import move
import utilities

skip = ["奥末忽灵"]


class Attack:
    def __init__(self):
        self.mv = move.Move()
        self.min_hp = 25
        self.min_mp = 25
        self.need_loot = False

    @staticmethod
    def search_target():
        key = "tab"
        keyboard.press_and_release(key)
        return utilities.find_target(skip=skip)

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
        # img = cv2.medianBlur(img,5)
        img[img > 1] = 255

        return int(list(img[1]).index(255)/135*100)

        cv2.imshow('Computer Vision', img)
        cv2.waitKey(1)

        return loc[0] / 133 * 100

    def check_hp(self):
        return self.check_player_stat("hp")

    def check_mp(self):
        return self.check_player_stat("mp")

    def face_to_target(self):
        self.mv.rotate_to_target()
        # need some time to rotate
        time.sleep(0.2)
        self.mv.stop_moving()

    def recover(self):
        hp = self.check_hp()
        mp = self.check_mp()
        print("hp:", int(hp))
        print("mp:", int(mp))

        if hp < self.min_hp or mp < self.min_mp:
            time.sleep(2)  # sleep for delay, GCD or jump
            if hp < self.min_hp:
                keyboard.press_and_release("-")
                print("need hp")
            if mp < self.min_mp:
                keyboard.press_and_release("=")
                print("need mana")

            time.sleep(20)
            keyboard.press_and_release("space")

class Magic(Attack):
    def __init__(self):
        super(Magic, self).__init__()

    def cast(self, key):
        keyboard.press_and_release(key)

    def attack(self):
        self.face_to_target()
        while True:
            # check if target dead
            if not utilities.find_target(dead=False, threshold=0.5):
                # multi target
                time.sleep(2)
                # if add target will show up
                if not utilities.find_target(dead=False, threshold=0.5):
                    break
            # make sure not too far
            if not utilities.skill_in_range("1"):
                print("skill not in range, moving.")
                self.mv.go_to_target_range("1")
            # skip when spelling
            if utilities.spelling_check():
                continue
            # attack
            else:
                # self.face_to_target()
                self.cast("1")
                # time.sleep(2.5)
        self.loot()
        self.recover()

    def loot(self):
        if not self.need_loot:
            return
        print("looting.")
        time.sleep(0.5)
        # if not utilities.find_target(dead=True, threshold=0.5):
        keyboard.press_and_release("g")
        self.mv.rotate_to_target()
        while True:
            if utilities.find_target(dead=True, threshold=0.8):
                print("target is dead, looting.")
                break
        time.sleep(2)


if __name__ == '__main__':
    while True:
        print(Attack.check_player_stat("mp"))