import time
import mouse
import keyboard

import utilities
from utilities import get_delta_angle


class Move:
    def __init__(self):
        self.right_btn_is_pressed = False  # mouse.is_pressed seems does not work here, so I set a flag
        self.move_mouse_pos = (1000, 500)
        self.minimap = None
        self.rotate_speed = 2
        mouse.move(self.move_mouse_pos[0], self.move_mouse_pos[1])

    def rotate_to(self):
        self.minimap.get_target()
        self.minimap.get_minimap()
        self.minimap.get_orientation()
        delta_angle = get_delta_angle(self.minimap.orientation, self.minimap.move_angle)
        if delta_angle < 2:
            if self.right_btn_is_pressed:
                mouse.release("right")
                self.right_btn_is_pressed = False
            return delta_angle

        if not self.right_btn_is_pressed:
            mouse.move(self.move_mouse_pos[0], self.move_mouse_pos[1])
            mouse.press("right")
            self.right_btn_is_pressed = True
        pos = mouse.get_position()

        # rotate to left or right
        if self.minimap.orientation < 180 \
                and self.minimap.move_angle - self.minimap.orientation < 180 \
                and self.minimap.move_angle > self.minimap.orientation:
            rotate_value = delta_angle
        elif 180 < self.minimap.orientation < self.minimap.move_angle:
            rotate_value = delta_angle
        elif self.minimap.orientation > 180 and self.minimap.move_angle < self.minimap.orientation - 180:
            rotate_value = delta_angle
        else:
            rotate_value = -1 * delta_angle

        mouse.move(pos[0] + rotate_value * self.rotate_speed, pos[1])
        return delta_angle

    def move_forward_patrol(self):
        keyboard.press_and_release("space")
        keyboard.press("w")
        if self.minimap.distance < 2:
            # print("arrived", self.minimap.current_path_fname)
            self.minimap.load_next_path_img()

    def move_forward(self):
        keyboard.press_and_release("space")
        if not keyboard.is_pressed("w"):
            keyboard.press("w")

    def rotate_to_target(self):
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
        self.minimap.get_minimap()
        self.rotate_to()
        self.move_forward_patrol()

    def go_to_target_range(self, index):
        while True:
            if not utilities.skill_in_range(index):
                print("target is out of range, moving to the target.")
                self.rotate_to_target()
                self.move_forward()
                time.sleep(1)
            else:
                self.stop_moving()
                return

    def move_back(self):
        self.minimap.get_target()
        if self.minimap.distance > 2:
            print("coming back. distance:", self.minimap.distance)
            self.right_btn_is_pressed = False
            self.minimap.get_minimap()
            self.rotate_speed = 1
            while True:
                angle = self.rotate_to()
                # print(angle)
                if angle < 2:
                    self.rotate_speed = 2
                    break
            # while True:
            #     self.minimap.get_target()
            #     if self.minimap.distance > 2:
            #         self.move_forward_patrol()
            #     else:
            #         break
            self.move_forward_patrol()
        print("moved back.")
