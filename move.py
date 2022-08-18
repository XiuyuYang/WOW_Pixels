import time
import mouse
import keyboard

from utilities import get_delta_angle


class Move:
    def __init__(self):
        self.right_btn_is_pressed = False
        self.move_mouse_pos = (1000, 500)
        self.minimap = None
        self.rotate_speed = 2

    def rotate_to(self):
        self.minimap.get_target()
        self.minimap.get_minimap()
        self.minimap.get_orientation()
        delta_angle = get_delta_angle(self.minimap.orientation, self.minimap.move_angle)
        if delta_angle < 2:
            if self.right_btn_is_pressed:
                mouse.release("right")
                self.right_btn_is_pressed = False
            return

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

    def move_forward(self):
        keyboard.press("w")
        if self.minimap.distance < 2:
            # print("arrived", self.minimap.current_path_fname)
            self.minimap.load_next_path_img()

    def stop_moving(self):
        mouse.release("right")
        keyboard.release("w")

    def patrol(self):
        self.minimap.get_minimap()
        self.rotate_to()
        self.move_forward()
