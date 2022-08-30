import time

import cv2
import keyboard
import numpy as np

import move
import utilities

skip = []


class Attack:
    def __init__(self):
        self.target_hp_befor = 100
        self.mv = move.Move()
        self.min_hp = 50
        self.min_mp = 35
        self.need_loot = False
        self.target_hp = None
        self.start_fight = None
        self.skinning = False

    def search_target(self):
        # print("searching target.")
        key = "tab"
        keyboard.press_and_release(key)
        time.sleep(0.2)
        keyboard.press_and_release("2")
        if utilities.find_target(skip=skip):
            self.face_to_target(force=True)
            print("found the target.")
            return True
        else:
            return False

    def attack(self):
        self.mv.stop_moving()
        utilities.run_macro('''/script SetRaidTarget('target', 8);''')
        while True:
            # make sure not too far
            if not utilities.skill_in_range("1"):
                print("skill not in range, moving.")
                self.mv.go_to_target_range("1")
            # skip when spelling
            if utilities.spelling_check():
                continue
            # attack
            else:
                self.face_to_target()
                self.attack_loop()
                if self.check_overtime(wait=20):
                    print("Cannot attack the target.")
                    utilities.run_macro("/cleartarget")
                    self.mv.stuck()
                    self.update_fight_time(reset=True)
                    return
            # check if target dead
            if not utilities.find_target(dead=False, threshold=0.5):
                # multi target
                time.sleep(1)
                # if add target will show up
                if not utilities.find_target(dead=False, threshold=0.5):
                    self.update_fight_time(reset=True)
                    break
                else:
                    return

        self.loot()
        self.skin()
        self.recover()

        self.after_battle()

    def attack_loop(self):
        pass

    def after_battle(self):
        pass

    def cast(self, key):
        keyboard.press_and_release(key)

    @staticmethod
    def check_stat(stat_type):
        if stat_type == "hp":
            bbox = (108, 80, 245, 88)
            img = utilities.get_screenshot(bbox)
            img = cv2.split(img)[2]
        elif stat_type == "mp":
            bbox = (108, 90, 245, 100)
            img = utilities.get_screenshot(bbox)
            img = cv2.split(img)[2]
        elif stat_type == "enimy":
            bbox = (304, 80, 440, 88)
            img = utilities.get_screenshot(bbox)
            img = cv2.split(img)[0]
        else:
            return
        img *= 20
        img[img > 1] = 255

        list_line = list(img[1])
        list_line.append(255)
        index = list_line.index(255)
        percent = int(index / 135 * 100)
        return percent

    def check_hp(self):
        return self.check_stat("hp")

    def check_mp(self):
        return self.check_stat("mp")

    def check_target_hp(self):
        self.target_hp = self.check_stat("enimy")
        return self.target_hp

    def face_to_target(self, force=False):
        # init target hp
        self.check_target_hp()
        if force:
            self.target_hp_befor = self.target_hp - 1

        if self.target_hp == self.target_hp_befor:
            return
        elif self.target_hp < self.target_hp_befor:
            # if target get hit, then update hp
            self.target_hp_befor = self.target_hp
            self.update_fight_time()
            return
        else:
            self.target_hp_befor = self.target_hp
            print(self.target_hp, self.target_hp_befor)
            # if target get heal or add a new enimy then face to it.
            print("facing to target.")
            self.mv.interact_target()
            # need some time to rotate
            time.sleep(0.2)
            self.mv.stop_moving()

    def recover(self):
        hp = self.check_hp()
        mp = self.check_mp()
        print("hp:", int(hp))
        print("mp:", int(mp))

        if hp < self.min_hp or mp < self.min_mp:
            # time.sleep(2)  # sleep for delay, GCD or jump
            if hp < self.min_hp:
                keyboard.press_and_release(12)  # if use str "-", it will use digit keyboard "-"
                print("need hp")
            if mp < self.min_mp:
                keyboard.press_and_release("=")
                print("need mana")

            start_eat = time.time()
            time.sleep(0.5)
            while True:
                if utilities.find_target():
                    print("player has been attacked.")
                    return
                if time.time() - start_eat > 20:
                    keyboard.press_and_release("space")
                    return

    def loot(self):
        if not self.need_loot:
            return
        print("looting.")
        # if not utilities.find_target(dead=True, threshold=0.5):
        keyboard.press_and_release("g")
        self.mv.interact_target()
        time.sleep(0.1)
        dead_time = time.time()
        while True:
            if not utilities.find_target(dead=True, threshold=0.5):
                print("got items.")
                break
            if time.time() - dead_time > 8:
                print("loot over time, continue.")
                utilities.run_macro("/cleartarget")
                break
            time.sleep(1)

    def skin(self):
        time.sleep(0.5)
        print("skinning.")
        if self.skinning:
            skinable = None
            while True:
                keyboard.press_and_release("g")
                time.sleep(0.1)
                self.mv.interact_target()
                time.sleep(2)
                if skinable is None:
                    skinable = utilities.spelling_check()
                if not skinable:
                    print("target is not skinable.")
                    utilities.run_macro("/cleartarget")
                    return
                time.sleep(2)
                if not utilities.find_target(dead=True, threshold=0.5):
                    break
                print("skin failed, try again.")
            print("skin successful.")

    def update_fight_time(self, reset=False):
        if reset:
            self.start_fight = None
            return
        self.start_fight = time.time()

    def check_overtime(self, wait=10):
        if self.start_fight is None:
            self.start_fight = time.time()
            return
        fight_time = time.time() - self.start_fight
        # print("fight_time:", fight_time)
        if fight_time > wait and (self.target_hp == 100):
            return True
        else:
            return False


