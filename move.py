import time
import mouse
import keyboard

import utilities
from utilities import get_delta_angle


class Move:
    def __init__(self):
        # self.right_btn_is_pressed = False  # mouse.is_pressed seems does not work here, so I set a flag
        self.move_time = time.time()
        self.move_mouse_pos = (1000, 500)
        self.minimap = None
        self.rotate_speed = 2
        mouse.move(self.move_mouse_pos[0], self.move_mouse_pos[1])

    def rotate_to(self):
        delta_angle = get_delta_angle(self.minimap.orientation, self.minimap.move_angle)
        if delta_angle < 2:
            # self.mouse_release_right()
            print("return rotate_to func")
            return delta_angle

        pos = mouse.get_position()
        print(pos,mouse.is_pressed("right"))

        # rotate to left or right
        if self.minimap.orientation < 180 \
                and self.minimap.move_angle - self.minimap.orientation < 180 \
                and self.minimap.move_angle > self.minimap.orientation:
            rotate_value = 1
        elif 180 < self.minimap.orientation < self.minimap.move_angle:
            rotate_value = 1
        elif self.minimap.orientation > 180 and self.minimap.move_angle < self.minimap.orientation - 180:
            rotate_value = 1
        else:
            rotate_value = -1
        rotate_value = rotate_value * delta_angle
        mouse.move(pos[0] + rotate_value * self.rotate_speed, pos[1])
        return delta_angle

    def mouse_press_right(self):
        print("move to screen middle and right click.")
        # mouse.release("right")
        mouse.move(self.move_mouse_pos[0], self.move_mouse_pos[1])
        # self.right_btn_is_pressed = True
        time.sleep(0.1)
        mouse.press("right")
        time.sleep(0.1)

    def mouse_release_right(self):
        # self.right_btn_is_pressed=False
        mouse.release("right")

    def move_forward(self):
        keyboard.press_and_release("space")
        if not keyboard.is_pressed("w"):
            keyboard.press("w")

    def interact_target(self):
        interact_key = "."
        keyboard.press_and_release(interact_key)

    def stop_moving(self):
        mouse.release("right")
        keyboard.release("w")
        # press w one more time for stop moving from right click or interact with target
        keyboard.press_and_release("w")
        # if utilities.find_target(dead=True):
        #     keyboard.press_and_release("tab")

    def patrol(self):
        if time.time() - self.move_time > 30:
            self.stuck()

        self.minimap.get_target()
        self.minimap.get_minimap()
        self.minimap.get_orientation()

        delta_angle = self.rotate_to()
        self.move_forward()
        print("distance:", int(self.minimap.distance), "delta:", delta_angle)
        if self.minimap.distance < 5:
            # print("arrived", self.minimap.current_path_fname)
            self.minimap.load_next_path_img()
            self.move_time = time.time()

    def go_to_target_range(self, index):
        self.move_time = time.time()
        while True:
            self.stuck()
            if not utilities.skill_in_range(index):
                print("target is out of range, moving to the target.")
                self.interact_target()
                self.move_forward()
                time.sleep(1)
            else:
                self.stop_moving()
                return

    def move_back(self):
        print("finished combat, coming back.")
        utilities.mount()
        self.move_time = time.time()
        self.mouse_press_right()
        while True:
            self.patrol()
            if self.minimap.distance < 10:
                print("moved back.")
                return

    def stuck(self):
        print("stucked.")
        keyboard.press_and_release("w")
        keyboard.press("s")
        time.sleep(3)
        keyboard.release("s")
        keyboard.press("a")
        time.sleep(3)
        keyboard.release("a")
        keyboard.press("w")
        time.sleep(3)
        keyboard.release("w")
        self.move_time = time.time()


if __name__ == '__main__':
    time.sleep(4)
    pos = mouse.get_position()
    mouse.move(pos[0] + 800, pos[1], duration=1)
