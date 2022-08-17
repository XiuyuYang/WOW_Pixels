import time
import mouse
import keyboard

from utilities import get_delta_angle


class Move:
    def __init__(self):
        self.move_mouse_pos = (1000, 500)
        self.minimap = None
        self.need_rotate = True
        self.need_move = True

    def rotate_to(self):
        if not self.need_rotate:
            return
        self.minimap.get_target()
        mouse.move(self.move_mouse_pos[0], self.move_mouse_pos[1])
        mouse.press("right")
        while True:
            self.minimap.get_minimap()
            self.minimap.get_orientation()
            delta_angle = get_delta_angle(self.minimap.orientation, self.minimap.move_angle)
            if delta_angle < 2:
                mouse.release("right")
                self.need_rotate = False
                self.need_move = True
                return
            # time.sleep(1 / 120)
            pos = mouse.get_position()
            if self.minimap.orientation < 180 \
                    and self.minimap.move_angle - self.minimap.orientation < 180 \
                    and self.minimap.move_angle > self.minimap.orientation:
                rotate_value = delta_angle / 2 + 1
            elif 180 < self.minimap.orientation < self.minimap.move_angle:
                rotate_value = delta_angle / 2 + 1
            elif self.minimap.orientation > 180 and self.minimap.move_angle < self.minimap.orientation - 180:
                rotate_value = delta_angle / 2 + 1
            else:
                rotate_value = -1 * delta_angle / 2 - 1
            mouse.move(pos[0] + rotate_value, pos[1])

    def go_to(self):
        if not self.need_move:
            return
        self.minimap.get_target()
        keyboard.press("w")
        if self.minimap.distance < 1:
            print("arrived", self.minimap.current_path_fname)
            self.minimap.load_next_path_img()
            self.need_rotate = True
            keyboard.release("w")
            self.need_move = False