class Magic(Attack):
    def __init__(self):
        super(Magic, self).__init__()

    def attack_loop(self):
        self.cast("1")

    def after_battle(self):
        self.make_supply()

    @staticmethod
    def make_supply():
        # food
        make_icon = utilities.get_skill_img(9)
        use_icon = utilities.get_skill_img(11)
        has_food = utilities.compair_birghtness(make_icon, use_icon)
        # water
        make_icon = utilities.get_skill_img(10)
        use_icon = utilities.get_skill_img(12)
        has_water = utilities.compair_birghtness(make_icon, use_icon)

        if not has_food:
            keyboard.press_and_release("9")
            time.sleep(3.5)
        if not has_water:
            keyboard.press_and_release("0")
            time.sleep(3.5)


class Druid(Attack):
    def __init__(self):
        super(Druid, self).__init__()

    def attack(self):
        self.mv.stop_moving()
        utilities.run_macro('''/script SetRaidTarget('target', 8);''')
        utilities.run_macro('''/startattack''')
        while True:
            self.face_to_target()
            if self.check_overtime(wait=20):
                print("Cannot attack the target.")
                utilities.run_macro("/cleartarget")
                self.mv.stuck()
                self.update_fight_time(reset=True)
                return
            # check if target dead
            if not utilities.find_target(dead=False, threshold=0.7):
                break
            self.attack_loop()
        self.update_fight_time(reset=True)

        time.sleep(2)
        self.loot()
        self.skin()
        self.recover()

        self.after_battle()

    def attack_loop(self):
        # print("attacking")
        keyboard.press("space")
        time.sleep(1)
        keyboard.press_and_release(".")
        self.cast("1")
        keyboard.release("space")
        if self.check_hp() < 50:
            self.cast("9")

    def recover(self):
        hp = self.check_hp()
        # print("hp:", int(hp))

        if hp < self.min_hp:
            # time.sleep(2)  # sleep for delay, GCD or jump
            if hp < self.min_hp:
                print("need hp")
                keyboard.press_and_release(12)
                time.sleep(3.5)
                self.cast("5")


if __name__ == '__main__':
    utilities.set_foreground()
    m = Druid()
    print(utilities.find_target(dead=True, threshold=0.5))
    # print(m.check_stat("hp"))
    # print(m.check_stat("mp"))
    # for i in range(10):
    #     print(next(keyboard._winkeyboard.map_name("k")))
    # keyboard.press_and_release(12)
