import time
import mouse
import keyboard


class Move:
    def __init__(self):
        self.move_mouse_pos = (1000, 500)
        self.minimap = None
        self.need_rotate = True
        self.need_move = True

    def rotate_to(self):
        if not self.need_rotate:
            return
        mouse.move(self.move_mouse_pos[0], self.move_mouse_pos[1])
        mouse.press("right")
        while True:
            self.minimap.get_minimap()
            self.minimap.get_orientation()
            delta_angle = abs(self.minimap.orientation - self.minimap.move_angle)
            if delta_angle < 3:
                mouse.release("right")
                self.need_rotate = False
                return
            # time.sleep(1 / 120)
            pos = mouse.get_position()
            if self.minimap.orientation < 180 and self.minimap.move_angle - self.minimap.orientation < 180 and self.minimap.move_angle > self.minimap.orientation:
                rotate_value = delta_angle / 2 + 1
            elif self.minimap.orientation > 180 and self.minimap.move_angle > self.minimap.orientation:
                rotate_value = delta_angle / 2 + 1
            elif self.minimap.orientation > 180 and self.minimap.move_angle < self.minimap.orientation - 180:
                rotate_value = delta_angle / 2 + 1
            else:
                rotate_value = -1 * delta_angle / 2 - 1
            mouse.move(pos[0] + rotate_value, pos[1])
            distance = self.minimap.distance

    def go_to(self):
        if not self.need_move:
            return
        keyboard.press("w")
        self.minimap.get_direction()
        print(self.minimap.distance)
        if self.minimap.distance < 3:
            keyboard.release("w")
            self.need_move = False
